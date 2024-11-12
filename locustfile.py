from locust import HttpUser, TaskSet, task, between, constant_pacing

class TokenTaskSet(TaskSet):
    token = ""

    # Task for requesting a token from /token endpoint
    @task(1)
    def get_token(self):
        response = self.client.post("/token", data={
            "client_id": "devops",
            "client_secret": "devops",
            "scope": "push_send",
            "grant_type": "client_credentials"
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]

    @task(2)
    def check_token(self):
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            self.client.get("/check", headers=headers)

class TokenUser(HttpUser):
    tasks = [TokenTaskSet]
    wait_time = constant_pacing(0.1)