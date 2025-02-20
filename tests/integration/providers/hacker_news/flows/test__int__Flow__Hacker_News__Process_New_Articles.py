from unittest import TestCase

from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__Process_New_Articles import \
    Flow__Hacker_News__Process_New_Articles
from osbot_utils.utils.Dev import pprint


class test_Flow__Hacker_News__Process_New_Articles(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.flow_process_new_articles = Flow__Hacker_News__Process_New_Articles()

    def test_process_flow(self):
        result                   = self.flow_process_new_articles.run()
        pprint(result.flow_return_value)