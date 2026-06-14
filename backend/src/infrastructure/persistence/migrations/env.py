import sys
from pathlib import Path

from sqlalchemy import engine_from_config, pool
from sqlalchemy.engine import Connection
from alembic import context
from loguru import logger

project_root = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(project_root / "backend"))

from src.settings import Settings
from src.infrastructure.persistence.models import Base

settings = Settings()
config = context.config


target_metadata = Base.metadata

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO",
)


def run_migrations_offline() -> None:
    url = settings.database.url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True,
    )

    logger.info("Running migrations in offline mode")
    with context.begin_transaction():
        context.run_migrations()
    logger.info("Offline migrations completed successfully")


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        render_as_batch=True,
        include_schemas=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = settings.database.url

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    logger.info(f"Connecting to database: {settings.database.host}")

    with connectable.connect() as connection:
        do_run_migrations(connection)

    connectable.dispose()
    logger.info("Migrations completed successfully")


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
