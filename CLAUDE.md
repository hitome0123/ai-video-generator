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
├── docs/
│   ├── AI流程.docx        # 客户原始需求
│   └── AI短视频制作系统设计.md  # 详细设计文档
├── src/
│   ├── image_processor.py    # 图片处理模块
│   ├── selling_analyzer.py   # 卖点分析模块
│   ├── prompt_generator.py   # Prompt生成模块
│   ├── video_generator.py    # 视频生成模块
│   └── api_server.py         # API服务
└── output/                # 输出目录
```

---

## 开发计划

| 阶段 | 内容 | 工时 | 状态 |
|------|------|------|------|
| Phase 1 | 图片处理模块 | 8h | 待开发 |
| Phase 2 | 卖点分析模块 | 12h | 待开发 |
| Phase 3 | Prompt生成模块 | 8h | 待开发 |
| Phase 4 | 视频生成模块 | 12h | 待开发 |
| Phase 5 | API服务+部署 | 8h | 待开发 |
| Phase 6 | Web界面 | 12h | 待开发 |
| **总计** | | **60h** | |

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

### 2026-02-14
- [x] 分析客户需求文档 (AI流程.docx)
- [x] 完成详细设计文档
- [x] 创建项目目录结构
- [ ] 开始MVP开发

---

*创建日期: 2026-02-14*
*最后更新: 2026-02-14*
