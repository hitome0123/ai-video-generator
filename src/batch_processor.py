"""
批量处理模块
功能：支持多产品队列生成，逐个处理，最后 ZIP 打包下载
"""
import json
import shutil
import threading
import uuid
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .config import settings
from .prompt_generator import PromptGenerator
from .video_generator import VideoGenerator
from .post_processor import PostProcessor
from . import database as db


@dataclass
class BatchItem:
    item_id: str
    product_name: str
    selling_points: List[str]
    status: str = "pending"   # pending / processing / success / failed
    error: str = ""
    video_path: str = ""


@dataclass
class BatchJob:
    batch_id: str
    items: List[BatchItem]
    video_service: str = "seedance"
    add_subtitle: bool = False
    add_bgm: bool = False
    reference_image_path: str = ""
    status: str = "pending"   # pending / processing / done
    completed: int = 0
    failed: int = 0

    @property
    def total(self) -> int:
        return len(self.items)


# 全局批量任务存储
batch_jobs: Dict[str, BatchJob] = {}


def start_batch(
    items: List[Dict],
    video_service: str = "seedance",
    add_subtitle: bool = False,
    add_bgm: bool = False,
    reference_image_path: str = "",
) -> str:
    """
    创建并启动批量任务，返回 batch_id

    Args:
        items: [{"product_name": ..., "selling_points": [...]}, ...]
        video_service: seedance 或 creatok
        add_subtitle: 是否烧录字幕
        add_bgm: 是否混入 BGM
        reference_image_path: 参考图片路径（可选，所有产品共用）
    """
    batch_id = str(uuid.uuid4())
    batch_items = [
        BatchItem(
            item_id=str(uuid.uuid4()),
            product_name=item["product_name"].strip(),
            selling_points=[p.strip() for p in item["selling_points"] if p.strip()],
        )
        for item in items
        if item.get("product_name", "").strip()
    ]

    job = BatchJob(
        batch_id=batch_id,
        items=batch_items,
        video_service=video_service,
        add_subtitle=add_subtitle,
        add_bgm=add_bgm,
        reference_image_path=reference_image_path,
    )
    batch_jobs[batch_id] = job

    t = threading.Thread(target=_process_batch, args=(job,), daemon=True)
    t.start()
    return batch_id


def get_batch(batch_id: str) -> Optional[BatchJob]:
    """查询批量任务状态"""
    return batch_jobs.get(batch_id)


def _process_batch(job: BatchJob):
    """后台线程：逐个处理批量任务中的每条产品"""
    job.status = "processing"
    duration = 5 if job.video_service == "seedance" else 15

    pg = PromptGenerator()
    vg = VideoGenerator()
    pp = PostProcessor()

    for item in job.items:
        if item.status != "pending":
            continue

        item.status = "processing"
        output_dir = settings.output_dir / "batch" / job.batch_id / item.item_id
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Step 1: 生成视频脚本 + Prompt
            # 批量模式跳过 DALL-E（降低成本），直接用卖点作产品描述
            product_desc = "、".join(item.selling_points) if item.selling_points else item.product_name
            prompt_result = pg.generate_complete_prompt(
                product_name=item.product_name,
                product_description=product_desc,
                selling_points=item.selling_points,
                duration=duration,
            )
            script = prompt_result["script"]
            video_prompt = prompt_result["video_prompt"]

            # 保存脚本
            with open(output_dir / "script.json", "w", encoding="utf-8") as f:
                json.dump(script, f, ensure_ascii=False, indent=2)

            # Step 2: 生成视频
            safe_name = item.product_name.replace(" ", "_").replace("/", "_")
            raw_video = output_dir / f"{safe_name}_raw.mp4"
            final_video = output_dir / f"{safe_name}.mp4"

            ref_image = job.reference_image_path if job.reference_image_path and Path(job.reference_image_path).exists() else None
            video_result = vg.generate_video(
                prompt=video_prompt,
                output_path=str(raw_video),
                reference_image_path=ref_image,
                duration=duration,
                backend=job.video_service,
                wait=True,
            )

            if video_result["status"] != "success":
                raise Exception(video_result.get("error", "视频生成失败"))

            # Step 3: 后处理
            if job.add_subtitle or job.add_bgm:
                pp.process(
                    video_path=str(raw_video),
                    output_path=str(final_video),
                    script=script if job.add_subtitle else None,
                    add_subtitle=job.add_subtitle,
                    add_bgm=job.add_bgm,
                )
            else:
                shutil.copy2(str(raw_video), str(final_video))

            try:
                raw_video.unlink(missing_ok=True)
            except Exception:
                pass

            item.status = "success"
            item.video_path = str(final_video)
            job.completed += 1

            # 写入历史数据库
            db.create_job(item.item_id, item.product_name, job.video_service, job.add_subtitle, job.add_bgm)
            db.update_job(
                item.item_id,
                status="success",
                video_path=str(final_video),
                script=json.dumps(script, ensure_ascii=False),
                video_prompt=video_prompt,
            )

        except Exception as e:
            item.status = "failed"
            item.error = str(e)
            job.failed += 1
            print(f"❌ 批量任务 [{item.product_name}] 失败: {e}")

    job.status = "done"
    print(f"✅ 批量任务完成: {job.completed} 成功, {job.failed} 失败")


def create_zip(batch_id: str) -> Optional[str]:
    """
    将批量任务中所有成功的视频打包为 ZIP

    Returns:
        ZIP 文件路径，如果没有成功视频则返回 None
    """
    job = batch_jobs.get(batch_id)
    if not job:
        return None

    successful = [i for i in job.items if i.status == "success" and i.video_path]
    if not successful:
        return None

    zip_dir = settings.temp_dir / "batch_zips"
    zip_dir.mkdir(parents=True, exist_ok=True)
    zip_path = zip_dir / f"{batch_id}.zip"

    with zipfile.ZipFile(str(zip_path), "w", zipfile.ZIP_DEFLATED) as zf:
        for idx, item in enumerate(successful, 1):
            p = Path(item.video_path)
            if p.exists():
                safe = item.product_name.replace(" ", "_").replace("/", "_")
                # 避免重名，加序号前缀
                zf.write(str(p), f"{idx:02d}_{safe}.mp4")

    return str(zip_path)
