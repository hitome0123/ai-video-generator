# AI TikTok Video Generator - MVP

**状态**: ✅ MVP 开发完成，可测试使用

AI 驱动的 TikTok 产品视频自动生成系统。上传产品图片，自动完成扩图、脚本生成、视频制作全流程。

## 🚀 MVP Features（已实现）

- ✅ **AI 图片处理**: ChatGPT Vision 分析产品 + DALL·E 3 生成白底图
- ✅ **智能脚本生成**: GPT-4 生成 TikTok 爆款视频脚本
- ✅ **AI 视频生成**: 集成 Creatok API 自动生成 9:16 竖版视频
- ✅ **一站式流程**: 命令行一键执行，从图片到成品视频

## 💡 MVP 工作流程

```
产品图片 (JPG/PNG)
    ↓
[步骤 1] ChatGPT Vision 分析产品
    ↓
[步骤 2] DALL·E 3 生成白底图（1024x1792）
    ↓
[步骤 3] GPT-4 生成视频脚本（痛点+卖点+CTA）
    ↓
[步骤 4] GPT-4 优化视频 Prompt
    ↓
[步骤 5] Creatok 生成视频（15秒）
    ↓
输出: MP4 视频 + 脚本 JSON + Prompt TXT
```

## ⚡ 快速开始

### 1. 安装依赖

```bash
cd ai-video-generator
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
cp .env.example .env
# 编辑 .env，填入以下 API Key:
# - OPENAI_API_KEY (必需)
# - CREATOK_API_KEY (必需)
```

### 3. 运行示例

```bash
python main.py smartwatch.jpg "智能手表V8 Pro" "30天续航" "50米防水" "心率监测"
```

**参数说明**:
- `smartwatch.jpg`: 产品图片路径
- `"智能手表V8 Pro"`: 产品名称
- `"30天续航"` `"50米防水"` `"心率监测"`: 卖点列表（3-5个）

### 4. 查看输出

```
output/smartwatch/
├── processed/           # 处理后的图片
│   └── white_bg.png     # DALL·E 生成的白底图
├── script.json          # 视频脚本（含分镜）
├── video_prompt.txt     # 视频生成 Prompt
└── 智能手表V8_Pro.mp4   # 生成的视频
```

## Documentation

- [Product Requirements (PRD)](docs/PRD.md)
- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOY.md)

## Project Structure

```
ai-video-generator/
├── client/                 # Next.js frontend
│   ├── app/
│   ├── components/
│   └── package.json
├── server/                 # FastAPI backend
│   ├── api/
│   ├── services/
│   ├── models/
│   └── requirements.txt
├── n8n-workflows/          # n8n workflow JSON files
│   ├── main-workflow.json
│   └── video-generation.json
├── docs/                   # Documentation
│   ├── PRD.md
│   └── API.md
├── docker-compose.yml
└── README.md
```

## Environment Variables

```env
# OpenAI
OPENAI_API_KEY=sk-xxx

# Sora (if available)
SORA_API_KEY=xxx

# Creatok
CREATOK_API_KEY=xxx

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/ai_video

# Storage
OSS_ACCESS_KEY=xxx
OSS_SECRET_KEY=xxx
OSS_BUCKET=ai-video-generator
```

## 📋 Roadmap

### Phase 1: MVP ✅ 已完成（2026-02-20）
- [x] 图片处理模块（ChatGPT Vision + DALL·E 3）
- [x] Prompt 生成模块（GPT-4 脚本生成）
- [x] 视频生成模块（Creatok 集成）
- [x] 命令行工具（main.py）

### Phase 2: 完整功能（开发中）
- [ ] FastMoss 竞品分析集成
- [ ] 去水印功能（ezremove API）
- [ ] 批量处理（Excel 导入）
- [ ] FastAPI 服务端
- [ ] Web 界面（Next.js）

### Phase 3: SaaS 化（规划中）
- [ ] 用户系统
- [ ] 多租户支持
- [ ] 付费订阅
- [ ] 数据分析看板

## License

MIT
