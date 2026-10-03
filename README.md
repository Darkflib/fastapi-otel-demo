# FastAPI native OpenTelemetry demo

Demonstrates FastAPI's built-in OpenTelemetry support
([docs](https://fastapi.tiangolo.com/advanced/opentelemetry/)). The app contains **no OTel code**:
the `OTEL_*` env vars in `compose.yaml` make FastAPI auto-configure OTLP exporters for traces, metrics and logs.

```bash
docker compose up --build
```

## Services

| Service | URL | Purpose |
|---|---|---|
| `app` | http://localhost:8000/docs | FastAPI app (`app/main.py`) emitting traces, metrics and logs over OTLP/HTTP |
| `collector` | http://localhost:8889/metrics | OpenTelemetry Collector: receives OTLP on 4317/4318, prints everything to stdout (`docker compose logs -f collector`), forwards traces to Jaeger, exposes metrics in Prometheus format |
| `jaeger` | http://localhost:16686 | Trace UI — pick service `fastapi-demo` |
| `prometheus` | http://localhost:9090 | Scrapes the collector's metrics endpoint every 5s |
| `grafana` | http://localhost:3000 | Provisioned "FastAPI OTel metrics" dashboard (anonymous admin access) |
| `traffic` | — | curl loop sending good, 404, 422 and 500 requests so there is data to look at |

## What the app demonstrates

- A dependency (`slow_lookup`) appears as its own span.
- A background task (`audit`) appears in the request's trace and emits a log.
- `/boom` raises an unhandled exception: error span plus exception log.
- `telemetry={"exclude": ...}` keeps `/health` out of the telemetry.

## Layout

- `app/main.py`, `Dockerfile`, `requirements.txt` — the app
- `otel-collector.yaml` — collector pipelines
- `prometheus.yaml` — scrape config
- `grafana/` — datasource and dashboard provisioning

Stop with `docker compose down`.
