from unittest                                                                                       import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__1__Download_RSS_Feed  import Flow__Hacker_News__1__Download_RSS_Feed
from osbot_utils.helpers.flows.Flow                                                                 import Flow
from tests.integration.data_feeds__objs_for_tests                                                   import cbr_website__assert_local_stack


class test__int__Flow__Hacker_News__1__Download_RSS_Feed(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
        cls.download_rss_feed = Flow__Hacker_News__1__Download_RSS_Feed()

    def test_run(self):

        with self.download_rss_feed as _:
            _.files.feed_data__current()
            feed__s3_path__now = _.files.s3_db.s3_path__raw_data__feed_xml__now()
            flow               = _.run()
            assert type(flow) is Flow
            assert flow.flow_return_value == { 'articles_loaded'         : 50                           ,
                                               'duration__fetch_rss_feed': _.duration__fetch_rss_feed   ,
                                               'feed__s3_path__latest'   : 'latest/feed-data.json'      ,
                                               'feed__s3_path__now'      : feed__s3_path__now           }

