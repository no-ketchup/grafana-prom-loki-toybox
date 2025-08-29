import os
from locust import HttpUser, task, between

WAIT_MIN = float(os.getenv("LOCUST_WAIT_MIN", "0.1"))
WAIT_MAX = float(os.getenv("LOCUST_WAIT_MAX", "0.5"))

class ToyboxUser(HttpUser):
    # Locust will use LOCUST_HOST env (set in compose) or the UI field
    wait_time = between(WAIT_MIN, WAIT_MAX)

    @task(5)
    def root(self):
        # name shows as "GET /" in UI regardless of query params, etc.
        with self.client.get("/", name="GET /", timeout=5, catch_response=True) as r:
            if r.status_code >= 500:
                r.failure("server error")

    @task(1)
    def work(self):
        self.client.get("/work", name="GET /work", timeout=5)
