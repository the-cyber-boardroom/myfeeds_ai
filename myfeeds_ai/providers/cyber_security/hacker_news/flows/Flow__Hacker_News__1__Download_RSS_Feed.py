from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files                      import Hacker_News__Files
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed   import Model__Hacker_News__Data__Feed
from osbot_utils.helpers.duration.decorators.capture_duration                                import capture_duration

from osbot_utils.helpers.flows.Flow                                                          import Flow
from osbot_utils.helpers.flows.decorators.flow                                               import flow
from osbot_utils.helpers.flows.decorators.task                                               import task
from osbot_utils.type_safe.Type_Safe                                                         import Type_Safe

S3_FILE_NAME__FEED__TIMELINE = 'feed-timeline'

class Flow__Hacker_News__1__Download_RSS_Feed(Type_Safe):
    files                              : Hacker_News__Files
    data_feed                          : Model__Hacker_News__Data__Feed
    output                             : dict
    duration__fetch_rss_feed           : float

    @task()
    def fetch_rss_feed(self):
        with capture_duration() as duration:
            data_feed = self.files.feed_data__load_rss_and_parse()
            if data_feed is None:
                raise ValueError("in fetch_rss_feed failed to fetch data_feed")
            if len(data_feed.feed_data.articles) == 0:
                raise ValueError("in fetch_rss_feed there were no articles in the fetched data feed")
            self.data_feed = data_feed
        self.duration__fetch_rss_feed = duration.seconds

    @task()
    def create_output(self):
        feed__s3_path__now        = self.files.s3_db.s3_path__raw_data__feed_xml__now       ()
        feed__s3_path__latest     = self.files.s3_db.s3_path__raw_data__feed_data__latest   ()
        self.output               = dict(articles_loaded = len(self.data_feed.feed_data.articles),
                                         feed__s3_path__latest     = feed__s3_path__latest        ,
                                         feed__s3_path__now        = feed__s3_path__now           ,
                                         duration__fetch_rss_feed  = self.duration__fetch_rss_feed)



    @flow()
    def download_rss_feed(self) -> Flow:
        with self as _:
            _.fetch_rss_feed ()
            _.create_output  ()
        return self.output

    def run(self):
        return self.download_rss_feed().execute_flow()