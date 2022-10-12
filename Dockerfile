FROM python:3.10.6-alpine3.16
LABEL maintainer="klusowskimat@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app
WORKDIR /app

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        app-user
    
ENV PATH="/py/bin:$PATH"

USER app-user