FROM archlinux:latest

RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm python python-pip uv gifski && \
    pacman -Scc --noconfirm

WORKDIR /bot

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --no-dev

# Fix the miserable default behavior of copying
# the _contents only_ of `resources/` to `/app`
COPY resources/ resources/
COPY migrations/ migrations/
COPY alembic.ini .
COPY *.py .
COPY rusty-sussy/target/release/rusty-sussy .


# Migrations run before the bot connects, so the schema is always current
ENTRYPOINT ["sh", "-c", "uv run --no-dev alembic upgrade head && exec uv run --no-dev bone-bot.py"]
