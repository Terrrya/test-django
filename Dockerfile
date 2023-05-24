FROM python:3.11.2-slim-buster

LABEL maintainer="denys.tereshchuk.dev@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR app/

RUN apt-get update

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8232"]
