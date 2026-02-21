# AI 短视频生成器

**输入产品图片，自动输出 TikTok 带货短视频**

AI 驱动的一站式视频生成系统，面向跨境电商卖家。上传产品照片，系统自动完成图片处理、脚本生成、AI 视频制作全流程，10 分钟出片。

---

## 功能特性

- **AI 图片处理** — GPT-4o Vision 分析产品外观，DALL·E 3 生成专业白底图
- **智能脚本生成** — GPT-4o 生成 TikTok 爆款脚本（痛点 + 卖点 + CTA 结构）
- **双引擎视频生成** — 支持豆包 Seedance（推荐）和 Creatok 两种 AI 视频服务
- **Web 界面** — 浏览器上传图片、填写卖点、一键生成、下载视频，无需命令行

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

---

## 输出文件

```
output/<产品名>/
├── processed/
│   └── white_bg.png        # DALL·E 生成的白底图
├── script.json             # 视频脚本（hook / scenes / cta）
├── video_prompt.txt        # AI 视频生成 Prompt
└── 智能手表V8_Pro.mp4      # 成品视频
```

---

## 项目结构

```
ai-video-generator/
├── run.py                  # 一键启动 Web 服务器
├── main.py                 # 命令行工具
├── requirements.txt
├── .env.example            # API Key 配置模板
├── src/
│   ├── config.py           # 配置管理
│   ├── image_processor.py  # 图片处理（GPT-4o + DALL·E 3）
│   ├── prompt_generator.py # 脚本 & Prompt 生成（GPT-4o）
│   ├── video_generator.py  # 视频生成（Seedance / Creatok）
│   └── api_server.py       # FastAPI 后端
├── static/
│   └── index.html          # Web 前端
├── docs/
│   ├── PRD.md              # 产品需求文档
│   └── QUICKSTART.md       # 详细上手指南
└── output/                 # 视频输出目录（自动创建）
```

---

## 视频服务对比

| 项目 | 豆包 Seedance（推荐）| Creatok |
|------|---------------------|---------|
| 视频时长 | 5 秒 | 15 秒 |
| 单次成本 | ~¥0.9 | ~¥2.2 |
| 网络要求 | 国内直连 | 需境外网络 |
| 图生视频 | ✅ 支持 | ✅ 支持 |

---

## 开发进度

### 已完成

- [x] 图片处理模块（GPT-4o Vision + DALL·E 3）
- [x] Prompt 生成模块（GPT-4o 脚本 + 视频 Prompt）
- [x] 视频生成模块（豆包 Seedance + Creatok 双引擎）
- [x] FastAPI 后端服务
- [x] Web 界面（上传 / 选择服务 / 进度展示 / 下载）
- [x] 命令行工具

### 开发中 / 规划中

- [ ] 后处理：FFmpeg 自动添加字幕 + BGM
- [ ] 历史记录：任务列表持久化，支持重新下载
- [ ] 竞品分析：FastMoss 集成，自动提取爆款卖点
- [ ] 批量处理：Excel 导入，多产品队列生成

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

## License

MIT
