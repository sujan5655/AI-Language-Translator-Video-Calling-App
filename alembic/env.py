from logging.config import fileConfig

import os
import sys

from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context


# ============================================================
# ADD SRC TO PYTHON PATH
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
    )
)


SRC_DIR = os.path.join(
    BASE_DIR,
    "src",
)

sys.path.insert(0, SRC_DIR)


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(
    os.path.join(
        BASE_DIR,
        ".env",
    )
)


# ============================================================
# ALEMBIC CONFIG
# ============================================================

config = context.config


# ============================================================
# DATABASE URL
# ============================================================

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is missing from .env"
    )

config.set_main_option(
    "sqlalchemy.url",
    DATABASE_URL,
)

# ============================================================
# LOGGING
# ============================================================

if config.config_file_name is not None:
    fileConfig(
        config.config_file_name
    )


# ============================================================
# IMPORT SQLALCHEMY MODELS
# ============================================================

from video_calling_app.database import Base
from video_calling_app import models


target_metadata = Base.metadata


# ============================================================
# OFFLINE MIGRATIONS
# ============================================================

def run_migrations_offline() -> None:

    url = config.get_main_option(
        "sqlalchemy.url"
    )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
    )

    with context.begin_transaction():
        context.run_migrations()


# ============================================================
# ONLINE MIGRATIONS
# ============================================================

def run_migrations_online() -> None:

    connectable = engine_from_config(
        config.get_section(
            config.config_ini_section,
            {},
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


# ============================================================
# RUN
# ============================================================

if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()