from locust import HttpUser, task, constant
import random
from pyquery import PyQuery as pq


class ExampleFlaskAppUser(HttpUser):
    wait_time = constant(2)

    @task
    def homepage(self):
        self.client.get("/")

    @task
    def article_check(self):
        res = self.client.get("/")
        page_content = pq(res.content)

        post_headings = page_content("a.article-title")

        chosen_post = random.choice(post_headings)
        self.client.get(chosen_post.attrib["href"])
