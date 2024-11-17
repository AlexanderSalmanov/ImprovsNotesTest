FROM python:3.9-alpine3.13 

ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./

COPY ./core /core

WORKDIR /core
EXPOSE 8000 
RUN python -m venv /env && \
    /env/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev && \
    /env/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app

ENV PATH="/env/bin:$PATH"
USER app