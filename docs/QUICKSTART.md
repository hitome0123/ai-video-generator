# AI Video Generator - 快速上手指南

**版本**: 1.0 正式版
**更新时间**: 2026-02-21

---

## 📦 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/hitome0123/ai-video-generator.git
cd ai-video-generator
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

**主要依赖**:
- `openai` - OpenAI API 客户端（GPT-4o、DALL·E 3）
- `fastapi` / `uvicorn` - Web 框架及服务器
- `Pillow` / `opencv-python` - 图片处理
- `httpx` / `requests` - HTTP 客户端
- `aiofiles` - 异步文件操作

### 3. 配置 API Key

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的 API Key：

```env
# OpenAI API Key（必需）
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 视频生成（二选一，推荐 Seedance）
ARK_API_KEY=your-ark-api-key-here        # 豆包 Seedance（火山引擎）
CREATOK_API_KEY=your-creatok-api-key-here  # Creatok（备选）

# 可选配置
OUTPUT_DIR=./output
TEMP_DIR=./temp
```

**API Key 获取地址**:

| Key | 申请地址 |
|-----|---------|
| OPENAI_API_KEY | https://platform.openai.com/api-keys |
| ARK_API_KEY | https://console.volcengine.com → 火山方舟 → API Key 管理 |
| CREATOK_API_KEY | https://www.creatok.ai |

---

## 🎯 使用方法

### 方式 1: Web 界面（推荐）

```bash
python run.py
```

浏览器打开 **http://localhost:8000**，按页面引导操作：

1. 上传产品图片（拖拽或点击）
2. 填写产品名称和卖点
3. 选择视频服务（Seedance 推荐 / Creatok 备选）
4. 可选开启字幕烧录 / BGM 混音
5. 点击「生成视频」，等待完成后一键下载

**Web 界面功能页面**:

| 页面 | 地址 | 说明 |
|------|------|------|
| 主页 | / | 上传图片 + 生成视频 |
| 历史记录 | /history.html | 查看 / 下载历史任务 |
| 批量处理 | /batch.html | CSV 导入批量生成 |
| 设置 | /settings.html | 管理 API Key 及参数 |
| 广告系列 | /campaigns.html | 创建和管理广告系列 |
| 数据分析 | /analytics.html | ROAS、花费趋势看板 |
| 优化分析 | /optimization.html | AI 优化建议队列 |

### 方式 2: 命令行工具

```bash
python main.py <图片路径> <产品名称> <卖点1> <卖点2> ...
```

**示例**:

```bash
# 智能手表示例
python main.py \
    smartwatch.jpg \
    "智能手表V8 Pro" \
    "30天超长续航" \
    "50米防水" \
    "24小时心率监测" \
    "100+运动模式"
```

---

## 📂 输出结构

```
output/<job_id>/
├── processed/
│   └── white_bg.png        # DALL·E 3 生成的白底图（1024×1792）
├── script.json             # 视频脚本（hook / scenes / cta）
├── video_prompt.txt        # 优化后的视频生成 Prompt
└── <产品名称>.mp4          # 成品视频（含字幕 / BGM，9:16 竖版）
```

历史任务保存在 `data/jobs.db`，重启服务后可在历史记录页面重新下载。

---

## 💰 成本估算

### Seedance 方案（推荐）

| 步骤 | API | 费用 |
|------|-----|------|
| 图片分析 | GPT-4o Vision | ~$0.01 |
| 白底图生成 | DALL·E 3 | $0.08 |
| 脚本生成 | GPT-4o | ~$0.01 |
| Prompt 优化 | GPT-4o | ~$0.01 |
| 视频生成（5 秒）| 豆包 Seedance | ~¥0.9 |
| **合计** | | **~¥1.5 / 视频** |

### Creatok 方案（备选）

| 步骤 | API | 费用 |
|------|-----|------|
| 图片分析 + 脚本 | GPT-4o | ~$0.11 |
| 视频生成（15 秒）| Creatok | ~¥2.2 |
| **合计** | | **~¥3 / 视频** |

---

## ⚠️ 常见问题

### Q1: DALL·E 3 生成的图片不理想？

调整 `src/image_processor.py` 中 `expand_image()` 函数里的 Prompt 模板：

```python
prompt = f"""A professional product photo on a pure white background:
{product_description}

Additional requirements:
- 添加你的自定义要求
"""
```

### Q2: 视频生成失败？

检查以下几点：
1. `.env` 中 API Key 是否填写正确（也可在 Web 设置页面修改）
2. API 配额是否用完
3. Prompt 是否包含敏感内容
4. 使用 Seedance 时确认火山引擎账户余额充足

### Q3: 如何选择视频时长？

在 Web 界面的服务选择卡片中切换：
- **豆包 Seedance** — 5 秒，~¥0.9
- **Creatok** — 15 秒，~¥2.2

### Q4: 如何批量处理多个产品？

在 Web 界面打开 **批量处理**（/batch.html）：
1. 下载 CSV 模板，填写产品名称和卖点
2. 上传 CSV 文件（最多 20 个产品）
3. 点击「开始批量生成」，完成后一键下载 ZIP

### Q5: 如何添加背景音乐？

将 mp3 / wav / m4a / aac 文件放入 `static/bgm/` 目录，生成时在 Web 界面勾选「混入 BGM」即可。

---

## 🐛 调试

### 开启详细日志

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 测试单个模块

```bash
# 测试图片处理
python -m src.image_processor

# 测试 Prompt 生成
python -m src.prompt_generator
```

---

## 📞 技术支持

遇到问题？

- 查看 [CLAUDE.md](../CLAUDE.md) 了解项目架构和开发记录
- 查看 [PRD_v2.md](PRD_v2.md) 了解完整功能规划
- 提交 Issue: https://github.com/hitome0123/ai-video-generator/issues

---

**Happy Video Creating!**
