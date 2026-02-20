"""
视频生成模块 - MVP 版本
功能：
1. 集成 Creatok API 生成视频
2. （可选）集成 Sora API
"""
import time
import httpx
from pathlib import Path
from typing import Optional, Dict
from openai import OpenAI

from .config import settings


class VideoGenerator:
    """视频生成器"""

    def __init__(
        self,
        creatok_api_key: Optional[str] = None,
        openai_api_key: Optional[str] = None
    ):
        """
        初始化视频生成器

        Args:
            creatok_api_key: Creatok API Key
            openai_api_key: OpenAI API Key（用于 Sora）
        """
        self.creatok_api_key = creatok_api_key or settings.creatok_api_key
        self.creatok_api_url = settings.creatok_api_url
        self.openai_client = OpenAI(api_key=openai_api_key or settings.openai_api_key)

    def generate_with_creatok(
        self,
        prompt: str,
        reference_image_path: Optional[str] = None,
        duration: int = 15,
        aspect_ratio: str = "9:16"
    ) -> Dict:
        """
        使用 Creatok 生成视频

        Args:
            prompt: 视频生成提示词
            reference_image_path: 参考图片路径（可选）
            duration: 视频时长（秒）
            aspect_ratio: 宽高比（9:16 或 16:9）

        Returns:
            包含任务ID和状态的字典
        """
        print(f"🎬 使用 Creatok 生成视频...")
        print(f"时长: {duration}秒")
        print(f"宽高比: {aspect_ratio}")

        # Creatok API 调用（示例格式，需要根据实际 API 文档调整）
        headers = {
            "Authorization": f"Bearer {self.creatok_api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "prompt": prompt,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "model": "creatok-v1"  # 根据实际模型名称调整
        }

        # 如果有参考图片，上传并添加到 payload
        if reference_image_path:
            # TODO: 实现图片上传逻辑
            print(f"📎 使用参考图片: {reference_image_path}")
            pass

        try:
            # 发起生成请求
            response = httpx.post(
                f"{self.creatok_api_url}/videos/generate",
                headers=headers,
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()

            task_id = result.get("task_id") or result.get("id")
            print(f"✅ 任务创建成功: {task_id}")

            return {
                "status": "created",
                "task_id": task_id,
                "backend": "creatok"
            }

        except httpx.HTTPError as e:
            print(f"❌ Creatok API 调用失败: {e}")
            return {
                "status": "error",
                "error": str(e),
                "backend": "creatok"
            }

    def check_creatok_status(self, task_id: str) -> Dict:
        """
        检查 Creatok 视频生成状态

        Args:
            task_id: 任务 ID

        Returns:
            包含状态和视频 URL 的字典
        """
        print(f"🔍 检查任务状态: {task_id}")

        headers = {
            "Authorization": f"Bearer {self.creatok_api_key}"
        }

        try:
            response = httpx.get(
                f"{self.creatok_api_url}/videos/{task_id}",
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            result = response.json()

            status = result.get("status")
            video_url = result.get("video_url") or result.get("url")

            if status == "completed" and video_url:
                print(f"✅ 视频生成完成: {video_url}")
                return {
                    "status": "completed",
                    "video_url": video_url
                }
            elif status == "failed":
                error = result.get("error", "未知错误")
                print(f"❌ 生成失败: {error}")
                return {
                    "status": "failed",
                    "error": error
                }
            else:
                progress = result.get("progress", 0)
                print(f"⏳ 生成中... {progress}%")
                return {
                    "status": "processing",
                    "progress": progress
                }

        except httpx.HTTPError as e:
            print(f"❌ 状态查询失败: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

    def wait_for_completion(
        self,
        task_id: str,
        max_wait_time: int = 300,
        check_interval: int = 10
    ) -> Dict:
        """
        等待视频生成完成

        Args:
            task_id: 任务 ID
            max_wait_time: 最大等待时间（秒）
            check_interval: 检查间隔（秒）

        Returns:
            最终状态字典
        """
        print(f"⏰ 等待视频生成完成（最多 {max_wait_time} 秒）...")

        start_time = time.time()

        while True:
            elapsed = time.time() - start_time

            if elapsed > max_wait_time:
                print(f"⏱️  超时：已等待 {elapsed:.0f} 秒")
                return {
                    "status": "timeout",
                    "error": f"等待超过 {max_wait_time} 秒"
                }

            # 检查状态
            result = self.check_creatok_status(task_id)

            if result["status"] in ["completed", "failed", "error"]:
                return result

            # 等待后重试
            time.sleep(check_interval)

    def download_video(self, video_url: str, output_path: str):
        """
        下载生成的视频

        Args:
            video_url: 视频 URL
            output_path: 保存路径
        """
        print(f"⬇️  下载视频到: {output_path}")

        response = httpx.get(video_url, timeout=60.0)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(response.content)

        print(f"✅ 视频已保存 ({len(response.content) / 1024 / 1024:.2f} MB)")

    def generate_video(
        self,
        prompt: str,
        output_path: str,
        reference_image_path: Optional[str] = None,
        duration: int = 15,
        wait: bool = True
    ) -> Dict:
        """
        完整的视频生成流程

        Args:
            prompt: 视频生成提示词
            output_path: 输出视频路径
            reference_image_path: 参考图片路径
            duration: 视频时长
            wait: 是否等待生成完成

        Returns:
            生成结果字典
        """
        print("\n" + "="*50)
        print("开始生成视频")
        print("="*50)

        # 创建输出目录
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # 发起生成请求
        result = self.generate_with_creatok(
            prompt=prompt,
            reference_image_path=reference_image_path,
            duration=duration
        )

        if result["status"] != "created":
            return result

        task_id = result["task_id"]

        # 如果不等待，直接返回任务 ID
        if not wait:
            return {
                "status": "created",
                "task_id": task_id,
                "message": "视频生成中，请稍后查询"
            }

        # 等待生成完成
        final_result = self.wait_for_completion(task_id)

        if final_result["status"] != "completed":
            return final_result

        # 下载视频
        video_url = final_result["video_url"]
        self.download_video(video_url, output_path)

        return {
            "status": "success",
            "output_path": output_path,
            "video_url": video_url
        }


# 测试代码
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使用方法: python video_generator.py '<视频 prompt>'")
        sys.exit(1)

    prompt = sys.argv[1]
    output_path = "./output/test_video.mp4"

    generator = VideoGenerator()
    result = generator.generate_video(
        prompt=prompt,
        output_path=output_path,
        duration=15
    )

    print("\n" + "="*50)
    print("生成完成！")
    print("="*50)
    print(f"结果: {result}")
