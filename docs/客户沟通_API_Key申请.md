# 客户沟通 - API Key 申请话术

---

## 📱 版本 1: 精简版（推荐 - 微信/短信用）

```
您好！

TikTok 视频生成系统的 MVP 已经开发完成 ✅

现在需要您提供 2 个 API Key 进行测试：

1️⃣ OpenAI API Key（图片生成 + 脚本生成）
   - 获取：https://platform.openai.com/api-keys
   - 成本：约 $0.11/个视频

2️⃣ Creatok API Key（视频生成）
   - 获取：https://www.creatok.ai/
   - 成本：约 $0.20/个视频

总计：单个视频成本约 $0.31（约 2 元人民币）

提供后我马上测试，预计 1 小时内出第一个成品视频给您看效果。

需要详细申请步骤吗？我可以发给您。
```

---

## 📧 版本 2: 详细版（邮件/正式沟通用）

```
【项目进度更新】TikTok 视频生成系统 - MVP 完成

您好！

很高兴地通知您，**AI TikTok 视频生成系统的 MVP 版本已开发完成**。

✅ 已实现功能：
- 产品图片自动处理（AI 抠图 + 白底图生成）
- 智能视频脚本生成（根据卖点自动编写）
- AI 视频生成（9:16 竖版，15-30秒）
- 一键执行完整流程

📋 当前进度：代码完成 ✅  |  测试待进行 ⏳

为了进行端到端测试，需要您提供以下 API Key：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔑 需要的 API Key（2个）

1. **OpenAI API Key**
   - 用途：AI 图片处理 + 视频脚本生成
   - 获取地址：https://platform.openai.com/api-keys
   - 单视频成本：约 $0.11
   - 备注：如果您已有 ChatGPT Plus 账号，用同一账号登录即可

2. **Creatok API Key**
   - 用途：AI 视频生成（核心功能）
   - 获取地址：https://www.creatok.ai/
   - 单视频成本：约 $0.20
   - 备注：新用户可能有试用额度

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💰 成本估算

| 项目 | 单价 | 10个视频 | 100个视频 |
|------|------|----------|-----------|
| 单视频成本 | $0.31 | $3.1 | $31 |
| 人民币 | ¥2.2 | ¥22 | ¥220 |

测试阶段建议：充值 $10-20 即可（够生成 30-60 个视频）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 下一步安排

收到 API Key 后：
1. 配置测试环境（10分钟）
2. 使用您的智能手表产品图测试（30分钟）
3. 发送第一个成品视频给您验收
4. 根据效果调整优化

预计 1 小时内可以看到第一个视频成果。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ 需要帮助吗？

如果申请过程有任何问题，我可以提供：
- 详细的申请步骤（带截图）
- 充值指南
- 常见问题解答

期待您的反馈！
```

---

## 🛠️ 版本 3: 技术版（客户懂技术的话用这个）

```
Hi,

ai-video-generator MVP 已完成开发并提交到 Git。

技术栈：
- GPT-4V (产品分析)
- DALL·E 3 (白底图生成, 1024x1792)
- GPT-4 (视频脚本生成)
- Creatok API (视频生成)

现需要 2 个 API Key 进行集成测试：

1. OPENAI_API_KEY
   - 获取：https://platform.openai.com/api-keys
   - Scope: gpt-4o, dall-e-3
   - 估算：$0.11/video

2. CREATOK_API_KEY
   - 获取：https://www.creatok.ai/
   - 估算：$0.20/video

配置后执行：
```bash
export OPENAI_API_KEY=sk-xxx
export CREATOK_API_KEY=xxx
python main.py product.jpg "Product Name" "Feature 1" "Feature 2"
```

输出：
- output/product/processed/white_bg.png (DALL·E 生成)
- output/product/script.json (GPT-4 脚本)
- output/product/Product_Name.mp4 (Creatok 视频)

预计 1h 内完成首次测试。

GitHub Repo: (如果推送了可以提供)
```

---

## 📎 附件：详细申请步骤

### OpenAI API Key 申请（3 分钟）

```
步骤 1: 访问 https://platform.openai.com/api-keys
步骤 2: 登录您的 OpenAI 账号（如果没有则注册）
步骤 3: 点击 "Create new secret key"
步骤 4: 复制 API Key（格式：sk-proj-xxxxx）
步骤 5: 发给我

注意：
- API Key 只显示一次，请妥善保存
- 建议充值 $10-20 用于测试
- 如果之前用过 ChatGPT Plus，用同一账号即可
```

### Creatok API Key 申请（5 分钟）

```
步骤 1: 访问 https://www.creatok.ai/
步骤 2: 注册账号（邮箱注册）
步骤 3: 进入 Dashboard 或 Settings
步骤 4: 找到 "API Keys" 或 "Developer" 菜单
步骤 5: 创建 API Key
步骤 6: 复制并发给我

注意：
- Creatok 可能需要企业认证或付费账号
- 如果无法申请，我们有备选方案（使用其他视频生成 API）
```

---

## 🔄 备选方案（如果 Creatok 申请困难）

如果 Creatok API 无法获取，我们可以切换到：

| 备选方案 | 优势 | 劣势 |
|---------|------|------|
| **Sora API** | 质量最高 | 需要 ChatGPT Plus，等待名单 |
| **Runway Gen-2** | 质量好，易申请 | 价格稍高（$0.35/视频） |
| **Pika Labs** | 价格低（$0.1/视频） | 质量一般 |

如果需要切换，请告知，我 30 分钟内可以调整代码。

---

## 💡 常见问题

### Q1: 为什么需要我提供 API Key？
**A**: 这些是第三方 AI 服务（OpenAI、Creatok），需要您自己的账号和额度。这样成本透明，您可以随时查看用量。

### Q2: API Key 安全吗？
**A**: 非常安全。只在本地服务器使用，不会上传到任何地方。测试完成后您可以随时删除。

### Q3: 充值多少合适？
**A**: 测试阶段建议：
- OpenAI: $10（够生成 90+ 个视频）
- Creatok: $10（够生成 50 个视频）

### Q4: 可以先看效果再充值吗？
**A**: Creatok 可能有免费试用额度，OpenAI 新用户也有 $5 赠金。可以先用免费额度测试 2-3 个视频看效果。

### Q5: 如果不满意怎么办？
**A**: 测试阶段只生成 1-2 个视频（成本约 $1），看效果后再决定是否继续。不满意的话成本很低。

---

**建议使用**:
- 如果客户关系好/时间紧急 → 用**版本 1（精简版）**
- 如果需要正式沟通 → 用**版本 2（详细版）**
- 如果客户是技术人员 → 用**版本 3（技术版）**

需要我调整话术吗？或者帮你合并几个版本？
