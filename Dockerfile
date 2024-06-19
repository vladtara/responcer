FROM python:3.11.9-alpine3.20 as builder
WORKDIR /app
RUN apk update \
    && apk add --no-cache musl-dev linux-headers make automake gcc g++ subversion python3-dev \
    && rm -vrf /var/cache/apk/*
COPY . .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels .

FROM python:3.11.9-alpine3.20 
WORKDIR /app
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels
EXPOSE 8000/tcp
ENTRYPOINT ["responcer"]
