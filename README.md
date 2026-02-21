# AI 短视频生成器

**输入产品图片，自动输出 TikTok 带货短视频**

AI 驱动的一站式视频生成系统，面向跨境电商卖家。上传产品照片，系统自动完成图片处理、脚本生成、AI 视频制作、字幕/BGM 后处理全流程。

---

## 功能特性

- **AI 图片处理** — GPT-4o Vision 分析产品外观，DALL·E 3 生成专业白底图
- **智能脚本生成** — GPT-4o 生成 TikTok 爆款脚本（痛点 + 卖点 + CTA 结构）
- **双引擎视频生成** — 支持豆包 Seedance（推荐）和 Creatok 两种 AI 视频服务
- **AI 卖点建议** — 输入产品名，GPT-4o 自动补充核心卖点
- **竞品文案分析** — 粘贴竞品内容，AI 提取卖点、钩子句式和策略摘要
- **后处理** — FFmpeg 自动烧录字幕、混入背景音乐（BGM）
- **历史记录** — SQLite 持久化任务，重启后可重新下载视频
- **Web 界面** — 浏览器全流程操作，无需命令行

---

## 生成流程

```
产品图片 (JPG/PNG)
    ↓
Step 1  GPT-4o Vision 分析产品  →  产品描述 JSON
    ↓
Step 2  DALL·E 3 生成白底图    →  1024×1792 PNG
    ↓
Step 3  GPT-4o 生成视频脚本   →  script.json（hook / scenes / cta）
    ↓
Step 4  GPT-4o 优化视频 Prompt →  video_prompt.txt
    ↓
Step 5  AI 视频生成
        ├── 豆包 Seedance（推荐）→  5 秒 MP4，约 ¥0.9
        └── Creatok             →  15 秒 MP4，约 ¥2.2
    ↓
Step 6  后处理（可选）
        ├── FFmpeg 字幕烧录
        └── BGM 混音
```

---

## 快速开始

### 1. 安装依赖

```bash
git clone https://github.com/hitome0123/ai-video-generator.git
cd ai-video-generator
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
cp .env.example .env
```

编辑 `.env`，填入以下 Key：

```env
# 必填
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx

# 视频生成（二选一，推荐 Seedance）
ARK_API_KEY=xxxxxxxxxxxxxxxx        # 豆包 Seedance（火山引擎）
CREATOK_API_KEY=xxxxxxxxxxxxxxxx    # Creatok（备选）
```

**API Key 获取地址：**

| Key | 申请地址 |
|-----|---------|
| OPENAI_API_KEY | https://platform.openai.com/api-keys |
| ARK_API_KEY | https://console.volcengine.com → 火山方舟 → API Key 管理 |
| CREATOK_API_KEY | https://www.creatok.ai |

### 3. 启动 Web 界面（推荐）

```bash
python run.py
```

浏览器打开 **http://localhost:8000**，按页面引导操作即可。

### 4. 命令行模式（可选）

```bash
python main.py <图片路径> <产品名称> <卖点1> [卖点2] ...

# 示例
python main.py smartwatch.jpg "智能手表V8 Pro" "30天续航" "50米防水" "心率监测"
```

### 5. 添加背景音乐（可选）

将 mp3/wav 文件放入 `static/bgm/` 目录，生成时勾选「混入 BGM」即可自动混音。

---

## 输出文件

```
output/<job_id>/
├── processed/
│   └── white_bg.png        # DALL·E 生成的白底图
├── script.json             # 视频脚本（hook / scenes / cta）
├── video_prompt.txt        # AI 视频生成 Prompt
└── <产品名>.mp4            # 成品视频（含字幕/BGM）
```

历史任务记录保存在 `data/jobs.db`（SQLite），服务重启后可通过历史记录页面重新下载。

---

## 项目结构

```
ai-video-generator/
├── run.py                      # 一键启动 Web 服务器
├── main.py                     # 命令行工具
├── requirements.txt
├── .env.example                # API Key 配置模板
├── src/
│   ├── config.py               # 配置管理
│   ├── utils.py                # 工具函数（JSON 解析等）
│   ├── image_processor.py      # 图片处理（GPT-4o + DALL·E 3）
│   ├── prompt_generator.py     # 脚本 & Prompt 生成（GPT-4o）
│   ├── video_generator.py      # 视频生成（Seedance / Creatok）
│   ├── post_processor.py       # 后处理（FFmpeg 字幕 + BGM）
│   ├── database.py             # SQLite 任务持久化
│   ├── competitor_analyzer.py  # AI 卖点建议 + 竞品分析
│   └── api_server.py           # FastAPI 后端
├── static/
│   ├── index.html              # Web 前端（主页）
│   ├── history.html            # 历史记录页面
│   └── bgm/                    # 背景音乐目录（放置 mp3/wav）
├── data/                       # SQLite 数据库（自动创建）
├── docs/
│   ├── PRD.md                  # 产品需求文档
│   └── QUICKSTART.md           # 详细上手指南
└── output/                     # 视频输出目录（自动创建）
```

---

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/generate` | 提交生成任务 |
| GET | `/api/status/{job_id}` | 查询任务进度 |
| GET | `/api/download/{job_id}` | 下载视频 |
| GET | `/api/history` | 获取历史记录 |
| DELETE | `/api/history/{job_id}` | 删除任务记录 |
| POST | `/api/suggest-selling-points` | AI 卖点建议 |
| POST | `/api/analyze-competitor` | 竞品文案分析 |

---

## 视频服务对比

| 项目 | 豆包 Seedance（推荐）| Creatok |
|------|---------------------|---------|
| 视频时长 | 5 秒 | 15 秒 |
| 单次成本 | ~¥0.9 | ~¥2.2 |
| 网络要求 | 国内直连 | 需境外网络 |
| 图生视频 | ✅ 支持 | ✅ 支持 |

---

## 成本参考

| 项目 | 成本 |
|------|------|
| GPT-4o 图片分析 | ~$0.01 |
| DALL·E 3 白底图 | ~$0.08 |
| GPT-4o 脚本生成 | ~$0.02 |
| 豆包 Seedance 视频 | ~¥0.9 |
| **合计（Seedance 方案）** | **~¥1.5 / 视频** |

---

## 开发进度

- [x] 图片处理模块（GPT-4o Vision + DALL·E 3）
- [x] Prompt 生成模块（GPT-4o 脚本 + 视频 Prompt）
- [x] 视频生成模块（豆包 Seedance + Creatok 双引擎）
- [x] FastAPI 后端服务
- [x] Web 界面（上传 / 服务选择 / 进度展示 / 下载）
- [x] 后处理（FFmpeg 字幕烧录 + BGM 混音）
- [x] 历史记录（SQLite 持久化 + 历史页面）
- [x] AI 卖点建议 + 竞品文案分析
- [x] 命令行工具
- [ ] 批量处理（Excel 导入 + 队列生成）

---

## License

MIT
