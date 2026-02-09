from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "SIEM Platform"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Security
    secret_key: str = "change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database (PostgreSQL)
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "siem_platform"
    database_user: str = "siem"
    database_password: str = "siem"
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"
    
    # OpenSearch
    opensearch_host: str = "localhost"
    opensearch_port: int = 9200
    opensearch_index_raw: str = "siem-raw"
    opensearch_index_security: str = "siem-security"
    opensearch_index_alerts: str = "siem-alerts"
    opensearch_index_cases: str = "siem-cases"
    
    @property
    def opensearch_url(self) -> str:
        return f"http://{self.opensearch_host}:{self.opensearch_port}"
    
    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_topics_raw: str = "siem-raw-events"
    kafka_topics_normalized: str = "siem-normalized"
    kafka_topics_alerts: str = "siem-alerts"
    
    # Redis (cache)
    redis_url: str = "redis://localhost:6379"
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
