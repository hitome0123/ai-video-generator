"""
视频生成模块
支持两种视频生成服务：
1. 豆包 Seedance（火山引擎 ARK，推荐）- 国内直连，成本低，支持图生视频
2. Creatok - 国际服务，15秒视频
"""
import time
import base64
import httpx
from pathlib import Path
from typing import Optional, Dict

from .config import settings


class VideoGenerator:
    """视频生成器，支持 Seedance 和 Creatok 两种后端"""

    def __init__(
        self,
        ark_api_key: Optional[str] = None,
        creatok_api_key: Optional[str] = None,
    ):
        self.ark_api_key = ark_api_key or settings.ark_api_key
        self.creatok_api_key = creatok_api_key or settings.creatok_api_key
        self.creatok_api_url = settings.creatok_api_url
        self.seedance_api_url = settings.seedance_api_url
        self.seedance_model_id = settings.seedance_model_id

    # ────────────────────────────────────────────────────────────
    # 工具方法
    # ────────────────────────────────────────────────────────────

    def _encode_image_base64(self, image_path: str) -> str:
        """将本地图片编码为 base64 data URL"""
        suffix = Path(image_path).suffix.lower()
        mime = "image/png" if suffix == ".png" else "image/jpeg"
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime};base64,{data}"

    def download_video(self, video_url: str, output_path: str):
        """下载视频到本地"""
        print(f"⬇️  下载视频: {output_path}")
        with httpx.Client(timeout=120.0, follow_redirects=True) as client:
            response = client.get(video_url)
            response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        size_mb = len(response.content) / 1024 / 1024
        print(f"✅ 视频已保存 ({size_mb:.2f} MB)")

    # ────────────────────────────────────────────────────────────
    # 豆包 Seedance（火山引擎 ARK）
    # ────────────────────────────────────────────────────────────

    def generate_with_seedance(
        self,
        prompt: str,
        reference_image_path: Optional[str] = None,
        duration: int = 5,
        aspect_ratio: str = "9:16",
        resolution: str = "720p",
    ) -> Dict:
        """
        使用豆包 Seedance 生成视频（图生视频）

        Args:
            prompt: 视频描述文本
            reference_image_path: 参考图片路径（白底产品图，作为首帧）
            duration: 视频时长（秒），Lite 模型支持 5-10 秒
            aspect_ratio: 宽高比，9:16 为 TikTok 竖版
            resolution: 分辨率，480p / 720p

        Returns:
            包含 task_id 的字典
        """
        print(f"🎬 使用豆包 Seedance 生成视频...")
        print(f"模型: {self.seedance_model_id}")
        print(f"时长: {duration}秒 | 比例: {aspect_ratio} | 分辨率: {resolution}")

        # 在 prompt 末尾追加控制参数
        text_with_params = (
            f"{prompt} "
            f"--resolution {resolution} "
            f"--duration {duration} "
            f"--ratio {aspect_ratio}"
        )

        # 构建请求内容
        content = [{"type": "text", "text": text_with_params}]

        # 如果有参考图，编码为 base64 追加到 content
        if reference_image_path and Path(reference_image_path).exists():
            print(f"📎 使用参考图片: {reference_image_path}")
            image_data_url = self._encode_image_base64(reference_image_path)
            content.append({
                "type": "image_url",
                "image_url": {"url": image_data_url}
            })

        headers = {
            "Authorization": f"Bearer {self.ark_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.seedance_model_id,
            "content": content,
        }

        try:
            response = httpx.post(
                f"{self.seedance_api_url}/contents/generations/tasks",
                headers=headers,
                json=payload,
                timeout=30.0,
            )
            response.raise_for_status()
            result = response.json()
            task_id = result.get("task_id") or result.get("id")
            print(f"✅ Seedance 任务创建成功: {task_id}")
            return {"status": "created", "task_id": task_id, "backend": "seedance"}

        except httpx.HTTPError as e:
            print(f"❌ Seedance API 调用失败: {e}")
            return {"status": "error", "error": str(e), "backend": "seedance"}

    def check_seedance_status(self, task_id: str) -> Dict:
        """查询 Seedance 任务状态"""
        headers = {"Authorization": f"Bearer {self.ark_api_key}"}
        try:
            response = httpx.get(
                f"{self.seedance_api_url}/contents/generations/tasks/{task_id}",
                headers=headers,
                timeout=15.0,
            )
            response.raise_for_status()
            result = response.json()
            status = result.get("status")

            if status == "done":
                video_url = result.get("video_url")
                print(f"✅ Seedance 生成完成: {video_url}")
                return {"status": "completed", "video_url": video_url}
            elif status == "failed":
                error = result.get("error", "未知错误")
                print(f"❌ Seedance 生成失败: {error}")
                return {"status": "failed", "error": error}
            else:
                progress = result.get("progress", 0)
                print(f"⏳ Seedance 生成中... {progress}%")
                return {"status": "processing", "progress": progress}

        except httpx.HTTPError as e:
            print(f"❌ Seedance 状态查询失败: {e}")
            return {"status": "error", "error": str(e)}

    # ────────────────────────────────────────────────────────────
    # Creatok
    # ────────────────────────────────────────────────────────────

    def generate_with_creatok(
        self,
        prompt: str,
        reference_image_path: Optional[str] = None,
        duration: int = 15,
        aspect_ratio: str = "9:16",
    ) -> Dict:
        """使用 Creatok 生成视频"""
        print(f"🎬 使用 Creatok 生成视频...")
        print(f"时长: {duration}秒 | 比例: {aspect_ratio}")

        headers = {
            "Authorization": f"Bearer {self.creatok_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "model": "creatok-v1",
        }

        # 参考图上传（base64）
        if reference_image_path and Path(reference_image_path).exists():
            print(f"📎 使用参考图片: {reference_image_path}")
            image_data_url = self._encode_image_base64(reference_image_path)
            payload["reference_image"] = image_data_url

        try:
            response = httpx.post(
                f"{self.creatok_api_url}/videos/generate",
                headers=headers,
                json=payload,
                timeout=30.0,
            )
            response.raise_for_status()
            result = response.json()
            task_id = result.get("task_id") or result.get("id")
            print(f"✅ Creatok 任务创建成功: {task_id}")
            return {"status": "created", "task_id": task_id, "backend": "creatok"}

        except httpx.HTTPError as e:
            print(f"❌ Creatok API 调用失败: {e}")
            return {"status": "error", "error": str(e), "backend": "creatok"}

    def check_creatok_status(self, task_id: str) -> Dict:
        """查询 Creatok 任务状态"""
        headers = {"Authorization": f"Bearer {self.creatok_api_key}"}
        try:
            response = httpx.get(
                f"{self.creatok_api_url}/videos/{task_id}",
                headers=headers,
                timeout=10.0,
            )
            response.raise_for_status()
            result = response.json()
            status = result.get("status")

            if status == "completed":
                video_url = result.get("video_url") or result.get("url")
                print(f"✅ Creatok 生成完成: {video_url}")
                return {"status": "completed", "video_url": video_url}
            elif status == "failed":
                error = result.get("error", "未知错误")
                print(f"❌ Creatok 生成失败: {error}")
                return {"status": "failed", "error": error}
            else:
                progress = result.get("progress", 0)
                print(f"⏳ Creatok 生成中... {progress}%")
                return {"status": "processing", "progress": progress}

        except httpx.HTTPError as e:
            print(f"❌ Creatok 状态查询失败: {e}")
            return {"status": "error", "error": str(e)}

    # ────────────────────────────────────────────────────────────
    # 通用：等待完成 + 完整流程
    # ────────────────────────────────────────────────────────────

    def wait_for_completion(
        self,
        task_id: str,
        backend: str = "seedance",
        max_wait_time: int = 300,
        check_interval: int = 8,
    ) -> Dict:
        """轮询等待视频生成完成"""
        print(f"⏰ 等待生成完成（{backend}，最多 {max_wait_time} 秒）...")
        start_time = time.time()

        while True:
            elapsed = time.time() - start_time
            if elapsed > max_wait_time:
                return {
                    "status": "timeout",
                    "error": f"等待超过 {max_wait_time} 秒"
                }

            if backend == "seedance":
                result = self.check_seedance_status(task_id)
            else:
                result = self.check_creatok_status(task_id)

            if result["status"] in ("completed", "failed", "error"):
                return result

            time.sleep(check_interval)

    def generate_video(
        self,
        prompt: str,
        output_path: str,
        reference_image_path: Optional[str] = None,
        duration: int = 5,
        backend: str = "seedance",
        wait: bool = True,
    ) -> Dict:
        """
        完整视频生成流程（统一入口）

        Args:
            prompt: 视频描述文本
            output_path: 输出 MP4 路径
            reference_image_path: 参考图片（白底产品图）
            duration: 视频时长（Seedance 建议 5 秒，Creatok 建议 15 秒）
            backend: 'seedance' 或 'creatok'
            wait: 是否等待生成完成
        """
        print(f"\n{'='*50}")
        print(f"开始生成视频 [{backend}]")
        print(f"{'='*50}")

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # 根据 backend 调用对应生成器
        if backend == "seedance":
            result = self.generate_with_seedance(
                prompt=prompt,
                reference_image_path=reference_image_path,
                duration=duration,
            )
        else:
            result = self.generate_with_creatok(
                prompt=prompt,
                reference_image_path=reference_image_path,
                duration=duration,
            )

        if result["status"] != "created":
            return result

        task_id = result["task_id"]

        if not wait:
            return {"status": "created", "task_id": task_id, "backend": backend}

        # 轮询等待
        final_result = self.wait_for_completion(task_id, backend=backend)

        if final_result["status"] != "completed":
            return final_result

        # 下载视频
        self.download_video(final_result["video_url"], output_path)

        return {
            "status": "success",
            "output_path": output_path,
            "video_url": final_result["video_url"],
            "backend": backend,
        }


# ── 测试入口 ──────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使用方法: python video_generator.py '<视频 prompt>' [seedance|creatok]")
        sys.exit(1)

    prompt = sys.argv[1]
    backend = sys.argv[2] if len(sys.argv) > 2 else "seedance"
    duration = 5 if backend == "seedance" else 15

    generator = VideoGenerator()
    result = generator.generate_video(
        prompt=prompt,
        output_path=f"./output/test_{backend}.mp4",
        duration=duration,
        backend=backend,
    )

    print(f"\n{'='*50}\n生成结果: {result}")
