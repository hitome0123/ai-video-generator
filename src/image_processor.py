"""
图片处理模块 - MVP 版本
功能：
1. ChatGPT Vision 抠图
2. DALL·E 3 扩图（补背景）
"""
import os
import base64
from pathlib import Path
from typing import Optional
from openai import OpenAI
from PIL import Image
import httpx

from .config import settings


class ImageProcessor:
    """图片处理器"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化图片处理器

        Args:
            api_key: OpenAI API Key，如果不提供则从环境变量读取
        """
        self.client = OpenAI(api_key=api_key or settings.openai_api_key)

    def encode_image(self, image_path: str) -> str:
        """
        将图片编码为 base64

        Args:
            image_path: 图片路径

        Returns:
            base64 编码的图片
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def remove_background(self, image_path: str, output_path: str) -> dict:
        """
        使用 ChatGPT Vision 分析产品并生成抠图描述

        Args:
            image_path: 原始图片路径
            output_path: 输出路径

        Returns:
            包含产品描述和建议的字典
        """
        print(f"📸 分析产品图片: {image_path}")

        # 编码图片
        base64_image = self.encode_image(image_path)

        # 调用 GPT-4V 分析产品
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """请分析这张产品图片，并提供：
1. 产品名称和类别
2. 详细的外观描述（颜色、形状、材质、特征）
3. 建议的白底图描述（用于后续 AI 生成）

请用 JSON 格式返回，包含字段：
- product_name: 产品名称
- category: 类别
- description: 详细描述
- white_bg_prompt: 白底图生成提示词（英文）
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )

        # 提取分析结果
        result_text = response.choices[0].message.content
        print(f"✅ 产品分析完成")
        print(f"分析结果: {result_text[:200]}...")

        # 简单解析（生产环境应该用更严格的 JSON 解析）
        import json
        try:
            result = json.loads(result_text)
        except:
            # 如果不是标准 JSON，返回原始文本
            result = {
                "product_name": "未知产品",
                "description": result_text,
                "white_bg_prompt": result_text
            }

        return result

    def expand_image(
        self,
        image_path: str,
        product_description: str,
        output_path: str,
        size: str = "1024x1024"
    ) -> str:
        """
        使用 DALL·E 3 生成白底产品图（扩图）

        Args:
            image_path: 原始图片路径
            product_description: 产品描述（从 Vision 分析获得）
            output_path: 输出路径
            size: 图片尺寸（1024x1024 或 1024x1792）

        Returns:
            生成的图片 URL
        """
        print(f"🎨 使用 DALL·E 3 生成白底图...")
        print(f"产品描述: {product_description[:100]}...")

        # 构建 prompt
        prompt = f"""A professional product photo on a pure white background:
{product_description}

Requirements:
- Clean white background (#FFFFFF)
- Product centered
- Professional lighting
- High quality, e-commerce style
- No text, no watermarks
"""

        # 调用 DALL·E 3 生成图片
        response = self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="hd",
            n=1
        )

        # 获取生成的图片 URL
        image_url = response.data[0].url
        print(f"✅ 图片生成成功: {image_url}")

        # 下载图片
        self._download_image(image_url, output_path)

        return image_url

    def _download_image(self, url: str, output_path: str):
        """
        下载图片到本地

        Args:
            url: 图片 URL
            output_path: 保存路径
        """
        print(f"⬇️  下载图片到: {output_path}")

        response = httpx.get(url)
        response.raise_for_status()

        with open(output_path, "wb") as f:
            f.write(response.content)

        print(f"✅ 图片已保存")

    def process_image(
        self,
        input_path: str,
        output_dir: Optional[str] = None
    ) -> dict:
        """
        完整的图片处理流程

        Args:
            input_path: 输入图片路径
            output_dir: 输出目录（可选）

        Returns:
            处理结果字典
        """
        # 设置输出目录
        if output_dir is None:
            output_dir = settings.temp_dir / "processed"
        else:
            output_dir = Path(output_dir)

        output_dir.mkdir(parents=True, exist_ok=True)

        # 步骤 1: 分析产品
        print("\n" + "="*50)
        print("步骤 1: 分析产品图片")
        print("="*50)

        analysis = self.remove_background(input_path, str(output_dir / "temp.png"))

        # 步骤 2: 生成白底图
        print("\n" + "="*50)
        print("步骤 2: 生成白底产品图")
        print("="*50)

        white_bg_prompt = analysis.get("white_bg_prompt", analysis.get("description", ""))
        output_path = output_dir / "white_bg.png"

        image_url = self.expand_image(
            input_path,
            white_bg_prompt,
            str(output_path),
            size="1024x1792"  # 竖版，适合 TikTok
        )

        return {
            "status": "success",
            "analysis": analysis,
            "output_path": str(output_path),
            "image_url": image_url
        }


# 测试代码
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使用方法: python image_processor.py <图片路径>")
        sys.exit(1)

    image_path = sys.argv[1]

    processor = ImageProcessor()
    result = processor.process_image(image_path)

    print("\n" + "="*50)
    print("处理完成！")
    print("="*50)
    print(f"输出路径: {result['output_path']}")
    print(f"产品信息: {result['analysis']}")
