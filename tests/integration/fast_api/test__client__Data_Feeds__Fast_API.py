from unittest                                     import TestCase
from tests.integration.data_feeds__objs_for_tests import data_feeds__fast_api__client


class test__client__Data_Feeds__Fast_API(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = data_feeds__fast_api__client

    def test__docs__(self):
        response = self.client.get('/docs')
        assert response.status_code == 200
        assert '<title>FastAPI - Swagger UI</title>' in response.text

    def test__ui__html__hacker_news__hacker_news__v1(self):
        path          = 'ui/html/hacker-news/hacker-news__v1.html'
        expected_html = '<webc-hacker-news></webc-hacker-news>'
        response = self.client.get(path)
        assert response.status_code == 200
        assert expected_html in response.text