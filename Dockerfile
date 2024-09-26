FROM python:3.11

RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry

WORKDIR /warehouse
COPY poetry.lock pyproject.toml /warehouse/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY . /warehouse
