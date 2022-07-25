from locust import HttpUser, task, between
from faker import Faker


class PerformanceTests(HttpUser):
    wait_time = between(1, 3)

    @task(1)
    def test_creating(self):
        fake = Faker()
        data = {
            "login": fake.name(),
            "password": fake.password(),
            "email": fake.email()
        }
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        self.client.post("user/", headers=headers, data=data)
