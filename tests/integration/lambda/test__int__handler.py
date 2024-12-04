from unittest             import TestCase
from starlette.testclient import TestClient

from cbr_custom_news_feeds.lambdas.handler import app


class test__int__handler(TestCase):

    @classmethod
    def setUp(cls):
        cls.client = TestClient(app)

    def test_openapi(self):
        response = self.client.get("/openapi.json")
        assert response.status_code == 200
        assert response.json().get("openapi") == "3.1.0"
