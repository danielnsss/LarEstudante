
import os

from alembic import context
from sqlalchemy import create_engine, pool

from app.database.base import Base
from app.modules.usuarios import models as usuarios_models
from app.modules.republicas import models as republicas_models

config = context.config

target_metadata = Base.metadata


def run_migrations_offline():
    url = os.environ["DATABASE_URL"]

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    engine = create_engine(
        os.environ["DATABASE_URL"],
        poolclass=pool.NullPool
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True
        )

        with context.begin_transaction():
            context.run_migrations()

    engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
