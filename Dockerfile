FROM archlinux:latest

RUN pacman -Syu --noconfirm && \
    pacman -S --noconfirm python python-pip gifski && \
    pacman -Scc --noconfirm

WORKDIR /bot

COPY requirements.txt .
RUN python -m venv /bot/venv && \
    /bot/venv/bin/pip install --upgrade pip && \
    /bot/venv/bin/pip install --no-cache-dir -r requirements.txt

COPY resources/ .
COPY *.py .
COPY rusty-sussy/target/release/rusty-sussy .


ENTRYPOINT ["/bot/venv/bin/python", "bone-bot.py"]