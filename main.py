"""
AI Video Generator - MVP 主程序
一站式生成 TikTok 产品视频
"""
import sys
from pathlib import Path
from src.image_processor import ImageProcessor
from src.prompt_generator import PromptGenerator
from src.video_generator import VideoGenerator
from src.config import settings


def generate_video_from_image(
    image_path: str,
    product_name: str,
    selling_points: list,
    output_dir: str = None,
    duration: int = 15
):
    """
    从产品图片生成 TikTok 视频的完整流程

    Args:
        image_path: 产品图片路径
        product_name: 产品名称
        selling_points: 卖点列表
        output_dir: 输出目录
        duration: 视频时长（秒）
    """
    if output_dir is None:
        output_dir = settings.output_dir / Path(image_path).stem

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "🎬 "*25)
    print("AI TikTok Video Generator - MVP")
    print("🎬 "*25 + "\n")

    # ============================================
    # 步骤 1: 图片处理（抠图 + 扩图）
    # ============================================
    print("\n📸 步骤 1/3: 图片处理")
    print("-" * 50)

    image_processor = ImageProcessor()
    image_result = image_processor.process_image(
        input_path=image_path,
        output_dir=str(output_dir / "processed")
    )

    product_description = image_result["analysis"].get(
        "white_bg_prompt",
        image_result["analysis"].get("description", "")
    )
    processed_image_path = image_result["output_path"]

    print(f"✅ 图片处理完成: {processed_image_path}")

    # ============================================
    # 步骤 2: 生成视频 Prompt
    # ============================================
    print("\n📝 步骤 2/3: 生成视频脚本和 Prompt")
    print("-" * 50)

    prompt_generator = PromptGenerator()
    prompt_result = prompt_generator.generate_complete_prompt(
        product_name=product_name,
        product_description=product_description,
        selling_points=selling_points,
        duration=duration
    )

    video_prompt = prompt_result["video_prompt"]
    script = prompt_result["script"]

    # 保存 Prompt 和脚本
    with open(output_dir / "script.json", "w", encoding="utf-8") as f:
        import json
        json.dump(script, f, ensure_ascii=False, indent=2)

    with open(output_dir / "video_prompt.txt", "w", encoding="utf-8") as f:
        f.write(video_prompt)

    print(f"✅ 脚本已保存: {output_dir / 'script.json'}")
    print(f"✅ Prompt 已保存: {output_dir / 'video_prompt.txt'}")

    # ============================================
    # 步骤 3: 生成视频
    # ============================================
    print("\n🎬 步骤 3/3: AI 视频生成")
    print("-" * 50)

    video_output_path = output_dir / f"{product_name.replace(' ', '_')}.mp4"

    video_generator = VideoGenerator()
    video_result = video_generator.generate_video(
        prompt=video_prompt,
        output_path=str(video_output_path),
        reference_image_path=processed_image_path,
        duration=duration,
        wait=True
    )

    # ============================================
    # 完成
    # ============================================
    print("\n" + "="*50)
    print("✅ 生成完成！")
    print("="*50)

    print(f"\n输出目录: {output_dir}")
    print(f"  - 处理后的图片: {processed_image_path}")
    print(f"  - 视频脚本: {output_dir / 'script.json'}")
    print(f"  - 视频 Prompt: {output_dir / 'video_prompt.txt'}")

    if video_result["status"] == "success":
        print(f"  - 生成的视频: {video_result['output_path']}")
    else:
        print(f"  - 视频生成状态: {video_result['status']}")
        if "error" in video_result:
            print(f"  - 错误信息: {video_result['error']}")

    return {
        "image_result": image_result,
        "prompt_result": prompt_result,
        "video_result": video_result,
        "output_dir": str(output_dir)
    }


def main():
    """命令行入口"""
    if len(sys.argv) < 4:
        print("""
使用方法:
    python main.py <图片路径> <产品名称> <卖点1> [卖点2] [卖点3] ...

示例:
    python main.py smartwatch.jpg "智能手表V8 Pro" "30天续航" "50米防水" "心率监测"
        """)
        sys.exit(1)

    image_path = sys.argv[1]
    product_name = sys.argv[2]
    selling_points = sys.argv[3:]

    result = generate_video_from_image(
        image_path=image_path,
        product_name=product_name,
        selling_points=selling_points
    )

    return result


if __name__ == "__main__":
    main()
