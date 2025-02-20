from unittest import TestCase

from mgraph_db.mgraph.actions.MGraph__Diff import MGraph__Diff

from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__Process_New_Articles import \
    Flow__Hacker_News__Process_New_Articles
from osbot_utils.helpers.flows.decorators.flow import flow
from osbot_utils.utils.Dev import pprint


class test_Flow__Hacker_News__Process_New_Articles(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.flow_process_new_articles = Flow__Hacker_News__Process_New_Articles()
        cls.path__timeline__current   = '2025/02/20/23/feed-timeline.mgraph.json'
        cls.path__timeline__previous  = '2025/02/19/22/feed-timeline.mgraph.json'
        with cls.flow_process_new_articles as _:
            _.new_articles.path__timeline__current  = cls.path__timeline__current
            _.new_articles.path__timeline__previous = cls.path__timeline__previous

    def test_process_flow(self):
        with self.flow_process_new_articles as _:
            result = self.flow_process_new_articles.run()
        #pprint(result.flow_return_value)

    def test_load_and_diff_timeline_data(self):
        with self.flow_process_new_articles as _:
            _.load_and_diff_timeline_data()
            assert _.timeline_diff is not None

            #pprint(_.timeline_diff.json())
