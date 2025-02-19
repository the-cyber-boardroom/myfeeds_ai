from unittest import TestCase

from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__Process_RSS import \
    Flow__Hacker_News__Process_RSS
from osbot_utils.utils.Dev import pprint


class test__int__Flow__Hacker_News__Process_RSS(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.flow_process_rss = Flow__Hacker_News__Process_RSS()

    def test_process_flow(self):
        s3_path__now          = self.flow_process_rss.files.s3_db.s3_path__raw_data__feed_xml__now()
        result                = self.flow_process_rss.run()
        articles_loaded       = len(self.flow_process_rss.news_feed.articles)
        expected_return_value =  dict(articles_loaded = articles_loaded        ,
                                      s3_path__latest = 'latest/feed-data.json',
                                      s3_path__now    = s3_path__now           )

        assert articles_loaded          > 0
        assert result.flow_return_value == expected_return_value