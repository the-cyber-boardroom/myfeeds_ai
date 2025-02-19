from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files                                         import Hacker_News__Files
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed                      import Model__Hacker_News__Data__Feed
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__Create_MGraph__Articles__Timeline import Flow__Hacker_News__Create_MGraph__Articles__Timeline
from osbot_utils.helpers.flows.Flow                                                                             import Flow
from osbot_utils.helpers.flows.decorators.flow                                                                  import flow
from osbot_utils.helpers.flows.decorators.task                                                                  import task
from osbot_utils.type_safe.Type_Safe                                                                            import Type_Safe


class Flow__Hacker_News__Process_RSS(Type_Safe):
    files             : Hacker_News__Files
    data_feed         : Model__Hacker_News__Data__Feed
    output            : dict
    flow_timeline     : Flow__Hacker_News__Create_MGraph__Articles__Timeline

    @task()
    def fetch_rss_feed(self):
        data_feed = self.files.feed_data__load_rss_and_parse()
        if data_feed is None:
            raise ValueError("in fetch_rss_feed failed to fetch data_feed")
        if len(data_feed.feed_data.articles) == 0:
            raise ValueError("in fetch_rss_feed there were no articles in the fetched data feed")
        self.data_feed = data_feed

    @task()
    def create_timeline(self):
        with self.flow_timeline as _:
            _.setup(data_feed=self.data_feed)
            _.execute_flow()

    @task()
    def create_output(self):
        feed__s3_path__now        = self.files.s3_db.s3_path__raw_data__feed_xml__now       ()
        feed__s3_path__latest     = self.files.s3_db.s3_path__raw_data__feed_data__latest   ()
        timeline__s3_path__now    = self.flow_timeline.s3_path
        timeline__s3_path__latest = self.flow_timeline.s3_path_latest
        timeline__stats           = self.flow_timeline.mgraph_timeseries.index().stats()
        timeline__dot_code__size  = len(self.flow_timeline.dot_code )
        timeline__png__size       = len(self.flow_timeline.png_bytes)
        self.output               = dict(articles_loaded = len(self.data_feed.feed_data.articles),
                                         feed__s3_path__latest     = feed__s3_path__latest       ,
                                         feed__s3_path__now        = feed__s3_path__now          ,
                                         timeline__dot_code__size  = timeline__dot_code__size     ,
                                         timeline__png__size       = timeline__png__size          ,
                                         timeline__s3_path__latest = timeline__s3_path__latest   ,
                                         timeline__s3_path__now    = timeline__s3_path__now      ,
                                         timeline__stats           = timeline__stats             )

    @flow()
    def process_rss(self) -> Flow:
        with self as _:
            _.fetch_rss_feed ()
            _.create_timeline()
            _.create_output  ()
        return self.output

    def run(self):
        return self.process_rss().execute_flow()