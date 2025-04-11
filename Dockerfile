FROM python:3.11

SHELL ["/bin/bash", "-c"]

RUN pip install --upgrade pip
RUN pip install --upgrade poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

RUN poetry show uvicorn

CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
