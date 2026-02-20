"""
AI Video Generator - Web API 服务
提供 REST API 接口，供前端页面调用
"""
import json
import uuid
import threading
import shutil
from pathlib import Path
from typing import List

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .config import settings
from .image_processor import ImageProcessor
from .prompt_generator import PromptGenerator
from .video_generator import VideoGenerator


app = FastAPI(title="AI Video Generator")

# 内存中的任务状态存储（重启后清空）
jobs: dict = {}


def run_pipeline(
    job_id: str,
    image_path: str,
    product_name: str,
    selling_points: List[str]
):
    """
    后台线程：执行完整的视频生成流程

    步骤:
    1. 图片处理（GPT-4o Vision 分析 + DALL-E 3 白底图）
    2. 脚本生成（GPT-4o 视频脚本 + Prompt）
    3. 视频生成（Creatok API）
    """
    output_dir = settings.output_dir / job_id
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # ── 步骤 1: 图片处理 ──────────────────────────────────────
        jobs[job_id].update({
            "status": "processing",
            "step": 1,
            "step_name": "分析产品图片"
        })

        processor = ImageProcessor()
        image_result = processor.process_image(
            input_path=image_path,
            output_dir=str(output_dir / "processed")
        )

        if image_result["status"] != "success":
            raise Exception("图片处理失败，请检查图片是否清晰")

        product_description = image_result["analysis"].get(
            "white_bg_prompt",
            image_result["analysis"].get("description", "")
        )
        processed_image_path = image_result["output_path"]

        # ── 步骤 2: 生成脚本和 Prompt ────────────────────────────
        jobs[job_id].update({
            "step": 2,
            "step_name": "生成视频脚本"
        })

        generator = PromptGenerator()
        prompt_result = generator.generate_complete_prompt(
            product_name=product_name,
            product_description=product_description,
            selling_points=selling_points,
            duration=15
        )

        video_prompt = prompt_result["video_prompt"]
        script = prompt_result["script"]

        # 保存脚本和 Prompt 到文件
        with open(output_dir / "script.json", "w", encoding="utf-8") as f:
            json.dump(script, f, ensure_ascii=False, indent=2)
        with open(output_dir / "video_prompt.txt", "w", encoding="utf-8") as f:
            f.write(video_prompt)

        # ── 步骤 3: 生成视频 ─────────────────────────────────────
        jobs[job_id].update({
            "step": 3,
            "step_name": "AI 生成视频（约 2-3 分钟）"
        })

        safe_name = product_name.replace(" ", "_").replace("/", "_")
        video_output_path = output_dir / f"{safe_name}.mp4"

        video_gen = VideoGenerator()
        video_result = video_gen.generate_video(
            prompt=video_prompt,
            output_path=str(video_output_path),
            reference_image_path=processed_image_path,
            duration=15,
            wait=True
        )

        if video_result["status"] == "success":
            jobs[job_id].update({
                "status": "success",
                "step": 3,
                "step_name": "生成完成",
                "video_path": str(video_output_path),
                "script": script,
                "video_prompt": video_prompt
            })
        else:
            raise Exception(video_result.get("error", "视频生成失败，请稍后重试"))

    except Exception as e:
        jobs[job_id].update({
            "status": "failed",
            "error": str(e)
        })

    finally:
        # 清理上传的临时图片
        try:
            Path(image_path).unlink(missing_ok=True)
        except Exception:
            pass


# ────────────────────────────────────────────────────────────
# API 路由（必须在 StaticFiles 挂载之前注册）
# ────────────────────────────────────────────────────────────

@app.post("/api/generate")
async def start_generation(
    image: UploadFile = File(..., description="产品图片"),
    product_name: str = Form(..., description="产品名称"),
    selling_points: str = Form(..., description="卖点列表（每行一个）")
):
    """
    开始生成视频任务

    返回 job_id，前端通过 /api/status/{job_id} 轮询进度
    """
    # 验证文件类型
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片文件（JPG/PNG）")

    # 解析卖点（每行一个）
    points = [p.strip() for p in selling_points.strip().splitlines() if p.strip()]
    if not points:
        raise HTTPException(status_code=400, detail="请至少填写一个卖点")
    if len(points) > 10:
        raise HTTPException(status_code=400, detail="卖点最多填写 10 个")

    # 保存上传的图片到临时目录
    upload_dir = settings.temp_dir / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(image.filename).suffix if image.filename else ".jpg"
    job_id = str(uuid.uuid4())
    image_path = upload_dir / f"{job_id}{suffix}"

    content = await image.read()
    with open(image_path, "wb") as f:
        f.write(content)

    # 初始化任务状态
    jobs[job_id] = {
        "status": "queued",
        "step": 0,
        "step_name": "等待中",
        "product_name": product_name
    }

    # 启动后台线程
    t = threading.Thread(
        target=run_pipeline,
        args=(job_id, str(image_path), product_name, points),
        daemon=True
    )
    t.start()

    return {"job_id": job_id}


@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """查询任务状态和进度"""
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="任务不存在")

    # 只返回前端需要的字段，不暴露文件路径
    return {
        "status": job["status"],
        "step": job.get("step", 0),
        "step_name": job.get("step_name", ""),
        "error": job.get("error"),
        "product_name": job.get("product_name", "")
    }


@app.get("/api/download/{job_id}")
async def download_video(job_id: str):
    """下载生成的视频文件"""
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="任务不存在")
    if job["status"] != "success":
        raise HTTPException(status_code=400, detail="视频尚未生成完成")

    video_path = Path(job["video_path"])
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="视频文件不存在，可能已被清理")

    safe_name = job.get("product_name", "video").replace(" ", "_")
    return FileResponse(
        str(video_path),
        media_type="video/mp4",
        filename=f"{safe_name}.mp4"
    )


# ── 挂载静态文件（必须放在所有 API 路由之后）────────────────────
static_dir = Path(__file__).parent.parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
