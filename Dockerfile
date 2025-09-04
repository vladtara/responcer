
FROM python:3.13-alpine3.21 AS builder
WORKDIR /app
RUN apk update \
    && apk add --no-cache musl-dev linux-headers make automake gcc g++ subversion python3-dev \
    && rm -vrf /var/cache/apk/*
COPY . .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels .

FROM python:3.13-alpine3.21
WORKDIR /app
COPY --from=builder /app/wheels/ /tmp/wheels
RUN ls -la
RUN pip install --no-cache /tmp/wheels/* && rm -rf /tmp/wheels
EXPOSE 8000/tcp
ENTRYPOINT ["responcer"]
