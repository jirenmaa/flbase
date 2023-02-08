from locust import HttpUser, task
from faker import Faker

fake = Faker()

class WebsiteUser(HttpUser):
    min_wait = 1000
    max_wait = 5000

    @task
    def using_celery(self):
        # trying using celery for laod test
        # didnt end well
        question = fake.text()[:100] + "?"
        self.client.post("/fast_question", json={"question": question})

    @task
    def slow_page(self):
        question = fake.text()[:100] + "?"
        self.client.post("/slow_question", json={"question": question})
