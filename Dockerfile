FROM python:3.10-alpine3.16 as builder
WORKDIR /app
RUN apk update \
    && apk add --no-cache musl-dev linux-headers make automake gcc g++ subversion python3-dev \
    && rm -vrf /var/cache/apk/*
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.10-alpine3.16
WORKDIR /app
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*
COPY . .
EXPOSE 8000/tcp
ENTRYPOINT [ "uvicorn","--host", "0.0.0.0","--port", "8000"]
CMD ["main:app"]
