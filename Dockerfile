FROM python:3.12-slim

# System-Abhängigkeiten
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libgmp-dev \
    # python-ldap benötigt diese Bibliotheken zur Kompilierung
    libldap2-dev \
    libsasl2-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# uv installieren (offizieller Package Manager von helios-server)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY ./  /app/

RUN uv add "celery>=5.4,<5.5"

# Abhängigkeiten installieren (uv sync liest pyproject.toml)
RUN uv sync --no-dev \
    && uv pip install gunicorn \
    && rm -rf ~/.cache/pip

EXPOSE 8000

# Startbefehl (wird in docker-compose.yml überschrieben für worker)
CMD ["uv", "run", "gunicorn", "wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
