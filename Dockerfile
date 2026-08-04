FROM archlinux:latest

RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm python python-pip uv gifski && \
    pacman -Scc --noconfirm

WORKDIR /bot

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync

# Fix the miserable default behavior of copying
# the _contents only_ of `resources/` to `/app`
COPY resources/ resources/
COPY *.py .
COPY rusty-sussy/target/release/rusty-sussy .


ENTRYPOINT ["uv", "run", "bone-bot.py"]