# TODO清单 - AI短视频制作系统

**整体进度**: 65% (MVP + Web 界面完成，等待 API Key 测试)
**更新时间**: 2026-02-20

---

## 📋 项目概览

| 项目 | 说明 |
|------|------|
| **目标** | 输入产品照片 → 输出TikTok带货短视频 |
| **总工时** | 60小时（完整版）/ 20小时（MVP） |
| **当前阶段** | ✅ MVP + Web 界面完成，等待 API Key 测试 |

---

## ✅ 已完成（MVP）

### 设计阶段
- [x] 分析客户需求文档 (AI流程.docx)
- [x] 完成详细设计文档 (docs/AI短视频制作系统设计.md)
- [x] 确定技术架构和数据流
- [x] 创建项目目录结构

### 开发阶段 (2026-02-20) - MVP
- [x] 图片处理模块 (src/image_processor.py)
  - [x] ChatGPT Vision 产品分析
  - [x] DALL·E 3 白底图生成
- [x] Prompt 生成模块 (src/prompt_generator.py)
  - [x] GPT-4 视频脚本生成
  - [x] Prompt 优化
- [x] 视频生成模块 (src/video_generator.py)
  - [x] Creatok API 集成
  - [x] 状态查询和下载
- [x] 命令行工具 (main.py)
- [x] 文档
  - [x] README 更新
  - [x] QUICKSTART.md
  - [x] 客户沟通_API_Key申请.md

### 开发阶段 (2026-02-20) - Web 界面
- [x] FastAPI 后端服务 (src/api_server.py)
  - [x] POST /api/generate（接收图片+产品信息，启动后台线程）
  - [x] GET /api/status/{job_id}（实时查询进度）
  - [x] GET /api/download/{job_id}（下载 MP4）
  - [x] 静态文件托管
- [x] Web 前端页面 (static/index.html)
  - [x] 图片上传（点击/拖拽，带预览）
  - [x] 产品信息表单（名称 + 卖点）
  - [x] 3 步骤进度显示（实时轮询）
  - [x] 完成后下载按钮
- [x] 一键启动脚本 (run.py)
- [x] 更新依赖 (requirements.txt 添加 aiofiles)

### 代码统计
- 总代码量: ~1900 行
- 核心模块: 5 个（含 api_server.py）
- 前端页面: 1 个
- 文档: 3 个

---

## 🔴 Phase 1: 图片处理模块 (8小时)

### 1.1 ChatGPT抠图
- [ ] OpenAI API集成
- [ ] Vision API调用抠图
- [ ] 白底图片生成

### 1.2 高清修复
- [ ] 调研超分辨率API (Wink/其他)
- [ ] 集成高清修复功能
- [ ] 4K输出

### 1.3 九宫格合成
- [ ] PIL/OpenCV图像合成
- [ ] 3x3布局模板
- [ ] 自适应尺寸

---

## 🔴 Phase 2: 卖点分析模块 (12小时)

### 2.1 对标产品分析
- [ ] FastMoss API/爬虫调研
- [ ] TOP10爆款视频获取
- [ ] 视频链接提取

### 2.2 卖点提取
- [ ] 达人精灵集成（或替代方案）
- [ ] 视频字幕提取
- [ ] 卖点文案解析

### 2.3 卖点整合
- [ ] ChatGPT整合优化
- [ ] 结构化输出 (JSON)
- [ ] 痛点/卖点/场景分类

---

## 🔴 Phase 3: Prompt生成模块 (8小时)

### 3.1 视频脚本生成
- [ ] 视频结构模板设计
- [ ] ChatGPT脚本生成
- [ ] 分镜描述输出

### 3.2 产品外形描述
- [ ] ChatGPT Vision产品分析
- [ ] 外形锁定Prompt
- [ ] 细节描述

### 3.3 Prompt合并
- [ ] 视频内容 + 产品锁定
- [ ] 格式优化
- [ ] 多版本生成

---

## 🔴 Phase 4: 视频生成模块 (12小时)

### 4.1 Sora/Creatok集成
- [ ] API接入调研
- [ ] 视频生成调用
- [ ] 参考图片上传

### 4.2 去水印
- [ ] ezremove API集成
- [ ] 备选方案 (magiceraser)
- [ ] 质量检测

### 4.3 后处理
- [ ] FFmpeg集成
- [ ] 字幕添加（可选）
- [ ] BGM添加（可选）

---

## ✅ Phase 5: API服务 (8小时) - 已完成

- [x] FastAPI项目搭建 (src/api_server.py)
- [x] RESTful API设计
- [x] 文件上传接口 (multipart/form-data)
- [x] 后台线程异步处理（threading，无需 Celery）
- [x] 结果查询接口 (/api/status/{job_id})

---

## ✅ Phase 6: Web界面 (12小时) - 已完成（简化版）

- [x] 纯 HTML/CSS/JS 前端（无需 Vue/React，更易维护）
- [x] 上传页面（拖拽 + 点击，图片预览）
- [x] 进度展示（3 步骤 + 实时轮询）
- [x] 结果下载（完成后一键下载 MP4）
- [ ] 历史记录（待后续迭代）

---

## 📊 工作量汇总

| 阶段 | 内容 | 工时 | 优先级 | 状态 |
|------|------|------|--------|------|
| Phase 1 | 图片处理 | 8h | P0 | ⏳ 待开发 |
| Phase 2 | 卖点分析 | 12h | P0 | ⏳ 待开发 |
| Phase 3 | Prompt生成 | 8h | P0 | ⏳ 待开发 |
| Phase 4 | 视频生成 | 12h | P0 | ⏳ 待开发 |
| Phase 5 | API服务 | 8h | P1 | ✅ 已完成 |
| Phase 6 | Web界面 | 12h | P2 | ✅ 已完成 |
| **总计** | | **60h** | | |

---

## 🚀 MVP优先开发（20小时）

如果时间紧迫，先做MVP:

```
MVP = Phase 1 + Phase 3 + Phase 4 (部分)

具体内容:
├── ChatGPT抠图 (3h)
├── 手动输入卖点 (跳过Phase 2)
├── ChatGPT生成Prompt (4h)
├── Creatok生成视频 (8h)
└── 去水印输出 (5h)

总计: 20小时
```

---

## ⚠️ 风险项

| 风险 | 影响 | 应对 |
|------|------|------|
| Sora API限制 | 无法调用 | 备选Creatok |
| FastMoss封禁 | 无法对标 | 手动输入 |
| 视频质量不稳定 | 需重试 | 多版本生成 |
| API成本高 | 每视频$0.5-1 | 批量优惠 |

---

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `CLAUDE.md` | 项目概述文档 |
| `docs/AI流程.docx` | 客户原始需求 |
| `docs/AI短视频制作系统设计.md` | 详细设计文档 |

---

*最后更新: 2026-02-20*
