# TODO清单 - AI短视频制作系统

**整体进度**: 75% (MVP + Web 界面 + Seedance 集成完成)
**更新时间**: 2026-02-21

---

## 📋 项目概览

| 项目 | 说明 |
|------|------|
| **目标** | 输入产品照片 → 输出TikTok带货短视频 |
| **当前阶段** | ✅ MVP + Web 界面 + Seedance 集成完成，下一步：后处理模块 |

---

## ✅ 已完成

### 设计阶段
- [x] 分析客户需求文档 (AI流程.docx)
- [x] 完成详细设计文档 (docs/AI短视频制作系统设计.md)
- [x] 确定技术架构和数据流
- [x] 创建项目目录结构

### Phase 1：图片处理模块 ✅
- [x] GPT-4o Vision 产品分析
- [x] DALL·E 3 白底图生成（1024x1792）

### Phase 3：Prompt 生成模块 ✅
- [x] GPT-4o 视频脚本生成（hook/scenes/cta 结构）
- [x] 视频 Prompt 优化

### Phase 4：视频生成模块（Creatok）✅
- [x] Creatok API 集成
- [x] 异步任务状态查询
- [x] 视频下载

### Phase 5：API 服务 ✅
- [x] FastAPI 后端 (src/api_server.py)
- [x] POST /api/generate（图片上传 + 产品信息）
- [x] GET /api/status/{job_id}（进度查询）
- [x] GET /api/download/{job_id}（视频下载）
- [x] 后台线程异步处理

### Phase 6：Web 界面 ✅
- [x] 图片上传（拖拽 + 预览）
- [x] 产品信息表单
- [x] 3 步骤进度显示（实时轮询）
- [x] 一键下载 MP4
- [x] 一键启动脚本 (run.py)

### 文档
- [x] README 更新
- [x] QUICKSTART.md
- [x] 客户沟通_API_Key申请.md
- [x] PRD v1.2（新增 Seedance 规划）

---

## ✅ Phase 7：豆包 Seedance 集成（2026-02-21 完成）

### 7.1 后端：Seedance 生成器
- [x] `src/config.py` 新增配置项
  - [x] `ARK_API_KEY`（火山引擎 API Key）
  - [x] `SEEDANCE_MODEL_ID`（doubao-seedance-1-0-lite-i2v-250428）
  - [x] `SEEDANCE_API_URL`（ARK 接口地址）
- [x] `src/video_generator.py` 重构为双后端架构
  - [x] `generate_with_seedance()`：图生视频，base64 传图，ARK API
  - [x] `check_seedance_status()`：轮询（submitted/processing/done/failed）
  - [x] `generate_with_creatok()`：同步修复参考图 base64 上传
  - [x] `generate_video()` 统一入口，通过 `backend` 参数路由
- [x] `.env.example` 更新为 ARK_API_KEY，附申请地址说明

### 7.2 后端：API 更新
- [x] `/api/generate` 新增 `video_service` 参数（seedance 默认 / creatok）
- [x] 根据参数动态调整时长（Seedance 5s / Creatok 15s）

### 7.3 前端：服务选择器
- [x] 新增视频服务选择卡片（Seedance 默认推荐 / Creatok 备选）
- [x] 显示各服务成本（¥0.9 / ¥2.2）
- [x] 切换时动态更新底部成本提示

---

## 🟡 Phase 8：后处理模块（P1）

### 8.1 字幕合成
- [ ] `src/post_processor.py` 新建后处理模块
- [ ] 从 `script.json` 的 `scenes[].text` 读取文案
- [ ] 调用 FFmpeg 将文字烧录到视频
- [ ] 支持字体、颜色、位置配置

### 8.2 BGM 添加
- [ ] 内置 3-5 首免版权背景音乐
- [ ] FFmpeg 混音（视频音轨 + BGM）
- [ ] 支持淡入淡出

### 8.3 去水印（可选）
- [ ] 调研 ezremove API 接入方式
- [ ] 集成去水印（如 Creatok 输出有水印时使用）

### 8.4 前端更新
- [ ] `static/index.html` 新增后处理选项
  - [ ] 开关：是否添加字幕
  - [ ] 开关：是否添加 BGM

---

## 🟡 Phase 9：历史记录（P1）

### 9.1 数据持久化
- [ ] `src/database.py` 使用 SQLite 存储任务
  - [ ] 任务基本信息（job_id, 产品名, 状态, 时间）
  - [ ] 视频文件路径
  - [ ] 生成的脚本和 Prompt
- [ ] 服务器重启后历史记录不丢失

### 9.2 API 新增
- [ ] `GET /api/history` 获取历史任务列表
- [ ] `DELETE /api/history/{job_id}` 删除记录+文件

### 9.3 前端：历史页面
- [ ] `static/history.html` 历史记录列表
  - [ ] 显示产品名、生成时间、状态
  - [ ] 点击可重新下载视频
  - [ ] 支持删除

---

## 🟢 Phase 10：竞品分析（P2，标准版）

### 10.1 FastMoss 对接
- [ ] 调研 FastMoss API 或爬虫方案
- [ ] 输入产品类目关键词，获取 TOP10 爆款视频
- [ ] 提取视频卖点文案

### 10.2 TikTok 链接解析
- [ ] 输入 TikTok 视频链接
- [ ] AI 分析视频内容，自动提取卖点
- [ ] 填充到卖点输入框

---

## 🟢 Phase 11：批量处理 + 多版本（P2，标准版）

- [ ] Excel 批量导入（多产品信息）
- [ ] 队列处理（多个产品同时排队生成）
- [ ] 每个产品生成 3 个视频版本（A/B 测试）
- [ ] 批量下载（ZIP 打包）

---

## 📊 工作量汇总

| 阶段 | 内容 | 工时 | 优先级 | 状态 |
|------|------|------|--------|------|
| Phase 1 | 图片处理 | 8h | P0 | ✅ 已完成 |
| Phase 2 | 卖点分析（FastMoss） | 12h | P2 | ⏳ 待开发 |
| Phase 3 | Prompt 生成 | 8h | P0 | ✅ 已完成 |
| Phase 4 | 视频生成（Creatok） | 12h | P0 | ✅ 已完成 |
| Phase 5 | API 服务 | 8h | P1 | ✅ 已完成 |
| Phase 6 | Web 界面 | 12h | P2 | ✅ 已完成 |
| Phase 7 | **Seedance 集成** | 4-6h | **P0** | ✅ 已完成 |
| Phase 8 | 后处理（字幕/BGM） | 6-8h | P1 | 🟡 待开发 |
| Phase 9 | 历史记录 | 4-6h | P1 | 🟡 待开发 |
| Phase 10 | 竞品分析 | 12h | P2 | 🟢 待开发 |
| Phase 11 | 批量处理 | 8h | P2 | 🟢 待开发 |
| **总计** | | **~100h** | | **约 75% 完成** |

---

## ⚠️ 已知 BUG / 待修复

| 问题 | 文件 | 说明 |
|------|------|------|
| ~~Creatok 参考图上传未实现~~ | ~~`src/video_generator.py`~~ | ✅ Phase 7 已修复 |
| JSON 解析用裸 except | `src/image_processor.py`, `src/prompt_generator.py` | 应改为解析 markdown 代码块中的 JSON |
| 无重试机制 | `src/video_generator.py` | API 调用失败无自动重试 |

---

## 🔑 待获取的 API Key

| Key | 用途 | 状态 |
|-----|------|------|
| OPENAI_API_KEY | GPT-4o + DALL·E 3 | ⏳ 等待客户提供 |
| CREATOK_API_KEY | Creatok 视频生成 | ⏳ 等待客户提供 |
| ARK_API_KEY | 豆包 Seedance | ⏳ 等待客户申请 |

---

## 📁 文件结构（当前）

```
ai-video-generator/
├── run.py                    # 一键启动 Web 服务器
├── main.py                   # 命令行工具
├── requirements.txt          # Python 依赖
├── .env.example              # API Key 配置模板
├── docs/
│   ├── PRD.md                # 产品需求文档（v1.2）✅ 已更新
│   ├── QUICKSTART.md         # 快速上手指南
│   ├── AI短视频制作系统设计.md  # 详细设计文档
│   └── 客户沟通_API_Key申请.md  # 话术文档
├── src/
│   ├── config.py             # 配置管理
│   ├── image_processor.py    # 图片处理模块 ✅
│   ├── prompt_generator.py   # Prompt 生成模块 ✅
│   ├── video_generator.py    # 视频生成（Creatok）✅ 待加 Seedance
│   └── api_server.py         # FastAPI 后端 ✅
├── static/
│   └── index.html            # Web 前端 ✅ 待加服务选择器
└── output/                   # 视频输出目录
```

---

*最后更新: 2026-02-21（Phase 7 Seedance 集成完成，整体进度 75%）*
