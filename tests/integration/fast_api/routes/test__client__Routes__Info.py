from unittest                                       import TestCase
from myfeeds_ai.utils.Version                       import version__myfeeds_ai
from tests.integration.data_feeds__objs_for_tests   import myfeeds_tests__setup_fast_api__and_localstack


class test__client__Routes__Info(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = myfeeds_tests__setup_fast_api__and_localstack().data_feeds__fast_api__client

    def test_raw__uk__homepage(self):
        response = self.client.get('/info/version')
        assert response.status_code == 200
        assert response.json()      == {'version': version__myfeeds_ai }

