from unittest                                                                             import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__Process_RSS import Flow__Hacker_News__Process_RSS
from osbot_utils.utils.Objects                                                            import obj


class test__int__Flow__Hacker_News__Process_RSS(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.flow_process_rss = Flow__Hacker_News__Process_RSS()

    def test_process_flow(self):
        result                   = self.flow_process_rss.run()

        durations                =  dict(fetch_rss_feed  = self.flow_process_rss.duration__fetch_rss_feed ,
                                         create_timeline = self.flow_process_rss.duration__create_timeline,
                                         create_output   = self.flow_process_rss.duration__create_output  )
        feed__s3_path__now       = self.flow_process_rss.files.s3_db.s3_path__raw_data__feed_xml__now()
        timeline__dot_code__size = len(self.flow_process_rss.flow_timeline.dot_code)
        timeline__durations      = self.flow_process_rss.flow_timeline.durations
        timeline__png__size      = len(self.flow_process_rss.flow_timeline.png_bytes)
        timeline__s3_path__now   = self.flow_process_rss.flow_timeline.s3_path
        articles_loaded          = len(self.flow_process_rss.data_feed.feed_data.articles)
        timeline__stats          = self.flow_process_rss.flow_timeline.mgraph_timeseries.index().stats()
        index_data               = obj(timeline__stats).index_data
        expected_return_value    =  dict(articles_loaded           = articles_loaded                    ,
                                         durations                 = durations                          ,
                                         feed__s3_path__latest     = 'latest/feed-data.json'            ,
                                         feed__s3_path__now        = feed__s3_path__now                 ,
                                         timeline__durations       = timeline__durations                ,
                                         timeline__dot_code__size  = timeline__dot_code__size           ,
                                         timeline__png__size       = timeline__png__size                ,
                                         timeline__s3_path__latest = 'latest/feed-timeline__mgraph.json',
                                         timeline__s3_path__now    = timeline__s3_path__now             ,
                                         timeline__stats           = timeline__stats                    )

        assert articles_loaded           > 0
        assert index_data.edge_to_nodes  > 1
        assert result.flow_return_value  == expected_return_value