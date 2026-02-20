# AI TikTok Video Generator

AI 驱动的 TikTok 产品视频自动生成系统。上传产品图片，自动完成扩图、卖点分析、脚本生成、视频制作全流程。

## Features

- **一键生成**: 上传图片即可自动生成营销短视频
- **AI 扩图**: ChatGPT DALL·E 智能扩展产品图片
- **智能卖点**: AI 分析并补充产品卖点
- **多版本输出**: 每产品生成 3 个版本用于 A/B 测试
- **批量处理**: 支持 Excel 批量导入产品信息

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Next.js 14 + Tailwind CSS |
| Backend | Python FastAPI |
| Workflow | n8n (self-hosted) |
| Database | PostgreSQL |
| Storage | Aliyun OSS |
| Queue | Redis + Celery |

## Architecture

```
User Upload → AI Image Expand → Selling Points Analysis → Prompt Generation → Video Generation
                  ↓                     ↓                       ↓                    ↓
              DALL·E 3              GPT-4                   GPT-4            Sora/Creatok
```

## Quick Start

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/ai-video-generator.git
cd ai-video-generator

# Install dependencies
pip install -r requirements.txt
npm install --prefix client

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Run
docker-compose up -d
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

## Roadmap

- [x] PRD 完成
- [ ] MVP 开发 (2-3周)
  - [ ] 图片上传 + AI 扩图
  - [ ] 卖点分析 + 提示词生成
  - [ ] 视频生成集成
  - [ ] Web 界面
- [ ] Phase 2: 竞品数据对接 (FastMoss)
- [ ] Phase 3: SaaS 多租户

## License

MIT
