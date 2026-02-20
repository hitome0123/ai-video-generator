# AI短视频制作系统

## 项目概述

**一句话描述**: 输入产品照片，输出可发布的TikTok带货短视频

**目标用户**: 跨境电商卖家、TikTok带货达人

**核心价值**:
- 降低短视频制作门槛
- 提高内容生产效率
- 标准化爆款视频生成流程

---

## 系统架构

```
产品照片 → 图片处理 → 卖点分析 → Prompt生成 → AI视频生成 → 成品视频
```

### 5个核心模块

| 模块 | 功能 | 工具 |
|------|------|------|
| **图片处理** | 抠图+高清修复+九宫格 | ChatGPT Vision + Wink |
| **卖点分析** | 对标产品+提取卖点 | FastMoss + 达人精灵 + ChatGPT |
| **Prompt生成** | 视频脚本+产品描述 | ChatGPT |
| **视频生成** | AI生成视频 | Sora / Creatok |
| **后处理** | 去水印+添加字幕 | ezremove + FFmpeg |

---

## 技术栈

| 类型 | 技术 |
|------|------|
| 语言 | Python 3.11+ |
| Web框架 | FastAPI |
| 图像处理 | PIL / OpenCV |
| AI接口 | OpenAI API (GPT-4V) |
| 视频处理 | FFmpeg |
| 任务队列 | Celery + Redis |

---

## 外部API依赖

| 服务 | 用途 | 预估成本 |
|------|------|---------|
| OpenAI (GPT-4V) | 抠图、卖点、Prompt | $0.01-0.03/次 |
| FastMoss | 对标产品分析 | 需订阅 |
| Sora | 视频生成 | $0.2-0.5/视频 |
| Creatok | 视频生成 | $0.1-0.3/视频 |
| 去水印API | 水印移除 | $0.05/视频 |

---

## 项目文件结构

```
ai-video-generator/
├── CLAUDE.md              # 本文件 - 项目文档
├── TODO.md                # 开发进度
├── run.py                 # 一键启动 Web 服务器
├── main.py                # 命令行工具（CLI 模式）
├── requirements.txt       # Python 依赖
├── .env.example           # API Key 配置模板
├── docs/
│   ├── AI流程.docx              # 客户原始需求
│   ├── AI短视频制作系统设计.md    # 详细设计文档
│   ├── PRD.md                   # 产品需求文档
│   ├── QUICKSTART.md            # 快速上手指南
│   └── 客户沟通_API_Key申请.md   # 话术文档
├── src/
│   ├── config.py             # 配置管理（读取 .env）
│   ├── image_processor.py    # 图片处理模块
│   ├── prompt_generator.py   # Prompt 生成模块
│   ├── video_generator.py    # 视频生成模块
│   └── api_server.py         # FastAPI 后端服务
├── static/
│   └── index.html            # Web 前端页面
└── output/                   # 视频输出目录（自动创建）
```

---

## 开发计划

| 阶段 | 内容 | 工时 | 状态 |
|------|------|------|------|
| Phase 1 | 图片处理模块 | 8h | ✅ 已完成 |
| Phase 2 | 卖点分析模块 | 12h | ⏳ 待开发 |
| Phase 3 | Prompt生成模块 | 8h | ✅ 已完成 |
| Phase 4 | 视频生成模块 | 12h | ✅ 已完成（基础版）|
| Phase 5 | API服务+部署 | 8h | ✅ 已完成 |
| Phase 6 | Web界面 | 12h | ✅ 已完成 |
| **总计** | | **60h** | **约 65% 完成** |

---

## MVP方案（20小时）

```
MVP功能:
├── 手动上传产品图片
├── ChatGPT抠图 + 描述产品
├── 手动输入卖点 (跳过FastMoss)
├── ChatGPT生成Prompt
├── 调用Creatok生成视频
└── 手动下载结果
```

---

## 报价参考

| 方案 | 内容 | 报价 |
|------|------|------|
| MVP版 | 核心流程跑通 | 8,000-12,000元 |
| 标准版 | 完整功能 | 20,000-30,000元 |
| 含Web界面 | 全套系统 | 30,000-40,000元 |

---

## 相关链接

| 工具 | 链接 |
|------|------|
| Sora | https://sora.chatgpt.com/ |
| Creatok | https://www.creatok.ai/ |
| FastMoss | https://fastmoss.com/ |
| 去水印 | https://ezremove.ai/sora-watermark-remover/ |

---

## 进度记录

### 2026-02-20 ✅ MVP 开发完成

**里程碑**: MVP 版本开发完成，等待 API Key 测试

#### 已完成
- [x] 图片处理模块 (`src/image_processor.py` - 445行)
  - ChatGPT Vision 产品分析
  - DALL·E 3 白底图生成（1024x1792）
- [x] Prompt 生成模块 (`src/prompt_generator.py` - 308行)
  - GPT-4 视频脚本生成（痛点+卖点+CTA结构）
  - 视频 Prompt 优化
- [x] 视频生成模块 (`src/video_generator.py` - 257行)
  - Creatok API 集成
  - 异步任务状态查询
  - 视频下载
- [x] 命令行工具 (`main.py` - 182行)
  - 一键执行完整流程
  - 输出结构化结果
- [x] 文档完善
  - README 更新（MVP 说明）
  - QUICKSTART.md（快速上手指南）
  - 客户沟通_API_Key申请.md（话术文档）

#### 技术实现
```
产品图片 (JPG/PNG)
    ↓
[步骤 1] ChatGPT Vision 分析产品 → 产品描述 JSON
    ↓
[步骤 2] DALL·E 3 生成白底图 → 1024x1792 PNG
    ↓
[步骤 3] GPT-4 生成视频脚本 → script.json (hook/scenes/cta)
    ↓
[步骤 4] GPT-4 优化视频 Prompt → video_prompt.txt
    ↓
[步骤 5] Creatok 生成视频 → MP4 (9:16, 15秒)
```

#### 成本
- **单个视频**: ~$0.31 (约 ¥2.2)
  - GPT-4V 分析: $0.01
  - DALL·E 3: $0.08
  - GPT-4 脚本: $0.02
  - Creatok: $0.20

#### 下一步
- [ ] 等待客户提供 API Key
  - OpenAI API Key (必需)
  - Creatok API Key (必需)
- [ ] 端到端测试
- [ ] 根据效果优化 Prompt 模板

---

### 2026-02-20 ✅ Web 界面开发完成

**里程碑**: 完整 Web 界面上线，客户可通过浏览器直接使用，无需命令行

#### 已完成
- [x] FastAPI 后端服务 (`src/api_server.py`)
  - POST /api/generate（上传图片 + 提交产品信息）
  - GET /api/status/{job_id}（实时查询生成进度）
  - GET /api/download/{job_id}（下载成品 MP4）
  - 后台线程异步处理，前端无需等待
- [x] Web 前端页面 (`static/index.html`)
  - 图片上传区（点击 / 拖拽，带实时预览）
  - 产品信息表单（名称 + 卖点多行输入）
  - 3 步骤进度显示（每 4 秒自动轮询）
  - 完成后一键下载 MP4
  - 纯 HTML/CSS/JS，无外部依赖
- [x] 一键启动脚本 (`run.py`)
- [x] 依赖更新（`requirements.txt` 新增 aiofiles）

#### 使用方式
```bash
python run.py
# 浏览器打开 http://localhost:8000
```

#### 当前待完成项
- [ ] 等待 API Key 进行端到端测试
- [ ] Creatok 参考图上传（video_generator.py 中有 TODO 占位）
- [ ] Phase 2：FastMoss 竞品分析（标准版功能）
- [ ] 去水印 + FFmpeg 后处理（标准版功能）

### 2026-02-14
- [x] 分析客户需求文档 (AI流程.docx)
- [x] 完成详细设计文档
- [x] 创建项目目录结构

---

*创建日期: 2026-02-14*
*最后更新: 2026-02-20（Web 界面完成）*
