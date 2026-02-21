"""
竞品分析模块
功能：
1. AI 卖点建议 — 根据产品名称 + 已有卖点，用 GPT-4o 补充/优化卖点
2. 竞品文案分析 — 输入竞品视频的文案/标题，AI 提取可借鉴的卖点
"""
from typing import List, Optional

from openai import OpenAI

from .config import settings
from .utils import parse_json_response


def _client() -> OpenAI:
    return OpenAI(api_key=settings.openai_api_key)


# ── 1. AI 卖点建议 ────────────────────────────────────────────


def suggest_selling_points(
    product_name: str,
    existing_points: Optional[List[str]] = None,
    product_description: str = "",
) -> dict:
    """
    根据产品信息，用 GPT-4o 生成/补充卖点建议

    Args:
        product_name: 产品名称
        existing_points: 已有卖点（可为空）
        product_description: 产品描述（可选）

    Returns:
        {
            "status": "success" | "error",
            "suggestions": ["卖点1", "卖点2", ...],
            "reason": "...",   # status=error 时
        }
    """
    if not settings.openai_api_key:
        return {
            "status": "error",
            "reason": "未配置 OPENAI_API_KEY",
            "suggestions": [],
        }

    existing_text = ""
    if existing_points:
        existing_text = "\n已有卖点：\n" + "\n".join(f"- {p}" for p in existing_points)

    desc_text = f"\n产品描述：{product_description}" if product_description else ""

    prompt = f"""你是一位 TikTok 带货文案专家，擅长为跨境电商产品提炼爆款卖点。

产品名称：{product_name}{desc_text}{existing_text}

请为这个产品生成 5-8 个简洁有力的核心卖点，格式要求：
- 每个卖点 10 字以内
- 突出功能价值、解决痛点、情感共鸣
- 适合 TikTok 短视频呈现
- 避免重复已有卖点

请以 JSON 格式返回：
{{
  "suggestions": ["卖点1", "卖点2", ...]
}}"""

    try:
        resp = _client().chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=512,
        )
        text = resp.choices[0].message.content or ""
        data = parse_json_response(text)

        if isinstance(data, dict) and "suggestions" in data:
            suggestions = [s.strip() for s in data["suggestions"] if s.strip()]
            return {"status": "success", "suggestions": suggestions}
        else:
            # 解析失败，尝试提取纯文本行
            lines = [
                line.lstrip("•-0123456789. ").strip()
                for line in text.splitlines()
                if line.strip() and not line.strip().startswith("{")
            ]
            suggestions = [l for l in lines if 2 < len(l) <= 30][:8]
            return {"status": "success", "suggestions": suggestions}

    except Exception as e:
        return {"status": "error", "reason": str(e), "suggestions": []}


# ── 2. 竞品文案分析 ───────────────────────────────────────────


def analyze_competitor_text(competitor_text: str) -> dict:
    """
    分析竞品视频文案，提取可借鉴的卖点和表达方式

    Args:
        competitor_text: 竞品文案（标题 / 描述 / 评论等）

    Returns:
        {
            "status": "success" | "error",
            "selling_points": ["卖点1", ...],
            "hook_ideas": ["开头钩子1", ...],
            "summary": "分析摘要",
        }
    """
    if not settings.openai_api_key:
        return {
            "status": "error",
            "reason": "未配置 OPENAI_API_KEY",
            "selling_points": [],
            "hook_ideas": [],
            "summary": "",
        }

    if not competitor_text or not competitor_text.strip():
        return {
            "status": "error",
            "reason": "竞品文案不能为空",
            "selling_points": [],
            "hook_ideas": [],
            "summary": "",
        }

    prompt = f"""你是一位 TikTok 带货策略师，擅长分析爆款视频并提炼可复用的营销策略。

以下是竞品视频的文案内容：
---
{competitor_text[:2000]}
---

请分析这段文案，以 JSON 格式返回：
{{
  "selling_points": ["核心卖点1", "核心卖点2", ...],
  "hook_ideas": ["吸引眼球的开头钩子1", "开头钩子2", ...],
  "summary": "一句话总结这段文案的核心卖点策略"
}}

要求：
- selling_points：提取 3-6 个核心卖点（每条 15 字以内）
- hook_ideas：生成 2-3 个可借鉴的开头钩子句式
- summary：不超过 30 字"""

    try:
        resp = _client().chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=512,
        )
        text = resp.choices[0].message.content or ""
        data = parse_json_response(text)

        if isinstance(data, dict):
            return {
                "status": "success",
                "selling_points": data.get("selling_points", []),
                "hook_ideas": data.get("hook_ideas", []),
                "summary": data.get("summary", ""),
            }
        else:
            return {
                "status": "error",
                "reason": "GPT 返回格式异常",
                "selling_points": [],
                "hook_ideas": [],
                "summary": "",
            }

    except Exception as e:
        return {
            "status": "error",
            "reason": str(e),
            "selling_points": [],
            "hook_ideas": [],
            "summary": "",
        }
