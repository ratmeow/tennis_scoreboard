FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV  PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir poetry>=1.6.1 \
    && poetry config virtualenvs.create false \
    && poetry config installer.parallel false

WORKDIR /tennis_score
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY src src
COPY migrations migrations
COPY alembic.ini main.py ./

CMD ["sh", "-c", "alembic upgrade head && python main.py"]