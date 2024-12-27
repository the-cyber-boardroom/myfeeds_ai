from unittest import TestCase

from osbot_utils.utils.Misc import size

from osbot_utils.utils.Dev import pprint

from myfeeds_ai.providers.cyber_security.security_week.Security_Week__Http_Content import Security_Week__Http_Content
from tests.integration.data_feeds__objs_for_tests import cbr_website__assert_local_stack


class test_Security_Week__Http_Content(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
        cls.http_content = Security_Week__Http_Content()

    def test_raw_content(self):
        with self.http_content as _:
            result = _.raw_content()
            assert len(result.raw_data) > 5000
