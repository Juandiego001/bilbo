FROM ubuntu:focal
SHELL ["/bin/bash", "-c"]

# Noninteractive TZData Installation
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Bogota

# Python Packages Installation
RUN apt update && apt upgrade && apt install sudo
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends tzdata
RUN echo "deb-src http://archive.ubuntu.com/ubuntu/ focal main" >> /etc/apt/sources.list
RUN sudo apt update && sudo apt upgrade && sudo apt -y build-dep python3
RUN sudo apt -y install build-essential wget gdb lcov libbz2-dev libffi-dev libgdbm-dev libgdbm-compat-dev liblzma-dev libncurses5-dev libreadline6-dev libsqlite3-dev libssl-dev lzma lzma-dev tk-dev uuid-dev zlib1g-dev

# Python Installation
WORKDIR "/root"
RUN wget https://www.python.org/ftp/python/3.12.7/Python-3.12.7.tgz && tar -xf Python-3.12.7.tgz
WORKDIR "/root/Python-3.12.7"
RUN ./configure --enable-optimizations && sudo make install

# SQLite Installation
RUN apt-get remove -y --auto-remove sqlite3
WORKDIR "/root"
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3470200.tar.gz && tar -xf sqlite-autoconf-3470200.tar.gz
WORKDIR "/root/sqlite-autoconf-3470200"
RUN ./configure && make && make install && sqlite3 --version

# Project Installation
WORKDIR "/app"
COPY core ./core
COPY linux_requirements.txt .
COPY log.conf .
COPY run.py .

# Installing Dependencies
RUN mkdir /app/logs && \
    python3 -m venv /venv && \
    /venv/bin/pip install -U --no-cache-dir pip setuptools wheel && \
    /venv/bin/pip install --no-cache-dir nvidia-pyindex && \
    /venv/bin/pip install --no-cache-dir -r linux_requirements.txt

EXPOSE 5000

CMD ["/venv/bin/gunicorn", "run:app"]
