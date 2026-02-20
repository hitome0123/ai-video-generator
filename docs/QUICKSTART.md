# AI Video Generator - MVP 快速上手指南

**版本**: MVP 1.0
**更新时间**: 2026-02-20

---

## 📦 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/YOUR_USERNAME/ai-video-generator.git
cd ai-video-generator
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

**依赖包**:
- `openai` - OpenAI API 客户端（GPT-4V, DALL·E 3）
- `fastapi` - Web 框架（未来用）
- `Pillow` - 图片处理
- `httpx` - HTTP 客户端

### 3. 配置 API Key

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API Key：

```env
# OpenAI API Key（必需）
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Creatok API Key（必需）
CREATOK_API_KEY=your-creatok-api-key-here

# 可选配置
OUTPUT_DIR=./output
TEMP_DIR=./temp
```

---

## 🎯 使用方法

### 方式 1: 命令行工具（推荐）

```bash
python main.py <图片路径> <产品名称> <卖点1> <卖点2> ...
```

**示例**:

```bash
# 智能手表示例
python main.py \
    examples/smartwatch.jpg \
    "智能手表V8 Pro" \
    "30天超长续航" \
    "50米防水" \
    "24小时心率监测" \
    "100+运动模式"

# 充电器示例
python main.py \
    examples/charger.jpg \
    "20W快充充电器" \
    "PD快充协议" \
    "双USB接口" \
    "折叠插头" \
    "全球通用"
```

### 方式 2: Python 脚本

创建 `my_video.py`:

```python
from main import generate_video_from_image

result = generate_video_from_image(
    image_path="my_product.jpg",
    product_name="我的产品",
    selling_points=[
        "卖点1",
        "卖点2",
        "卖点3"
    ],
    duration=15  # 视频时长（秒）
)

print(f"视频已生成: {result['video_result']['output_path']}")
```

运行:

```bash
python my_video.py
```

---

## 📂 输出结构

运行后会在 `output/` 目录生成以下文件：

```
output/
└── 产品名称/
    ├── processed/              # 图片处理结果
    │   └── white_bg.png        # DALL·E 生成的白底图
    ├── script.json             # 视频脚本（JSON 格式）
    ├── video_prompt.txt        # 视频生成 Prompt
    └── 产品名称.mp4            # 最终视频
```

**文件说明**:

1. **white_bg.png** - AI 扩图后的白底产品图（1024x1792）
2. **script.json** - 包含 hook、分镜、CTA 的完整脚本
3. **video_prompt.txt** - 优化后的视频生成 Prompt
4. **产品名称.mp4** - 生成的 TikTok 视频（9:16 竖版）

---

## 🔧 模块化使用

### 1. 仅处理图片

```python
from src.image_processor import ImageProcessor

processor = ImageProcessor()
result = processor.process_image("product.jpg")

print(f"白底图: {result['output_path']}")
print(f"产品分析: {result['analysis']}")
```

### 2. 仅生成 Prompt

```python
from src.prompt_generator import PromptGenerator

generator = PromptGenerator()
result = generator.generate_complete_prompt(
    product_name="智能手表",
    product_description="A modern smartwatch with AMOLED display",
    selling_points=["30天续航", "防水"],
    duration=15
)

print(f"脚本: {result['script']}")
print(f"Prompt: {result['video_prompt']}")
```

### 3. 仅生成视频

```python
from src.video_generator import VideoGenerator

generator = VideoGenerator()
result = generator.generate_video(
    prompt="Your video prompt here",
    output_path="output/video.mp4",
    duration=15
)

print(f"视频: {result['output_path']}")
```

---

## 💰 成本估算

**单个视频成本（15秒）**:

| 步骤 | API | 价格 |
|------|-----|------|
| 图片分析 | GPT-4V | ~$0.01 |
| 白底图生成 | DALL·E 3 (HD) | $0.08 |
| 脚本生成 | GPT-4 | ~$0.01 |
| Prompt 优化 | GPT-4 | ~$0.01 |
| 视频生成 | Creatok | ~$0.20 |
| **总计** | | **~$0.31** |

**批量生产成本**:

| 数量 | 成本 |
|------|------|
| 10 个视频 | $3.1 |
| 100 个视频 | $31 |
| 1000 个视频 | $310 |

---

## ⚠️ 常见问题

### Q1: DALL·E 3 生成的图片不理想？

**答**: 可以调整 `image_processor.py` 中的 Prompt 模板：

```python
# 在 expand_image() 函数中修改
prompt = f"""A professional product photo on a pure white background:
{product_description}

Additional requirements:
- 添加你的自定义要求
"""
```

### Q2: 视频生成失败？

**答**: 检查以下几点：
1. Creatok API Key 是否正确
2. API 配额是否用完
3. Prompt 是否包含敏感内容

### Q3: 如何自定义视频时长？

**答**: 在命令行或 Python 脚本中指定 `duration` 参数：

```bash
# 不支持命令行参数，需要修改代码
# 在 main.py 中修改:
generate_video_from_image(..., duration=30)
```

### Q4: 如何批量处理多个产品？

**答**: 创建一个脚本循环处理：

```python
products = [
    {"image": "p1.jpg", "name": "产品1", "points": ["卖点1", "卖点2"]},
    {"image": "p2.jpg", "name": "产品2", "points": ["卖点1", "卖点2"]},
]

for p in products:
    generate_video_from_image(
        image_path=p["image"],
        product_name=p["name"],
        selling_points=p["points"]
    )
```

---

## 🐛 调试模式

### 开启详细日志

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 测试单个模块

```bash
# 测试图片处理
python -m src.image_processor smartwatch.jpg

# 测试 Prompt 生成
python -m src.prompt_generator
```

---

## 🔗 下一步

1. **测试生成的视频**: 检查视频质量、卖点展示是否清晰
2. **调整 Prompt**: 根据生成效果优化提示词模板
3. **批量处理**: 准备多个产品图片批量生成
4. **集成上传**: 配合 `tiktok-video-upload` 自动发布

---

## 📞 技术支持

遇到问题？

- 查看 [CLAUDE.md](../CLAUDE.md) 了解项目架构
- 查看 [PRD.md](PRD.md) 了解完整功能规划
- 提交 Issue: https://github.com/YOUR_USERNAME/ai-video-generator/issues

---

**Happy Video Creating! 🎬**
