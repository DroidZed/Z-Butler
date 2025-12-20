FROM python:3.12-buster as builder

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src ./src
COPY logs ./logs

ENTRYPOINT ["python", "./src/app.py"]
