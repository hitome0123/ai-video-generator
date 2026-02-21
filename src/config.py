"""
配置管理模块
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""

    # API Keys
    openai_api_key: str = ""
    creatok_api_key: str = ""
    creatok_api_url: str = "https://api.creatok.ai/v1"

    # 豆包 Seedance（火山引擎 ARK）
    ark_api_key: str = ""
    seedance_model_id: str = "doubao-seedance-1-0-lite-i2v-250428"
    seedance_api_url: str = "https://ark.cn-beijing.volces.com/api/v3"

    # 路径配置
    output_dir: Path = Path("./output")
    temp_dir: Path = Path("./temp")

    # 服务配置
    host: str = "0.0.0.0"
    port: int = 8000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 创建全局配置实例
settings = Settings()

# 确保目录存在
settings.output_dir.mkdir(parents=True, exist_ok=True)
settings.temp_dir.mkdir(parents=True, exist_ok=True)
