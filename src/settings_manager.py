"""
动态配置管理模块
优先级：SQLite DB > .env > SETTING_DEFS 默认值
"""
import os
from typing import Dict, Any

from . import database as db

# ── 配置定义 ────────────────────────────────────────────────────────────────

SETTING_DEFS: Dict[str, Dict[str, Any]] = {
    # AI 生成
    "openai_api_key": {
        "label": "OpenAI API Key",
        "group": "AI 生成",
        "secret": True,
        "default": "",
    },
    "ark_api_key": {
        "label": "ARK API Key（Seedance）",
        "group": "AI 生成",
        "secret": True,
        "default": "",
    },
    "creatok_api_key": {
        "label": "Creatok API Key",
        "group": "AI 生成",
        "secret": True,
        "default": "",
    },
    # TikTok 广告
    "tiktok_app_id": {
        "label": "TikTok App ID",
        "group": "TikTok 广告",
        "secret": False,
        "default": "",
    },
    "tiktok_app_secret": {
        "label": "TikTok App Secret",
        "group": "TikTok 广告",
        "secret": True,
        "default": "",
    },
    "tiktok_advertiser_id": {
        "label": "Advertiser ID",
        "group": "TikTok 广告",
        "secret": False,
        "default": "",
    },
    "tiktok_access_token": {
        "label": "Access Token",
        "group": "TikTok 广告",
        "secret": True,
        "default": "",
    },
    # 出海匠
    "chuhaijiang_api_key": {
        "label": "出海匠 API Key",
        "group": "出海匠",
        "secret": True,
        "default": "",
    },
    "chuhaijiang_accounts": {
        "label": "账号列表（每行一个）",
        "group": "出海匠",
        "secret": False,
        "multiline": True,
        "default": "",
    },
    # 广告策略
    "target_roas": {
        "label": "目标 ROAS",
        "group": "广告策略",
        "secret": False,
        "default": "2.0",
    },
    "stage_growth_impressions": {
        "label": "初期→热度期曝光阈值",
        "group": "广告策略",
        "secret": False,
        "default": "50000",
    },
    "stage_peak_roas_days": {
        "label": "热度期→爆品期持续天数",
        "group": "广告策略",
        "secret": False,
        "default": "3",
    },
    "roas_pause_threshold": {
        "label": "暂停广告 ROAS 阈值（低于目标的比例）",
        "group": "广告策略",
        "secret": False,
        "default": "0.5",
    },
    # 优化引擎
    "optimization_cycle_days": {
        "label": "优化循环周期（天）",
        "group": "优化引擎",
        "secret": False,
        "default": "3",
    },
    "optimization_mode": {
        "label": "发布模式",
        "group": "优化引擎",
        "secret": False,
        "default": "manual",
        "options": ["manual", "auto"],
    },
    "optimization_video_count": {
        "label": "每次生成新视频数",
        "group": "优化引擎",
        "secret": False,
        "default": "3",
    },
}

# env 变量名映射（DB key → env key）
_ENV_MAP = {
    "openai_api_key": "OPENAI_API_KEY",
    "ark_api_key": "ARK_API_KEY",
    "creatok_api_key": "CREATOK_API_KEY",
}

# ── 掩码工具 ─────────────────────────────────────────────────────────────────

def _mask(value: str) -> str:
    """将敏感值掩码显示，只保留前 4 个字符"""
    if not value:
        return ""
    if len(value) <= 4:
        return "*" * len(value)
    return value[:4] + "*" * min(len(value) - 4, 20)


# ── 核心读写 ─────────────────────────────────────────────────────────────────

def get(key: str) -> str:
    """读取配置：DB → .env → SETTING_DEFS 默认值"""
    # 1. 数据库
    db_val = db.get_setting(key)
    if db_val is not None and db_val != "":
        return db_val

    # 2. 环境变量
    env_key = _ENV_MAP.get(key)
    if env_key:
        env_val = os.environ.get(env_key, "")
        if env_val:
            return env_val

    # 3. 默认值
    return SETTING_DEFS.get(key, {}).get("default", "")


def set(key: str, value: str) -> None:
    """写入配置到数据库，同步更新 config.settings 属性（向后兼容）"""
    db.set_setting(key, value)
    _sync_to_config(key, value)


def get_all(mask_secrets: bool = True) -> Dict[str, Any]:
    """
    获取所有配置项（含当前值）。
    mask_secrets=True 时，secret 字段返回掩码值（供前端显示）。
    返回结构：{key: {"label", "group", "secret", "value", ...}}
    """
    db_vals = db.list_settings()
    result = {}
    for key, defn in SETTING_DEFS.items():
        raw = db_vals.get(key)
        if raw is None or raw == "":
            env_key = _ENV_MAP.get(key)
            raw = (os.environ.get(env_key, "") if env_key else "") or defn.get("default", "")

        display_val = _mask(raw) if (mask_secrets and defn.get("secret") and raw) else raw

        entry = {
            "label": defn["label"],
            "group": defn["group"],
            "secret": defn.get("secret", False),
            "multiline": defn.get("multiline", False),
            "default": defn.get("default", ""),
            "value": display_val,
            "has_value": bool(raw),
        }
        if "options" in defn:
            entry["options"] = defn["options"]
        result[key] = entry
    return result


def get_all_raw() -> Dict[str, str]:
    """获取所有配置的原始值（供内部使用）"""
    db_vals = db.list_settings()
    result = {}
    for key, defn in SETTING_DEFS.items():
        raw = db_vals.get(key)
        if raw is None or raw == "":
            env_key = _ENV_MAP.get(key)
            raw = (os.environ.get(env_key, "") if env_key else "") or defn.get("default", "")
        result[key] = raw
    return result


def get_groups() -> list:
    """返回按 group 分组的配置定义列表（供前端渲染表单）"""
    groups: Dict[str, list] = {}
    db_vals = db.list_settings()

    for key, defn in SETTING_DEFS.items():
        group_name = defn["group"]
        if group_name not in groups:
            groups[group_name] = []

        raw = db_vals.get(key)
        if raw is None or raw == "":
            env_key = _ENV_MAP.get(key)
            raw = (os.environ.get(env_key, "") if env_key else "") or defn.get("default", "")

        display_val = _mask(raw) if (defn.get("secret") and raw) else raw

        entry = {
            "key": key,
            "label": defn["label"],
            "secret": defn.get("secret", False),
            "multiline": defn.get("multiline", False),
            "default": defn.get("default", ""),
            "value": display_val,
            "has_value": bool(raw),
        }
        if "options" in defn:
            entry["options"] = defn["options"]
        groups[group_name].append(entry)

    return [{"group": g, "items": items} for g, items in groups.items()]


# ── 向后兼容：同步写入 config.settings ──────────────────────────────────────

def _sync_to_config(key: str, value: str) -> None:
    """将配置值写入 config.settings 对象，保持旧代码兼容"""
    try:
        from .config import settings
        attr_map = {
            "openai_api_key": "openai_api_key",
            "ark_api_key": "ark_api_key",
            "creatok_api_key": "creatok_api_key",
        }
        attr = attr_map.get(key)
        if attr and hasattr(settings, attr):
            setattr(settings, attr, value)
    except Exception:
        pass


def load_into_config() -> None:
    """启动时将 DB 中所有配置加载到 config.settings（向后兼容）"""
    try:
        from .config import settings
        attr_map = {
            "openai_api_key": "openai_api_key",
            "ark_api_key": "ark_api_key",
            "creatok_api_key": "creatok_api_key",
        }
        for key, attr in attr_map.items():
            val = get(key)
            if val and hasattr(settings, attr):
                setattr(settings, attr, val)
    except Exception:
        pass
