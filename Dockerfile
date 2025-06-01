FROM python:3.13-alpine

LABEL maintainer="codeBuddha"

WORKDIR /notification-service

COPY ./ /notification-service/

RUN apk add --no-cache \
    build-base \
    libffi-dev \
    postgresql-dev \
    musl-dev \
    gcc \
    python3-dev \
    libpq \
    libc-dev \
    && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN addgroup -S jam && adduser -S jam -G jam \
    && chown -R jam:jam /notification-service \
    && chmod -R 755 /notification-service

USER jam

EXPOSE 2000
CMD ["uvicorn", "app.index:app", "--host", "0.0.0.0", "--port", "2000", "--reload"]