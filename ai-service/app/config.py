from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: Literal["dev", "prod"] = "dev"
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"

    # WHY 火山方舟统一入口:DESIGN §4.2/§4.3 原方案要分别接 DeepSeek 直连 + 火山豆包,
    # 但 2026-06 起火山方舟内已托管 DeepSeek-V3.2,1 份 key 同时调通 L0/L2/Embedding/Vision,
    # 简化为单一 vendor 路径,运维少 1 个账号、计费统一
    llm_mode: Literal["mock", "live"] = "mock"
    doubao_api_key: str = ""
    doubao_base_url: str = "https://ark.cn-beijing.volces.com/api/v3"

    # WHY 用 endpoint ID 而非模型友好名:火山方舟「在线推理」是项目级资源,
    # 不同租户的同一模型有不同 ID,请求体的 model 字段必须填 ID(ep-xxxxxx)
    # 从火山控制台「在线推理」→ 推理接入点列表拷贝
    doubao_lite_endpoint: str = ""
    deepseek_endpoint: str = ""
    doubao_embedding_endpoint: str = ""
    doubao_vision_endpoint: str = ""

    # Provider 抽象层(DESIGN §2.3):本地 vs API 通过 env 切换,业务代码经工厂方法获取
    embedding_provider: Literal["mock", "local_bge_m3", "doubao"] = "local_bge_m3"
    reranker_provider: Literal["mock", "local_bge_reranker", "volc"] = "local_bge_reranker"
    ocr_provider: Literal["mock", "local_paddleocr", "baidu", "aliyun", "doubao"] = "local_paddleocr"

    baidu_ocr_api_key: str = ""
    baidu_ocr_secret_key: str = ""
    volc_reranker_api_key: str = ""
    volc_reranker_base_url: str = "https://ark.cn-beijing.volces.com/api/v3"

    qdrant_url: str = "http://qdrant:6333"
    qdrant_api_key: str = ""

    mysql_host: str = "mysql"
    mysql_port: int = 3306
    mysql_user: str = "meikai"
    mysql_password: str = ""
    mysql_db: str = "meikai"

    backend_internal_url: str = "http://backend:3001"

    langfuse_host: str = "https://cloud.langfuse.com"
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""

    allowed_origins: str = "https://www.meikaizs.com"
    max_upload_mb: int = 20
    max_concurrent_sessions: int = 8
    memory_degrade_mb: int = 400

    # WHY 营销折扣系数:DESIGN §7 产品规则——本系统是宣传用 AI 客服,展示价低于真实历史
    # 价,用引流价吸引用户留资,精确报价由销售接洽时谈定。
    # 与历史数据(quote_stats.json)解耦:Guardrail 输出侧仍以原始数据校验合理性,
    # 营销策略变更只需改本系数,不需重灌数据。
    # 建议范围 0.85-0.95;< 0.8 失真,> 0.95 引流效果弱。
    quote_display_factor: float = 0.9

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
