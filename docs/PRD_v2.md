# AI TikTok 广告自动化闭环系统

## Product Requirements Document (PRD)

**Version:** 2.0
**Date:** 2026-02-21
**状态:** 规划中（待开发）

---

## 一、产品愿景

> 从「生成一条视频」升级为「全自动广告投放 + 数据驱动优化的 AI 营销闭环」

**目标用户：** 跨境电商卖家、TikTok 带货团队
**核心价值：**
- 视频生成 → 自动投放 → 数据回收 → AI 优化 → 再投放，全流程无需人工干预
- 分阶段打品策略（初期/热度期/爆品期），系统自动识别并切换
- 爆款素材自动复制，批量产出高 ROAS 广告

---

## 二、系统全貌

```
┌──────────────────────────────────────────────────────────────────┐
│                        视频生成层（已完成）                         │
│  产品图片 → GPT-4o分析 → 脚本生成 → AI视频 → 字幕/BGM后处理       │
└────────────────────────┬─────────────────────────────────────────┘
                         │
            ┌────────────┴────────────┐
            ▼                         ▼
  ┌──────────────────┐      ┌──────────────────────┐
  │   轨道 A：自然流量  │      │   轨道 B：付费广告      │
  │   出海匠 API       │      │   TikTok Marketing   │
  │   多账号批量发布    │      │   API                │
  │   有机涨粉+曝光    │      │   Campaign 全生命周期  │
  └──────────────────┘      └──────────┬───────────┘
                                        │
                        ┌───────────────▼────────────────┐
                        │          数据监控层              │
                        │  TikTok Reporting API           │
                        │  指标：ROAS、CTR、CVR、曝光、消耗  │
                        │  频率：可配置（每天/每3天/每周）   │
                        └───────────────┬────────────────┘
                                        │
                        ┌───────────────▼────────────────┐
                        │        智能优化引擎              │
                        │  ① 筛选高 ROAS 广告素材          │
                        │  ② GPT-4o 拆解爆款脚本结构       │
                        │  ③ 批量生成相似脚本+视频          │
                        │  ④ 发出方式：人工确认 / 全自动    │
                        └───────────────┬────────────────┘
                                        │
                        ┌───────────────▼────────────────┐
                        │        全自动调度器              │
                        │  分阶段策略自动切换               │
                        │  预算自动扩/缩/暂停               │
                        │  操作日志全程记录                 │
                        └────────────────────────────────┘
```

---

## 三、分阶段打品策略

| 阶段 | 触发条件 | 核心 KPI | TikTok 优化目标 | 系统行为 |
|------|---------|---------|----------------|---------|
| **打品初期** | 新品上线 / 人工设定 | 播放量、曝光量 | VIDEO_VIEW / CPM | 广播投放，多素材测试，低出价 |
| **热度提升期** | 累计曝光 ≥ N 万 且点击率稳定 | ROAS | CONVERSIONS / VALUE | 暂停低 ROAS 广告，对高 ROAS 扩量 |
| **爆品期** | ROAS 连续 N 天 ≥ 目标值 | 日消耗规模 | MAXIMUM_CONVERSION_VALUE | 全力跑量，自动提预算上限 |

**阶段切换规则：** 阈值由人工在系统中设定，切换动作由调度器自动执行

---

## 四、功能模块详细说明

### Phase 12：广告投放集成（轨道 A + B）

#### 12.1 出海匠 API 集成（轨道 A）
- 多 TikTok 账号管理（账号列表、状态查询）
- 视频批量上传：将生成的视频自动发布到指定 TikTok 账号
- 发布配置：标题、话题标签、发布时间（定时发布）
- 多账号轮发（可设置发布到哪些账号、几个账号轮流发）

#### 12.2 TikTok Marketing API 集成（轨道 B）
- OAuth 2.0 认证 + Access Token 管理（自动刷新）
- 视频创意上传（POST /v1.3/file/video/ad/upload/）
- Campaign 创建（目标：VIDEO_VIEW / CONVERSIONS / VALUE）
- AdGroup 创建（受众定向、预算、出价策略、投放时间）
- Ad 创建（创意绑定、文案、落地页链接）
- 按阶段自动选择出价策略：
  - 初期：CPM/CPV
  - 热度期：Target CPA / ROAS Bidding
  - 爆品期：Lowest Cost + 高预算上限

#### 12.3 广告管理后台页面（`static/campaigns.html`）
- 当前所有广告系列列表（状态、阶段、今日消耗、ROAS）
- 单个广告详情（创意预览、指标趋势）
- 手动调整阶段 / 暂停 / 恢复
- 新建广告（从已生成的视频中选择素材）

---

### Phase 13：数据监控

#### 13.1 数据采集
- TikTok Reporting API 定时拉取（频率可配置）
- 采集指标：
  - 广告层：impressions、clicks、spend、conversions、purchase_roas、ctr、cvr
  - 账号层（轨道 A）：video_views、likes、shares、comments、followers_gained
- 数据存储：SQLite 新增 performance_daily 表

#### 13.2 数据看板（`static/analytics.html`）
- 总览：今日消耗、总 ROAS、总曝光、总转化
- 广告列表：按 ROAS 排序，标注高/中/低表现
- 折线图：ROAS / 消耗 / 曝光 趋势（7日/30日）
- 阶段分布：各阶段广告数量和消耗占比
- 自然流量：各账号播放量、涨粉趋势

#### 13.3 异常告警
- ROAS 跌破设定阈值 → 自动暂停广告 + 记录日志
- 单日消耗超出预算上限 → 告警 + 暂停
- 账号发布失败 → 记录错误

---

### Phase 14：智能优化引擎

#### 14.1 爆款素材筛选
- 筛选条件：ROAS ≥ 目标值 × 1.2，且运行时间 ≥ 3 天
- 从数据库中提取符合条件的广告及其对应视频 job_id

#### 14.2 GPT-4o 脚本拆解
- 输入：爆款视频的 script.json（已保存的 hook/scenes/cta）
- 分析维度：
  - Hook 类型（痛点型 / 数字型 / 悬念型 / 对比型）
  - 卖点排序逻辑
  - CTA 方式
  - 节奏（每个 scene 时长分布）
- 输出：结构化拆解报告 + 可复用的脚本模板

#### 14.3 批量生成新视频
- 基于拆解模板，自动变换：
  - 开头 Hook 措辞（3-5 个变体）
  - 卖点顺序重排
  - CTA 变体
- 调用现有视频生成流水线（批量处理模块）
- 生成 3-5 条新视频

#### 14.4 优化发出方式（可配置）

| 模式 | 行为 |
|------|------|
| **人工确认模式** | 生成完成后，在优化队列页面展示，需人工点击「确认投放」后才创建广告 |
| **全自动模式** | 生成完成后直接调用 TikTok Ads API 创建广告并投放 |

- 优化队列页面（`static/optimization.html`）：显示待投放素材、预估成本、拆解来源、操作按钮

---

### Phase 15：全自动调度器

#### 15.1 定时任务（APScheduler）

| 任务 | 默认周期 | 可配置 |
|------|---------|--------|
| 拉取广告数据 | 每 6 小时 | ✅ |
| 评估广告表现（扩/缩/暂停） | 每 24 小时 | ✅ |
| 检查阶段切换条件 | 每 24 小时 | ✅ |
| 触发爆款复制优化循环 | 每 3 天 | ✅ |

#### 15.2 预算自动调节规则

```
if ROAS >= 目标值 × 1.5:
    预算 × 1.3（上调 30%）
elif ROAS >= 目标值:
    预算不变
elif ROAS >= 目标值 × 0.7:
    预算 × 0.8（下调 20%）
else:
    暂停广告
```

#### 15.3 爆品期自动扩量
- 进入爆品期后，每 24 小时评估：
  - 日消耗未达预算上限 → 提高出价
  - 日消耗达到预算上限 → 提高预算上限（增量可配置）

#### 15.4 操作日志
- 每次自动决策（扩量/缩量/暂停/切阶段/触发优化）均记录：
  - 时间、触发原因、执行动作、执行前后数值

---

## 五、新增技术架构

```
src/
├── tiktok_ads_client.py      # TikTok Marketing API 封装
├── chuhaijiang_client.py     # 出海匠 API 封装
├── campaign_manager.py       # Campaign 全生命周期管理
├── performance_monitor.py    # 数据采集与异常告警
├── optimization_engine.py    # 爆款拆解 + 新视频生成触发
├── scheduler.py              # APScheduler 调度任务
└── database.py               # 新增 5 张数据表（扩展）

static/
├── campaigns.html            # 广告管理后台
├── analytics.html            # 数据看板
└── optimization.html         # 优化队列（人工确认界面）
```

### 新增数据库表

| 表名 | 字段 | 说明 |
|------|------|------|
| `campaigns` | campaign_id, name, stage, status, target_roas, daily_budget | TikTok Campaign 记录 |
| `ad_groups` | adgroup_id, campaign_id, targeting, bid_type, bid_price | Ad Group 记录 |
| `ads` | ad_id, adgroup_id, job_id, status, created_at | 单条广告（绑定视频） |
| `performance_daily` | ad_id, date, impressions, clicks, spend, conversions, roas, ctr | 每日数据快照 |
| `optimization_queue` | id, source_ad_id, new_batch_id, status, mode, created_at | 优化队列（待确认/已投放）|

---

## 六、API 依赖清单

| API | 用途 | 申请状态 |
|-----|------|---------|
| TikTok Marketing API | 广告创建、管理、报表 | ⏳ 待申请 |
| 出海匠 API | 多账号视频发布 | ⏳ 待申请 |
| OpenAI GPT-4o | 脚本拆解、生成（现有） | ✅ 现有 |
| 豆包 Seedance / Creatok | 视频生成（现有） | ✅ 现有 |

### TikTok Marketing API 申请步骤
1. 登录 TikTok for Business：https://business.tiktok.com
2. 进入「开发者」→「创建应用」
3. 申请权限：`ad.read`、`ad.write`、`report.read`
4. 获取 App ID + App Secret，配置 OAuth 回调地址

---

## 七、开发阶段计划

| 阶段 | 内容 | 优先级 | 预估工时 |
|------|------|--------|---------|
| Phase 12 | 出海匠 + TikTok Ads API 投放集成 | P0 | 20h |
| Phase 13 | 数据采集 + 看板 | P0 | 12h |
| Phase 14 | 智能优化引擎 + 优化队列 | P1 | 16h |
| Phase 15 | 全自动调度器 | P1 | 10h |
| **合计** | | | **~58h** |

**前置条件（开发启动前必须完成）：**
- [ ] TikTok Marketing API 开发者权限申请完成，获得 App ID + Secret
- [ ] 出海匠 API Key 申请完成，获取接口文档
- [ ] 确认 TikTok 广告账户 ID（Advertiser ID）
- [ ] 各阶段切换阈值敲定（如：初期→热度期的曝光量阈值、热度期→爆品期的 ROAS 阈值）

---

## 八、整体里程碑

```
现在（已完成）：视频生成 MVP，含批量处理、历史记录、AI 卖点建议
     ↓
Step 1（API 申请期）：申请 TikTok Marketing API + 出海匠 API
     ↓
Step 2（Phase 12）：接通两个投放轨道，能手动发布广告
     ↓
Step 3（Phase 13）：数据回流，看板可查
     ↓
Step 4（Phase 14）：优化引擎上线，人工确认模式先跑
     ↓
Step 5（Phase 15）：全自动调度上线，实现完整闭环
     ↓
终态：AIGC 广告自动化闭环系统，全程无需人工干预
```

---

*PRD Version 2.0 — 2026-02-21*
*覆盖范围：Phase 12–15（广告投放 + 数据监控 + 智能优化 + 全自动调度）*
