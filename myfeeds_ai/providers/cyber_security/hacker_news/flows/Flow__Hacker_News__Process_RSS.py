from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files              import Hacker_News__Files
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Feed import Model__Hacker_News__Feed
from osbot_utils.helpers.flows.Flow                                                  import Flow
from osbot_utils.helpers.flows.decorators.flow                                       import flow
from osbot_utils.helpers.flows.decorators.task                                       import task
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe


class Flow__Hacker_News__Process_RSS(Type_Safe):
    files    : Hacker_News__Files
    news_feed: Model__Hacker_News__Feed
    output   : dict

    @task()
    def fetch_rss_feed(self):
        data_feed = self.files.feed_data__load_rss_and_parse()
        if data_feed is None:
            raise ValueError("in fetch_rss_feed failed to fetch data_feed")
        if len(data_feed.feed_data.articles) == 0:
            raise ValueError("in fetch_rss_feed there were no articles in the fetched data feed")
        self.news_feed = data_feed.feed_data

    @task()
    def create_output(self):
        s3_path__now    = self.files.s3_db.s3_path__raw_data__feed_xml__now()
        s3_path__latest = self.files.s3_db.s3_path__raw_data__feed_data__latest()
        self.output = dict(articles_loaded = len(self.news_feed.articles),
                           s3_path__latest = s3_path__latest             ,
                           s3_path__now    = s3_path__now                )

    @flow()
    def process_rss(self) -> Flow:
        self.fetch_rss_feed()
        self.create_output()
        return self.output

    def run(self):
        return self.process_rss().execute_flow()