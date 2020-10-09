# coding: utf8

"""
alembic revision -m "first migration" --autogenerate --head head
alembic upgrade head
"""

from os import environ
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.split(dir_path)[0])

from app.configuration.settings import Setup
from app.database.models import db


config = context.config
fileConfig(config.config_file_name)

target_metadata = db
config_path = environ.get("CONFIG")
print(f"config path: {config_path}")
setup = Setup(config_path)

dt = setup.database["connect"]
url = f'postgresql://{dt["login"]}:{dt["password"]}@{dt["host"]}/{dt["name"]}'


def run_migrations_offline():
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=False,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    config_dict = config.get_section(config.config_ini_section)
    config_dict['sqlalchemy.url'] = url

    connectable = engine_from_config(
        config_dict,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
