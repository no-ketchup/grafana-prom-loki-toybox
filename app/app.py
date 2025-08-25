import os, random, time, logging
from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
logging.basicConfig(level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s")

REQS = Counter("app_requests_total", "Total requests", ["route","status"])
LAT  = Histogram("app_request_seconds", "Request latency (s)", ["route"])

CHAOS   = os.getenv("CHAOS","0") == "1"
SLOW_MS = int(os.getenv("SLOW_MS","0"))
NOISE   = os.getenv("LOG_NOISE","1") == "1"

def maybe_slow():
    if SLOW_MS > 0:
        time.sleep(random.randint(0, SLOW_MS)/1000.0)

@app.get("/")
def root():
    with LAT.labels("/").time():
        maybe_slow()
        if CHAOS and random.random() < 0.15:
            REQS.labels("/","500").inc()
            app.logger.error("random 500 triggered")
            return jsonify({"ok": False, "error": "chaos"}), 500
        REQS.labels("/","200").inc()
        if NOISE and random.random() < 0.3:
            app.logger.info("processing request normally")
        return jsonify({"ok": True})

@app.get("/work")
def work():
    with LAT.labels("/work").time():
        maybe_slow()
        REQS.labels("/work","200").inc()
        if NOISE:
            app.logger.warning("background job completed with warnings")
        return "done\n", 200

@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
