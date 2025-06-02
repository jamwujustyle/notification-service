FROM python:3.13-slim

LABEL maintainer="codeBuddha"

WORKDIR /notification-service

COPY ./ /notification-service/

RUN  pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


RUN adduser --disabled-password --no-create-home --gecos "" jam  \
    && chown -R jam /notification-service \
    && chmod -R 755 /notification-service

USER jam

EXPOSE 2000
CMD ["uvicorn", "app.index:app", "--host", "0.0.0.0", "--port", "2000", "--reload"]


    # apt update && apt install -y \
    # build-essential \
    # libffi-dev \
    # libpq-dev \
    # gcc \
    # && rm -rf /var/lib/apt/lists/* \