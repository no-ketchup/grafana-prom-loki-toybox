# Grafana + Prometheus + Loki + Alloy Toybox

 **Work in Progress**
A small local **incident lab** for experimenting with observability.

Stack includes:
- **Grafana** → dashboards & log exploration
- **Prometheus** → metrics & alerting
- **Loki** → log aggregation
- **Alloy** → scraping & log forwarding
- **Toy app** (Flask) → can simulate chaos (errors, latency, noisy logs)

---

## Requirements
- [Docker](https://docs.docker.com/get-docker/) + Docker Compose v2
- Git
- Terminal

---

## Quickstart

```bash
cd grafana-prom-loki-toybox
docker compose up -d --build
```

### Services
- Grafana → [http://localhost:3000](http://localhost:3000) (login: `admin` / `admin`)
- Prometheus → [http://localhost:9090](http://localhost:9090)
- Loki API → [http://localhost:3100](http://localhost:3100)
- Alertmanager → [http://localhost:9093](http://localhost:9093)
- Demo app → [http://localhost:8000](http://localhost:8000)

---

## Demo App Controls
Environment variables in `docker-compose.yml` let you toggle behavior:

| Variable   | Effect                          |
|------------|---------------------------------|
| `CHAOS=1`  | Random 500 errors               |
| `SLOW_MS`  | Adds up to N ms latency         |
| `LOG_NOISE`| Extra log lines for Loki        |

Apply changes by rebuilding the app:
```bash
docker compose up -d --build app
```

---

## Explore

**Metrics (Prometheus)**
```promql
rate(app_requests_total[1m])
histogram_quantile(0.95, sum(rate(app_request_seconds_bucket[5m])) by (le))
```

**Logs (Loki, in Grafana Explore)**
```
{container="app"} |= "error"
{container="app"} |~ "warning|error"
```

**Alerts**
- Example alert: high error rate in `prometheus/alerts.yml`
- Delivered via Alertmanager (stub config provided)

---

## Notes
- Configs live under `./prometheus`, `./loki`, `./alloy`, `./grafana/provisioning`
- Docker volumes persist data (`prom_data`, `loki_data`, `grafana_data`)
- **Not production-ready** — purely a local playground

---

## To-Do
- [ ] Add prebuilt Grafana dashboards for latency & error rate
- [ ] Proper Alertmanager config (Slack/email)
- [ ] Add Tempo for traces
- [ ] Add load generator service for chaos testing
- [ ] Polish app logs (structured JSON format)
- [ ] Add makefile helper targets (up, down, clean, logs)
- [ ] Write troubleshooting section

---

## License
MIT
