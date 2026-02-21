"""
工具函数模块
"""
import json
import re
from typing import Optional, Union


def parse_json_response(text: str) -> Optional[Union[dict, list]]:
    """
    从 GPT 响应文本中解析 JSON

    按以下顺序尝试：
    1. 直接 JSON 解析
    2. 从 markdown 代码块（```json ... ```）提取
    3. 提取第一个 JSON 对象 {...}
    4. 提取第一个 JSON 数组 [...]

    Returns:
        解析结果（dict 或 list），失败返回 None
    """
    if not text:
        return None

    text = text.strip()

    # 1. 直接解析
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. markdown 代码块
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # 3. 第一个 JSON 对象
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    # 4. 第一个 JSON 数组
    match = re.search(r"\[[\s\S]*\]", text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return None
