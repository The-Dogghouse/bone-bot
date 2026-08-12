import os
from pathlib import Path

from loguru import logger

DOGGHOUSE_GUILD_ID = 537011097824395274
GAMING_CHANNEL_ID = 1032340389941739610

_ASYNC_SCHEMES = {
    "postgres": "postgresql+asyncpg",
    "postgresql": "postgresql+asyncpg",
}


def read_secret(name: str) -> str | None:
    path = os.environ.get(f"{name}_FILE")
    if path is None:
        logger.error(f"No secret in `{name}_FILE`: trying the {name} environment variable")
        return os.environ.get(name)

    logger.info(f"Reading `{name}` from `{path}`")
    try:
        return Path(path).read_text().strip()
    except OSError as e:
        logger.error(f"Failed reading `{name}` from `{path}`: {e}")
        return None


def database_url() -> str | None:
    url = read_secret("BONE_DATABASE_URL")
    if not url:
        return None

    scheme, separator, rest = url.partition("://")
    if not separator:
        logger.error(f"`BONE_DATABASE_URL` is not a connection URL: `{scheme}`")
        return None

    driver = _ASYNC_SCHEMES.get(scheme)
    if driver is None:
        # Already driver-qualified (or not Postgres at all), leave it be
        return url

    return f"{driver}://{rest}"
