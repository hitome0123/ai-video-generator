"""
Prompt 生成模块 - MVP 版本
功能：
1. 根据产品信息和卖点生成视频脚本
2. 生成 Sora/Creatok 视频提示词
"""
from typing import List, Optional, Dict
from openai import OpenAI

from .config import settings
from .utils import parse_json_response


class PromptGenerator:
    """视频 Prompt 生成器"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 Prompt 生成器

        Args:
            api_key: OpenAI API Key
        """
        self.client = OpenAI(api_key=api_key or settings.openai_api_key)

    def generate_video_script(
        self,
        product_name: str,
        product_description: str,
        selling_points: List[str],
        duration: int = 15
    ) -> dict:
        """
        生成视频脚本

        Args:
            product_name: 产品名称
            product_description: 产品描述
            selling_points: 卖点列表
            duration: 视频时长（秒）

        Returns:
            包含脚本和分镜的字典
        """
        print(f"📝 生成视频脚本...")
        print(f"产品: {product_name}")
        print(f"卖点: {', '.join(selling_points)}")

        # 构建 prompt
        prompt = f"""为这个产品生成一个 {duration} 秒的 TikTok 短视频脚本：

产品名称: {product_name}
产品描述: {product_description}

核心卖点:
{chr(10).join(f'- {point}' for point in selling_points)}

要求:
1. 遵循 TikTok 爆款视频结构：痛点开头(3s) + 卖点展示 + 引导下单
2. 每个镜头 3-5 秒
3. 简洁有力，适合年轻用户
4. 突出产品的视觉冲击力

请用 JSON 格式返回，包含:
- hook: 痛点/吸引开头（1句话）
- scenes: 分镜列表，每个包含 duration(秒)、description(镜头描述)、text(屏幕文字)
- cta: 行动号召（1句话）

示例格式:
{{
  "hook": "还在为XX烦恼？",
  "scenes": [
    {{"duration": 3, "description": "产品特写镜头", "text": "核心卖点"}},
    ...
  ],
  "cta": "立即下单！"
}}
"""

        # 调用 GPT-4 生成脚本
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的 TikTok 短视频脚本编剧，擅长制作爆款带货视频。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # 提取脚本
        script_text = response.choices[0].message.content

        print(f"✅ 脚本生成完成")
        print(f"预览: {script_text[:200]}...")

        script = parse_json_response(script_text)
        if not isinstance(script, dict):
            script = {
                "hook": "产品介绍",
                "scenes": [{"duration": duration, "description": script_text, "text": ""}],
                "cta": "立即购买",
            }

        return script

    def generate_video_prompt(
        self,
        product_description: str,
        script: dict,
        reference_image_path: Optional[str] = None
    ) -> str:
        """
        生成 AI 视频生成工具的 Prompt（Sora/Creatok）

        Args:
            product_description: 产品外观描述
            script: 视频脚本（从 generate_video_script 获得）
            reference_image_path: 参考图片路径（可选）

        Returns:
            完整的视频生成 Prompt
        """
        print(f"🎬 生成视频 Prompt...")

        # 提取场景描述
        scenes_description = "\n".join([
            f"Scene {i+1} ({scene['duration']}s): {scene['description']}"
            for i, scene in enumerate(script.get("scenes", []))
        ])

        # 构建完整 Prompt
        prompt_template = f"""Create a professional TikTok product video (9:16 vertical format):

PRODUCT:
{product_description}

VIDEO STRUCTURE:
Hook: {script.get('hook', 'Product showcase')}

{scenes_description}

Call-to-Action: {script.get('cta', 'Buy now!')}

STYLE REQUIREMENTS:
- Vertical video (9:16 aspect ratio)
- Clean, modern aesthetic
- Smooth transitions between scenes
- Professional lighting
- Focus on product features
- Engaging, dynamic camera movements
- E-commerce style, suitable for TikTok

IMPORTANT:
- Keep the product visually consistent throughout
- Highlight key selling points
- Maintain high visual quality
- Suitable for social media marketing
"""

        # 使用 GPT-4 优化 Prompt
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个专业的 AI 视频生成提示词专家，擅长为 Sora、Creatok 等工具编写高质量的视频生成 Prompt。"
                },
                {
                    "role": "user",
                    "content": f"""请优化这个视频生成 Prompt，使其更适合 AI 视频生成工具（Sora/Creatok）：

{prompt_template}

要求:
1. 保持产品外观描述准确
2. 场景描述要具体、可视化
3. 添加适当的镜头运动、光线描述
4. 确保符合 9:16 竖版格式
5. 总长度控制在 500 tokens 以内

直接返回优化后的 Prompt，不要额外说明。
"""
                }
            ],
            temperature=0.5,
            max_tokens=800
        )

        optimized_prompt = response.choices[0].message.content

        print(f"✅ 视频 Prompt 生成完成")
        print(f"长度: {len(optimized_prompt)} 字符")

        return optimized_prompt

    def generate_complete_prompt(
        self,
        product_name: str,
        product_description: str,
        selling_points: List[str],
        duration: int = 15
    ) -> Dict[str, any]:
        """
        一站式生成完整的视频 Prompt

        Args:
            product_name: 产品名称
            product_description: 产品描述
            selling_points: 卖点列表
            duration: 视频时长

        Returns:
            包含脚本和 Prompt 的字典
        """
        # 生成脚本
        script = self.generate_video_script(
            product_name,
            product_description,
            selling_points,
            duration
        )

        # 生成视频 Prompt
        video_prompt = self.generate_video_prompt(
            product_description,
            script
        )

        return {
            "product_name": product_name,
            "script": script,
            "video_prompt": video_prompt,
            "duration": duration
        }


# 测试代码
if __name__ == "__main__":
    generator = PromptGenerator()

    # 测试数据
    result = generator.generate_complete_prompt(
        product_name="智能手表 V8 Pro",
        product_description="A modern smartwatch with black metal frame, round AMOLED display, and silicon strap",
        selling_points=[
            "30天超长续航",
            "50米防水",
            "24小时心率监测",
            "100+运动模式"
        ],
        duration=15
    )

    print("\n" + "="*50)
    print("生成完成！")
    print("="*50)
    print(f"\n脚本:\n{result['script']}")
    print(f"\n视频 Prompt:\n{result['video_prompt']}")
