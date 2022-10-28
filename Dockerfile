FROM python:3.11.0 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11.0

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./currency_scraper /code/currency_scraper

CMD ["uvicorn", "currency_scraper.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]

# https://fastapi.tiangolo.com/deployment/docker/