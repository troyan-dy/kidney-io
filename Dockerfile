FROM python:3.9 as requirements-builder

RUN mkdir build/
WORKDIR /build/

RUN pip install poetry

COPY pyproject.toml poetry.lock /build/

RUN poetry export --with-credentials --without-hashes -f requirements.txt -o requirements.txt

FROM python:3.9

RUN mkdir app/
WORKDIR /app/

COPY --from=requirements-builder /build/requirements.txt /app/requirements.txt

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

RUN pip install --extra-index-url https://backend-pypi-ro:naighiejeDuiroo8viiw@nexus.zvq.me/repository/backend-pypi/simple/ -r requirements.txt

COPY kidney_io /app/kidney_io

ENV SERVICE_NAME=kidney_io

CMD ["python", "-m", "kidney_io.web"]
