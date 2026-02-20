# AI TikTok 产品视频生成系统

## Product Requirements Document (PRD)

**Version:** 1.2
**Date:** 2026-02-20
**Author:** Mantou AI Studio
**Status:** Active

---

## Changelog

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| 1.0 | 2026-02-20 | 初版 PRD |
| 1.1 | 2026-02-20 | MVP + Web 界面完成 |
| 1.2 | 2026-02-20 | 新增豆包 Seedance 视频生成方案，重新规划后续路线图 |

---

## 1. 概述

### 1.1 产品简介

一套自动化 AI 视频生成系统，帮助跨境电商卖家快速将产品图片转化为 TikTok 营销短视频。用户只需上传产品照片，系统自动完成扩图、卖点提取、脚本生成、视频制作全流程。

### 1.2 目标用户

- 跨境电商卖家（TikTok Shop）
- 电商代运营公司
- 短视频内容制作团队

### 1.3 核心价值

| 痛点 | 解决方案 |
|------|----------|
| 手动流程繁琐，单个视频耗时 2-3 小时 | 自动化流水线，10 分钟出片 |
| 需要多个工具切换（ChatGPT、Wink、Sora...） | 一站式平台，上传即出片 |
| 卖点提炼靠经验，质量不稳定 | AI + 竞品数据，标准化输出 |
| 无法批量生产 | 支持批量上传，队列处理 |

---

## 2. 当前完成状态（截至 2026-02-20）

```
✅ 已完成                          ⏳ 待开发
─────────────────────────────────────────────
✅ 图片处理模块                    ⏳ Seedance 视频生成集成
   - GPT-4o Vision 产品分析              ⏳ 视频服务选择器（前端）
   - DALL·E 3 白底图生成                 ⏳ 后处理模块（字幕/BGM）
                                         ⏳ 历史记录功能
✅ Prompt 生成模块                  ⏳ 竞品分析（FastMoss）
   - GPT-4o 视频脚本生成                 ⏳ 批量处理
   - 视频 Prompt 优化

✅ 视频生成模块（Creatok）
   - API 集成
   - 状态查询 + 下载

✅ Web 界面
   - FastAPI 后端
   - HTML 前端（上传/进度/下载）

✅ 命令行工具（main.py）
```

---

## 3. 系统架构

### 3.1 技术栈

| 层级 | 技术选型 | 说明 |
|------|----------|------|
| 前端 | 纯 HTML/CSS/JS | 当前 Web 界面 |
| 后端 | Python FastAPI | API 服务 ✅ 已实现 |
| 工作流 | threading（MVP）→ Celery（标准版） | 异步任务处理 |
| 数据库 | SQLite（MVP）→ PostgreSQL（标准版） | 任务/历史数据 |
| 存储 | 本地文件系统（MVP）→ 阿里云 OSS（标准版） | 图片/视频 |
| 图像处理 | PIL / OpenCV | 本地图像操作 |
| 视频处理 | FFmpeg | 字幕/BGM 合成 |

### 3.2 核心流程

```
产品图片 (JPG/PNG)
    │
    ▼ Step 1: 图片处理
GPT-4o Vision 分析产品 → 产品描述 JSON
DALL·E 3 生成白底图 → 1024x1792 PNG
    │
    ▼ Step 2: Prompt 生成
GPT-4o 生成视频脚本 → script.json (hook/scenes/cta)
GPT-4o 优化视频 Prompt → video_prompt.txt
    │
    ▼ Step 3: 视频生成（可选其一）
    ├── Creatok API → MP4 (9:16, 15秒)
    └── 豆包 Seedance API → MP4 (9:16, 5秒)
    │
    ▼ Step 4: 后处理（标准版）
FFmpeg 添加字幕 + BGM → 成品视频
```

---

## 4. 视频生成方案对比

### 4.1 三种视频生成服务

| 项目 | Creatok | 豆包 Seedance | Sora |
|------|---------|--------------|------|
| **适用场景** | 国际市场 | 国内/国际均可 | 国际市场 |
| **视频时长** | 15秒 | 5秒（可拼接） | 5-20秒 |
| **画面质量** | ★★★★ | ★★★★★ | ★★★★★ |
| **生成速度** | 2-3 分钟 | 1-2 分钟 | 慢 |
| **API 文档** | 完善 | 完善（火山引擎） | 有限 |
| **网络要求** | 需境外代理 | 国内可直连 | 需境外代理 |
| **单次成本** | ~$0.20 | ~¥0.14（约$0.02） | $0.20+ |
| **参考图支持** | 支持（待完善） | 支持（图生视频） | 支持 |

### 4.2 Seedance 集成说明

豆包 Seedance 通过**火山引擎 ARK 平台**调用：

- **平台**: 火山引擎 (volcengine.com)
- **API 地址**: `https://ark.cn-beijing.volces.com/api/v3/`
- **模型**: `doubao-seedance-1-0-lite-i2v-250428`（图生视频）
- **所需 Key**: 火山引擎 API Key（ARK_API_KEY）
- **申请地址**: https://www.volcengine.com/product/doubao

**Seedance 优势**：
- 国内服务器，无需翻墙
- 成本极低（约 ¥0.14/次）
- 支持图生视频（将白底产品图作为参考帧）
- 字节跳动官方模型，质量可靠

---

## 5. 功能清单

### 5.1 P0 - 已完成（MVP 核心功能）

| 模块 | 功能 | 状态 |
|------|------|------|
| 图片处理 | GPT-4o Vision 产品分析 | ✅ |
| 图片处理 | DALL·E 3 白底图生成 | ✅ |
| Prompt 生成 | GPT-4o 视频脚本生成 | ✅ |
| Prompt 生成 | 视频 Prompt 优化 | ✅ |
| 视频生成 | Creatok API 集成 | ✅ |
| Web 界面 | 图片上传 + 进度展示 + 下载 | ✅ |
| 后端 API | FastAPI 服务 | ✅ |

### 5.2 P0 - 待开发（近期必做）

| 模块 | 功能 | 说明 |
|------|------|------|
| 视频生成 | **豆包 Seedance 集成** | 新增国内低成本方案 |
| 视频生成 | **Creatok 参考图上传修复** | 当前有 TODO 占位 |
| Web 界面 | **视频服务选择器** | 让用户选择 Creatok / Seedance |
| 配置 | **ARK_API_KEY 支持** | 新增火山引擎 Key 配置 |

### 5.3 P1 - 增强功能（二期）

| 模块 | 功能 | 说明 |
|------|------|------|
| 后处理 | FFmpeg 自动字幕 | 从 script.json 读取文案合成字幕 |
| 后处理 | BGM 添加 | 内置音乐库，自动匹配风格 |
| 后处理 | 去水印 | 接入 ezremove API |
| 历史记录 | 任务历史列表 | SQLite 存储，支持查询和重新下载 |
| 图片处理 | 高清修复 | Real-ESRGAN 超分辨率 |
| 图片处理 | 九宫格合成 | PIL 多图拼接 |

### 5.4 P2 - 标准版功能（三期）

| 模块 | 功能 | 说明 |
|------|------|------|
| 竞品分析 | FastMoss 对接 | 自动抓取竞品 TOP10 视频 |
| 竞品分析 | TikTok 链接解析 | 输入链接，AI 提取卖点 |
| 批量处理 | Excel 批量导入 | 多产品同时处理 |
| 多版本 | 一键生成 3 个版本 | A/B 测试支持 |
| 后处理 | AI 配音 | 自动生成语音旁白 |

### 5.5 P3 - SaaS 功能（四期）

| 模块 | 功能 | 说明 |
|------|------|------|
| 用户系统 | 登录 / 注册 | 支持多账号 |
| 计费 | 按量计费 | 按视频生成数量 |
| 存储 | 阿里云 OSS | 云端存储视频 |

---

## 6. 页面设计

### 6.1 当前页面（已实现）

```
http://localhost:8000/   →  主页（上传 + 生成 + 下载）
```

### 6.2 待新增页面

```
/           →  新建任务（当前已有，需增加服务选择）
/history    →  历史记录列表
/task/:id   →  任务详情（脚本预览 + 视频播放 + 重新生成）
```

### 6.3 新建任务流程（更新后）

```
Step 1: 上传图片
┌────────────────────────────────────┐
│  拖拽或点击上传产品图片             │
│  ┌─────────────────────────────┐   │
│  │   📷  点击上传/拖拽图片      │   │
│  └─────────────────────────────┘   │
└────────────────────────────────────┘
                 │
                 ▼
Step 2: 填写产品信息
┌────────────────────────────────────┐
│  产品名称: [                    ]  │
│  核心卖点: [                    ]  │
│           [  每行一个卖点        ]  │
└────────────────────────────────────┘
                 │
                 ▼
Step 3: 选择视频生成服务（新增）
┌────────────────────────────────────┐
│  ● 豆包 Seedance（推荐）           │
│    国内直连 · 速度快 · 成本低       │
│                                    │
│  ○ Creatok                         │
│    国际服务 · 15秒视频              │
└────────────────────────────────────┘
                 │
                 ▼
Step 4: 进度追踪（已实现）
┌────────────────────────────────────┐
│  ✓ 分析产品图片                    │
│  ⟳ 生成视频脚本...                 │
│  ○ AI 生成视频                     │
└────────────────────────────────────┘
```

---

## 7. API 设计

### 7.1 现有 API（已实现）

| 方法 | 路径 | 功能 |
|------|------|------|
| POST | /api/generate | 开始生成任务 |
| GET | /api/status/{job_id} | 查询进度 |
| GET | /api/download/{job_id} | 下载视频 |

### 7.2 待新增 API

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | /api/history | 获取历史任务列表 |
| GET | /api/history/{job_id} | 获取任务详情 |
| DELETE | /api/history/{job_id} | 删除任务记录 |

### 7.3 generate 接口更新（新增 video_service 参数）

```
POST /api/generate
Content-Type: multipart/form-data

字段:
- image          文件    产品图片（必填）
- product_name   文本    产品名称（必填）
- selling_points 文本    卖点列表，每行一个（必填）
- video_service  文本    视频生成服务: seedance / creatok（默认 seedance）
- duration       整数    视频时长秒数（默认 5）
```

### 7.4 任务状态流转

```
queued → step1(图片处理) → step2(生成脚本) → step3(视频生成) → success
                                                      ↓
                                                    failed
```

---

## 8. 外部服务与成本

### 8.1 AI 服务成本

| 服务 | 用途 | 单次成本 |
|------|------|---------|
| OpenAI GPT-4o | 产品分析 + 脚本生成 | ~$0.03 |
| OpenAI DALL·E 3 | 白底图生成 | ~$0.08 |
| 豆包 Seedance | 视频生成（推荐） | ~¥0.14（约$0.02）|
| Creatok | 视频生成（备选） | ~$0.20 |

**推荐方案总成本**（Seedance）：~$0.13/视频（约¥0.9）
**备选方案总成本**（Creatok）：~$0.31/视频（约¥2.2）

### 8.2 API Key 配置

| Key 名称 | 用途 | 获取地址 |
|---------|------|---------|
| OPENAI_API_KEY | GPT-4o + DALL·E 3 | platform.openai.com |
| ARK_API_KEY | 豆包 Seedance | volcengine.com |
| CREATOK_API_KEY | Creatok（备选） | creatok.ai |

---

## 9. 数据模型

### 9.1 任务数据结构（内存/SQLite）

```json
{
  "job_id": "uuid-xxx",
  "status": "success",
  "step": 3,
  "step_name": "完成",
  "product_name": "智能手表 V8 Pro",
  "video_service": "seedance",
  "video_path": "./output/uuid-xxx/xxx.mp4",
  "script": { "hook": "...", "scenes": [...], "cta": "..." },
  "video_prompt": "...",
  "created_at": "2026-02-20T10:00:00",
  "completed_at": "2026-02-20T10:05:00"
}
```

---

## 10. 开发路线图

### Phase 7：Seedance 集成 + 服务选择器（下一步）

```
优先级: P0（客户明确需求）
工时预估: 4-6 小时

内容:
├── src/config.py          → 添加 ARK_API_KEY、SEEDANCE_MODEL_ID
├── src/video_generator.py → 新增 SeedanceGenerator 类（图生视频）
├── src/api_server.py      → /api/generate 新增 video_service 参数
├── static/index.html      → 前端新增视频服务选择器（单选按钮）
└── .env.example           → 新增 ARK_API_KEY 说明
```

### Phase 8：后处理模块

```
优先级: P1
工时预估: 6-8 小时

内容:
├── src/post_processor.py  → 新建后处理模块
│   ├── FFmpeg 字幕合成（读取 script.json 中的 text 字段）
│   ├── BGM 添加（内置几首免版权背景音乐）
│   └── 去水印（接入 ezremove API）
└── static/index.html      → 后处理选项（是否加字幕/BGM）
```

### Phase 9：历史记录

```
优先级: P1
工时预估: 4-6 小时

内容:
├── src/database.py        → SQLite 任务持久化（重启不丢失）
├── src/api_server.py      → 新增 GET /api/history
└── static/history.html   → 历史记录页面（列表 + 重新下载）
```

### Phase 10：竞品分析（标准版）

```
优先级: P2
工时预估: 12 小时

内容:
├── src/competitor_analyzer.py → FastMoss API / TikTok 链接解析
└── static/index.html          → 新增「输入 TikTok 链接提取卖点」功能
```

### Phase 11：批量处理 + 多版本

```
优先级: P2
工时预估: 8 小时

内容:
├── 支持 Excel 批量导入多个产品
├── 每个产品生成 3 个视频版本（A/B 测试）
└── 队列管理界面
```

---

## 11. 风险与应对

| 风险 | 概率 | 应对措施 |
|------|------|----------|
| Creatok API 不稳定 | 高 | Seedance 作为主选，Creatok 备选 |
| Sora API 限制 | 高 | 已有 Creatok + Seedance 双备选 |
| OpenAI 境外网络问题 | 中 | Cloudflare Workers 中转或境外服务器 |
| Seedance 视频时长仅 5 秒 | 中 | 多段拼接或使用 Creatok 出 15 秒版 |
| 视频成本超预算 | 低 | Seedance 成本极低，可控 |

---

## 12. 附录

### 12.1 相关链接

| 工具 | 链接 |
|------|------|
| 豆包 Seedance | https://www.volcengine.com/product/doubao |
| 火山引擎控制台 | https://console.volcengine.com/ |
| Creatok | https://www.creatok.ai/ |
| Sora | https://sora.chatgpt.com/ |
| 去水印工具 | https://ezremove.ai/sora-watermark-remover/ |

### 12.2 术语表

| 术语 | 说明 |
|------|------|
| 图生视频 | 以产品图片作为第一帧，AI 生成后续动态画面 |
| ARK | 火山引擎的 AI 推理平台（Seedance 所在平台） |
| 扩图 | 使用 AI 扩展图片边缘，生成更大画幅 |
| 九宫格 | 将多张产品图拼接成 3x3 布局的合成图 |
| A/B 测试 | 同一产品生成多个版本，测试哪个效果更好 |
