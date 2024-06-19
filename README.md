### Responcer 
<p>Service return headers from client with real ip address</p>
<p>Service available:</p>

[https://responcer.glaps.fun](https://responcer.glaps.fun)

### Using
```
docker run -it --rm -p 8000:8000 glapss/responcer:latest
```

### Endpoints

* /docs - API docs.
* /api/v1/ip - return your external IP.
* /api/v1/version - return the version of the app.
* /metrics - return metrics.
* /health - return the status of the app.