from locust import task, HttpUser, between

class MyUser(HttpUser):
    wait_time = between(1, 3)   

    @task
    def get_posts(self):
        self.client.get("/posts", name ="API_Get_Posts")

    @task
    def get_post(self):
        self.client.get("/posts/1", name ="API_Get_Post_1")

    @task
    def post_post(self):
        self.client.post("/posts", json={"title": "Test Post", "content": "This is a test post."}, name="API_Post_Post")

