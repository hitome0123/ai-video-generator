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

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .config import settings
from .image_processor import ImageProcessor
from .prompt_generator import PromptGenerator
from .video_generator import VideoGenerator
from .post_processor import PostProcessor
from .competitor_analyzer import suggest_selling_points, analyze_competitor_text
from . import database as db
from . import batch_processor as bp


app = FastAPI(title="AI Video Generator")

# 内存任务状态（供实时轮询用，同时写入 SQLite 持久化）
jobs: dict = {}


def run_pipeline(
    job_id: str,
    image_path: str,
    product_name: str,
    selling_points: List[str],
    video_service: str = "seedance",
    add_subtitle: bool = False,
    add_bgm: bool = False,
):
    """
    后台线程：执行完整的视频生成流程

    步骤:
    1. 图片处理（GPT-4o Vision 分析 + DALL-E 3 白底图）
    2. 脚本生成（GPT-4o 视频脚本 + Prompt）
    3. 视频生成（Seedance / Creatok）
    4. 后处理（字幕 + BGM，按需执行）
    """
    output_dir = settings.output_dir / job_id
    output_dir.mkdir(parents=True, exist_ok=True)

    def _update(data: dict):
        jobs[job_id].update(data)
        db.update_job(job_id, **data)

    try:
        # ── 步骤 1: 图片处理 ──────────────────────────────────────
        _update({"status": "processing", "step": 1, "step_name": "分析产品图片"})

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
        _update({"step": 2, "step_name": "生成视频脚本"})

        duration = 5 if video_service == "seedance" else 15
        generator = PromptGenerator()
        prompt_result = generator.generate_complete_prompt(
            product_name=product_name,
            product_description=product_description,
            selling_points=selling_points,
            duration=duration
        )

        video_prompt = prompt_result["video_prompt"]
        script = prompt_result["script"]

        # 保存脚本和 Prompt 到文件
        with open(output_dir / "script.json", "w", encoding="utf-8") as f:
            json.dump(script, f, ensure_ascii=False, indent=2)
        with open(output_dir / "video_prompt.txt", "w", encoding="utf-8") as f:
            f.write(video_prompt)

        # ── 步骤 3: 生成视频 ─────────────────────────────────────
        service_label = "豆包 Seedance" if video_service == "seedance" else "Creatok"
        _update({"step": 3, "step_name": f"AI 生成视频（{service_label}，约 2-3 分钟）"})

        safe_name = product_name.replace(" ", "_").replace("/", "_")
        raw_video_path = output_dir / f"{safe_name}_raw.mp4"
        final_video_path = output_dir / f"{safe_name}.mp4"

        video_gen = VideoGenerator()
        video_result = video_gen.generate_video(
            prompt=video_prompt,
            output_path=str(raw_video_path),
            reference_image_path=processed_image_path,
            duration=duration,
            backend=video_service,
            wait=True
        )

        if video_result["status"] != "success":
            raise Exception(video_result.get("error", "视频生成失败，请稍后重试"))

        # ── 步骤 4: 后处理（字幕 / BGM）────────────────────────
        if add_subtitle or add_bgm:
            _update({"step": 4, "step_name": "后处理（字幕 / BGM）"})
            pp = PostProcessor()
            pp.process(
                video_path=str(raw_video_path),
                output_path=str(final_video_path),
                script=script if add_subtitle else None,
                add_subtitle=add_subtitle,
                add_bgm=add_bgm,
            )
        else:
            shutil.copy2(str(raw_video_path), str(final_video_path))

        # 清理临时原始视频
        try:
            raw_video_path.unlink(missing_ok=True)
        except Exception:
            pass

        _update({
            "status": "success",
            "step_name": "生成完成",
            "video_path": str(final_video_path),
            "script": json.dumps(script, ensure_ascii=False),
            "video_prompt": video_prompt,
        })

    except Exception as e:
        _update({"status": "failed", "error": str(e)})

    finally:
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
    selling_points: str = Form(..., description="卖点列表（每行一个）"),
    video_service: str = Form("seedance", description="视频生成服务：seedance 或 creatok"),
    add_subtitle: str = Form("false", description="是否添加字幕"),
    add_bgm: str = Form("false", description="是否混入 BGM"),
):
    """开始生成视频任务，返回 job_id"""
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="请上传图片文件（JPG/PNG）")

    if video_service not in ("seedance", "creatok"):
        raise HTTPException(status_code=400, detail="video_service 只支持 seedance 或 creatok")

    points = [p.strip() for p in selling_points.strip().splitlines() if p.strip()]
    if not points:
        raise HTTPException(status_code=400, detail="请至少填写一个卖点")
    if len(points) > 10:
        raise HTTPException(status_code=400, detail="卖点最多填写 10 个")

    sub = add_subtitle.lower() in ("true", "1", "yes")
    bgm = add_bgm.lower() in ("true", "1", "yes")

    upload_dir = settings.temp_dir / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(image.filename).suffix if image.filename else ".jpg"
    job_id = str(uuid.uuid4())
    image_path = upload_dir / f"{job_id}{suffix}"

    content = await image.read()
    with open(image_path, "wb") as f:
        f.write(content)

    # 初始化内存状态
    jobs[job_id] = {
        "status": "queued",
        "step": 0,
        "step_name": "等待中",
        "product_name": product_name,
        "video_service": video_service,
        "add_subtitle": sub,
        "add_bgm": bgm,
    }

    # 持久化到数据库
    db.create_job(
        job_id=job_id,
        product_name=product_name,
        video_service=video_service,
        add_subtitle=sub,
        add_bgm=bgm,
    )

    t = threading.Thread(
        target=run_pipeline,
        args=(job_id, str(image_path), product_name, points, video_service, sub, bgm),
        daemon=True
    )
    t.start()

    return {"job_id": job_id}


@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    """查询任务状态和进度"""
    # 优先从内存中读（内存有则说明任务是本次启动后创建的）
    job = jobs.get(job_id)
    if not job:
        # 尝试从数据库恢复（跨重启）
        job = db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="任务不存在")

    return {
        "status": job["status"],
        "step": job.get("step", 0),
        "step_name": job.get("step_name", ""),
        "error": job.get("error"),
        "product_name": job.get("product_name", ""),
    }


@app.get("/api/download/{job_id}")
async def download_video(job_id: str):
    """下载生成的视频文件"""
    job = jobs.get(job_id) or db.get_job(job_id)
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


@app.get("/api/history")
async def get_history():
    """获取历史任务列表（最近 50 条）"""
    records = db.list_jobs(limit=50)
    result = []
    for r in records:
        result.append({
            "job_id": r["job_id"],
            "product_name": r["product_name"],
            "status": r["status"],
            "video_service": r["video_service"],
            "add_subtitle": r["add_subtitle"],
            "add_bgm": r["add_bgm"],
            "created_at": r["created_at"],
            "has_video": bool(r.get("video_path") and Path(r["video_path"]).exists()),
        })
    return result


@app.delete("/api/history/{job_id}")
async def delete_history(job_id: str):
    """删除任务记录及对应视频文件"""
    record = db.get_job(job_id)
    if not record:
        raise HTTPException(status_code=404, detail="任务不存在")

    # 删除视频输出目录
    job_dir = settings.output_dir / job_id
    if job_dir.exists():
        shutil.rmtree(job_dir, ignore_errors=True)

    db.delete_job(job_id)

    # 同步清理内存
    jobs.pop(job_id, None)

    return {"status": "deleted"}


@app.post("/api/batch")
async def start_batch(
    items: str = Body(..., embed=True, description='[{"product_name":"...","selling_points":["..."]}]'),
    video_service: str = Body("seedance", embed=True),
    add_subtitle: bool = Body(False, embed=True),
    add_bgm: bool = Body(False, embed=True),
):
    """
    启动批量视频生成任务

    items 格式：[{"product_name": "产品名", "selling_points": ["卖点1", "卖点2"]}, ...]
    """
    import json as _json

    if isinstance(items, str):
        try:
            items_list = _json.loads(items)
        except Exception:
            raise HTTPException(status_code=400, detail="items 格式错误，需为 JSON 数组")
    else:
        items_list = items

    if not isinstance(items_list, list) or len(items_list) == 0:
        raise HTTPException(status_code=400, detail="至少需要 1 个产品")
    if len(items_list) > 20:
        raise HTTPException(status_code=400, detail="单次批量最多 20 个产品")

    for item in items_list:
        if not item.get("product_name", "").strip():
            raise HTTPException(status_code=400, detail="每个产品必须填写产品名称")
        if not item.get("selling_points"):
            raise HTTPException(status_code=400, detail=f"产品「{item.get('product_name')}」至少需要 1 个卖点")

    if video_service not in ("seedance", "creatok"):
        raise HTTPException(status_code=400, detail="video_service 只支持 seedance 或 creatok")

    batch_id = bp.start_batch(
        items=items_list,
        video_service=video_service,
        add_subtitle=add_subtitle,
        add_bgm=add_bgm,
    )
    return {"batch_id": batch_id, "total": len(items_list)}


@app.get("/api/batch/{batch_id}")
async def get_batch_status(batch_id: str):
    """查询批量任务进度"""
    job = bp.get_batch(batch_id)
    if not job:
        raise HTTPException(status_code=404, detail="批量任务不存在")

    return {
        "batch_id": job.batch_id,
        "status": job.status,
        "total": job.total,
        "completed": job.completed,
        "failed": job.failed,
        "items": [
            {
                "item_id": item.item_id,
                "product_name": item.product_name,
                "status": item.status,
                "error": item.error,
            }
            for item in job.items
        ],
    }


@app.get("/api/batch/{batch_id}/download")
async def download_batch(batch_id: str):
    """下载批量任务的所有视频（ZIP 格式）"""
    job = bp.get_batch(batch_id)
    if not job:
        raise HTTPException(status_code=404, detail="批量任务不存在")
    if job.status != "done":
        raise HTTPException(status_code=400, detail="批量任务尚未完成")

    zip_path = bp.create_zip(batch_id)
    if not zip_path:
        raise HTTPException(status_code=404, detail="没有成功生成的视频")

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename=f"batch_videos_{batch_id[:8]}.zip",
    )


@app.post("/api/suggest-selling-points")
async def api_suggest_selling_points(
    product_name: str = Body(..., embed=True),
    existing_points: List[str] = Body(default=[], embed=True),
):
    """AI 卖点建议：根据产品名称 + 已有卖点，返回补充建议"""
    if not product_name.strip():
        raise HTTPException(status_code=400, detail="产品名称不能为空")

    result = suggest_selling_points(
        product_name=product_name.strip(),
        existing_points=existing_points,
    )

    if result["status"] == "error":
        raise HTTPException(status_code=503, detail=result["reason"])

    return {"suggestions": result["suggestions"]}


@app.post("/api/analyze-competitor")
async def api_analyze_competitor(
    text: str = Body(..., embed=True),
):
    """分析竞品文案，提取卖点和钩子"""
    if not text.strip():
        raise HTTPException(status_code=400, detail="竞品文案不能为空")

    result = analyze_competitor_text(text.strip())

    if result["status"] == "error":
        raise HTTPException(status_code=503, detail=result["reason"])

    return {
        "selling_points": result["selling_points"],
        "hook_ideas": result["hook_ideas"],
        "summary": result["summary"],
    }


# ── 挂载静态文件（必须放在所有 API 路由之后）────────────────────
static_dir = Path(__file__).parent.parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
