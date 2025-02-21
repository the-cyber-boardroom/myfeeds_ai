from unittest import TestCase

from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types import Time_Chain__Day, Time_Chain__Source
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__Process_New_Articles import Flow__Hacker_News__Process_New_Articles

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Json import json__equals__list_and_set


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

    def test_load_and_diff_timeline_data(self):
        with self.flow_process_new_articles as _:

            _.load_and_diff_timeline_data()                             # since we are using cached data , these will always be the ame
            assert _.timeline_diff is not None
            assert json__equals__list_and_set(_.timeline_diff.json(), { 'added_values'  : {  Time_Chain__Day   : [ '20'],
                                                                                             Time_Chain__Source: [ '272b4927', 'e5091ea4', '5d2f8952', 'ce7e697e',
                                                                                                                   'd54c06c4', '9153bba8', '55b2f8d2'            ]},
                                                                        'removed_values': { Time_Chain__Day    : [ '10'],
                                                                                            Time_Chain__Source : [ '468bfcf6', 'f2082031', '08ec0110', 'ea2a87d4',
                                                                                                                   '0a68e403','d0ca70d4', '5f6bf957'             ]}}
                                              )

