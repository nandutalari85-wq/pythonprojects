import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    """Base application configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "academic-crop-analysis-secret-key-2026")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 5 * 1024 * 1024))  # 5 MB upload limit
    UPLOAD_EXTENSIONS = [".csv"]
    
    # Static folders
    STATIC_DIR = BASE_DIR / "app" / "static"
    CHARTS_DIR = STATIC_DIR / "charts"
    
    # SQLAlchemy configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    @staticmethod
    def build_database_uri():
        """
        Build database URI from environment variables.
        Supports explicit DATABASE_URL, or components for MySQL.
        Falls back to local SQLite if MySQL credentials are not supplied or if USE_SQLITE is true.
        """
        # If DATABASE_URL is explicitly set, use it
        explicit_url = os.getenv("DATABASE_URL")
        if explicit_url:
            return explicit_url

        use_sqlite = os.getenv("USE_SQLITE", "false").lower() in ("true", "1", "yes")
        if use_sqlite:
            db_path = BASE_DIR / "crop_analysis.db"
            return f"sqlite:///{db_path}"

        # MySQL configuration
        db_user = os.getenv("DB_USER", "root")
        db_pass = os.getenv("DB_PASSWORD", "root")
        db_host = os.getenv("DB_HOST", "127.0.0.1")
        db_port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME", "crop_analysis_db")

        return f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = Config.build_database_uri()


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = Config.build_database_uri()


class TestingConfig(Config):
    """Testing configuration (uses in-memory SQLite for fast, isolated tests)."""
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
