import os
from cachelib.file import FileSystemCache

SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY", "change-this-long-and-random")
SQLALCHEMY_DATABASE_URI = (
    f"postgresql+psycopg2://{os.getenv('SUPERSET_DB_USER','superset_user')}:"
    f"{os.getenv('SUPERSET_DB_PASS','superset_pass')}@{os.getenv('POSTGRES_HOST','postgres')}:"
    f"{os.getenv('POSTGRES_PORT','5432')}/{os.getenv('SUPERSET_DB','superset')}"
)

# Performance/recursos reduzidos
SUPERSET_WEBSERVER_WORKERS = 1
GUNICORN_TIMEOUT = 120

# Cache local simples
CACHE_CONFIG = {"CACHE_TYPE": "SimpleCache"}
DATA_CACHE_CONFIG = CACHE_CONFIG
FILTER_STATE_CACHE_CONFIG = CACHE_CONFIG
EXPLORE_FORM_DATA_CACHE_CONFIG = CACHE_CONFIG

# Desabilitar features que exigem Celery no começo
FEATURE_FLAGS = {
    "ALERT_REPORTS": False,
}
