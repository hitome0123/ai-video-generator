# 客户沟通 - API Key 申请话术

> **使用说明**：根据客户情况选择对应版本发送。
> 详细申请步骤见同目录 [API_KEY_申请指南.md](API_KEY_申请指南.md)

---

## 📱 版本 1: 精简版（推荐 - 微信/短信用）

```
您好！

TikTok 视频生成系统已全部开发完成 ✅

现在需要您提供 API Key 进行测试：

1️⃣ OpenAI API Key（图片处理 + 脚本生成）【必须】
   - 获取：https://platform.openai.com/api-keys
   - 单视频成本：约 ¥0.8

2️⃣ 视频生成 API（二选一）

   推荐 👉 豆包 Seedance（国内直连，¥0.9/视频）
   - 获取：https://console.volcengine.com/ark

   备选：Creatok（需要 VPN，¥2.2/视频）
   - 获取：https://www.creatok.ai/

合计：单个视频成本约 ¥1.7（Seedance 方案）

提供后我马上测试，很快出第一个成品视频给您看效果。

需要详细的申请步骤说明吗？我可以发给您。
```

---

## 📧 版本 2: 详细版（邮件/正式沟通用）

```
【项目进度更新】TikTok 视频生成系统 - 正式版完成

您好！

很高兴地通知您，AI TikTok 视频生成系统已全部开发完成。

✅ 已实现功能：
- 产品图片自动处理（AI 分析 + 白底图生成）
- 智能视频脚本生成（根据卖点自动编写）
- AI 视频生成（9:16 竖版，豆包 Seedance / Creatok 双引擎）
- 字幕烧录 + BGM 混音
- 历史记录（SQLite 持久化）
- AI 卖点建议 + 竞品文案分析
- 批量处理（CSV 导入，最多 20 个产品）
- 设置管理、数据分析、广告系列管理等

📋 当前进度：代码完成 ✅  |  测试待进行 ⏳

为了进行端到端测试，需要您提供以下 API Key：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔑 需要的 API Key

1. OpenAI API Key【必须】
   - 用途：AI 图片处理 + 视频脚本生成
   - 获取地址：https://platform.openai.com/api-keys
   - 单视频成本：约 ¥0.8
   - 备注：如果您已有 ChatGPT 账号，用同一账号登录即可

2. 豆包 Seedance API Key【推荐】
   - 用途：AI 视频生成（5 秒，国内直连）
   - 获取地址：https://console.volcengine.com/ark
   - 单视频成本：约 ¥0.9
   - 备注：有抖音/飞书账号可直接扫码登录

3. Creatok API Key【备选，有 Seedance 则不需要】
   - 用途：AI 视频生成（15 秒，需要 VPN）
   - 获取地址：https://www.creatok.ai/
   - 单视频成本：约 ¥2.2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 成本估算（Seedance 方案）

| 项目 | 单价 | 10个视频 | 100个视频 |
|------|------|----------|-----------|
| 单视频成本 | ¥1.7 | ¥17 | ¥170 |

测试阶段建议充值：OpenAI $10 + 豆包 Seedance ¥50，够测试 50+ 个视频

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 下一步安排

收到 API Key 后：
1. 配置测试环境
2. 使用您的产品图片进行测试
3. 发送第一个成品视频给您验收
4. 根据效果调整优化

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ 需要帮助吗？

我可以提供详细的图文申请教程（每一步都有说明），让完全不懂技术的用户也能独立完成申请。

期待您的反馈！
```

---

## 🛠️ 版本 3: 技术版（客户懂技术的话用这个）

```
Hi,

ai-video-generator 正式版已完成开发（Phase 1-13 全部完成）。

技术栈：
- GPT-4o Vision（产品分析）
- DALL·E 3（白底图生成，1024x1792）
- GPT-4o（视频脚本生成）
- 豆包 Seedance doubao-seedance-1-0-lite-i2v-250428（视频生成，推荐）
- Creatok API（视频生成，备选）
- FFmpeg（字幕烧录 + BGM 混音）
- SQLite（任务持久化）

需要以下 API Key：

1. OPENAI_API_KEY
   - 获取：https://platform.openai.com/api-keys
   - 用途：gpt-4o, dall-e-3
   - 成本：~¥0.8/video

2. ARK_API_KEY（推荐）
   - 获取：https://console.volcengine.com/ark → API Key 管理
   - 用途：doubao-seedance-1-0-lite-i2v-250428
   - 成本：~¥0.9/video

3. CREATOK_API_KEY（备选，有 ARK 则不需要）
   - 获取：https://www.creatok.ai/
   - 成本：~¥2.2/video

.env 配置：
OPENAI_API_KEY=sk-proj-xxx
ARK_API_KEY=xxx
# CREATOK_API_KEY=xxx  # 二选一

Web 启动：
python run.py
# 浏览器打开 http://localhost:8000

CLI 模式：
python main.py product.jpg "Product Name" "Feature 1" "Feature 2"

输出：
- output/<job_id>/processed/white_bg.png（DALL·E 生成）
- output/<job_id>/script.json（GPT-4o 脚本）
- output/<job_id>/Product_Name.mp4（成品视频）

GitHub: https://github.com/hitome0123/ai-video-generator
```

---

## 🔄 视频服务对比

| 项目 | 豆包 Seedance（推荐）| Creatok（备选）|
|------|---------------------|----------------|
| 视频时长 | 5 秒 | 15 秒 |
| 单次成本 | ~¥0.9 | ~¥2.2 |
| 网络要求 | 国内直连 | 需 VPN |
| 支付方式 | 支付宝 / 微信 | 国际信用卡 |

---

## 💡 常见问题

**Q1: 为什么需要我提供 API Key？**

这些是第三方 AI 服务（OpenAI、火山引擎、Creatok），需要您自己的账号和额度。这样成本完全透明，您可以随时在各平台后台查看用量，不存在二次收费。

**Q2: API Key 安全吗？**

Key 只配置在您自己的服务器上，不会上传到任何第三方。建议不要截图发到公开群里，一对一私信给我即可。

**Q3: 充值多少合适？**

测试阶段建议：
- OpenAI：$10（约 ¥73，够生成 90+ 个视频）
- 豆包 Seedance：¥50（够生成 55 个视频）

**Q4: 可以先看效果再充值吗？**

豆包 Seedance 新用户可能有赠送额度，OpenAI 新用户也有 $5 赠金，可以先用免费额度测试 2-3 个视频看效果，满意后再充值。

---

**建议使用**：
- 客户关系好 / 时间紧急 → **版本 1（精简版）**
- 需要正式沟通 → **版本 2（详细版）**
- 客户是技术人员 → **版本 3（技术版）**
- 客户要自己申请 → 发送 **[API_KEY_申请指南.md](API_KEY_申请指南.md)**
