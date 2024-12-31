FROM python:3.12.8-alpine

WORKDIR /app

COPY core/ .
COPY linux_requirements.txt .
COPY log.conf .
COPY run.py .

RUN mkdir /app/logs && \
    python -m venv /venv && \
    /venv/bin/pip install -U pip && \
    /venv/bin/pip install wheel && \
    /venv/bin/pip install nvidia-pyindex && \
    /venv/bin/pip install -r linux_requirements.txt

EXPOSE 5000

CMD ["/venv/bin/gunicorn", "run:app"]
