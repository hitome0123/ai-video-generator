"""
数据库模块
功能：使用 SQLite 持久化存储任务记录，服务器重启后历史不丢失
"""
import json
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Optional, List, Dict

DB_PATH = Path(__file__).parent.parent / "data" / "jobs.db"


def _init_db(conn: sqlite3.Connection):
    """初始化数据库表结构"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id      TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            status      TEXT NOT NULL DEFAULT 'queued',
            step        INTEGER DEFAULT 0,
            step_name   TEXT DEFAULT '',
            video_service TEXT DEFAULT 'seedance',
            video_path  TEXT,
            script      TEXT,
            video_prompt TEXT,
            error       TEXT,
            add_subtitle INTEGER DEFAULT 0,
            add_bgm     INTEGER DEFAULT 0,
            created_at  REAL NOT NULL,
            updated_at  REAL NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key         TEXT PRIMARY KEY,
            value       TEXT NOT NULL DEFAULT '',
            updated_at  REAL NOT NULL
        )
    """)
    conn.commit()


@contextmanager
def get_conn():
    """数据库连接上下文管理器"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        _init_db(conn)
        yield conn
    finally:
        conn.close()


# ── CRUD 操作 ──────────────────────────────────────────────────


def create_job(
    job_id: str,
    product_name: str,
    video_service: str = "seedance",
    add_subtitle: bool = False,
    add_bgm: bool = False,
) -> None:
    """创建新任务记录"""
    now = time.time()
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO jobs (job_id, product_name, status, video_service,
                              add_subtitle, add_bgm, created_at, updated_at)
            VALUES (?, ?, 'queued', ?, ?, ?, ?, ?)
            """,
            (job_id, product_name, video_service,
             1 if add_subtitle else 0,
             1 if add_bgm else 0,
             now, now),
        )
        conn.commit()


def update_job(job_id: str, **kwargs) -> None:
    """更新任务字段（只更新传入的字段）"""
    if not kwargs:
        return

    kwargs["updated_at"] = time.time()

    # 将 script/video_prompt 序列化为 JSON 字符串
    if "script" in kwargs and isinstance(kwargs["script"], dict):
        kwargs["script"] = json.dumps(kwargs["script"], ensure_ascii=False)

    columns = ", ".join(f"{k} = ?" for k in kwargs)
    values = list(kwargs.values()) + [job_id]

    with get_conn() as conn:
        conn.execute(f"UPDATE jobs SET {columns} WHERE job_id = ?", values)
        conn.commit()


def get_job(job_id: str) -> Optional[Dict]:
    """查询单个任务"""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM jobs WHERE job_id = ?", (job_id,)
        ).fetchone()

    if row is None:
        return None

    return _row_to_dict(row)


def list_jobs(limit: int = 50) -> List[Dict]:
    """获取最近的任务列表（按创建时间倒序）"""
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ).fetchall()

    return [_row_to_dict(r) for r in rows]


def get_setting(key: str) -> Optional[str]:
    """查询单个配置项，不存在返回 None"""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT value FROM settings WHERE key = ?", (key,)
        ).fetchone()
    return row["value"] if row else None


def set_setting(key: str, value: str) -> None:
    """写入或更新配置项"""
    now = time.time()
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO settings (key, value, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at
            """,
            (key, value, now),
        )
        conn.commit()


def list_settings() -> Dict[str, str]:
    """读取全部配置，返回 {key: value} 字典"""
    with get_conn() as conn:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
    return {r["key"]: r["value"] for r in rows}


def delete_job(job_id: str) -> bool:
    """删除任务记录，返回是否删除成功"""
    with get_conn() as conn:
        cursor = conn.execute(
            "DELETE FROM jobs WHERE job_id = ?", (job_id,)
        )
        conn.commit()
        return cursor.rowcount > 0


# ── 内部工具 ───────────────────────────────────────────────────


def _row_to_dict(row: sqlite3.Row) -> Dict:
    d = dict(row)
    # 反序列化 script JSON
    if d.get("script") and isinstance(d["script"], str):
        try:
            d["script"] = json.loads(d["script"])
        except json.JSONDecodeError:
            pass
    # 布尔字段
    d["add_subtitle"] = bool(d.get("add_subtitle"))
    d["add_bgm"] = bool(d.get("add_bgm"))
    return d
