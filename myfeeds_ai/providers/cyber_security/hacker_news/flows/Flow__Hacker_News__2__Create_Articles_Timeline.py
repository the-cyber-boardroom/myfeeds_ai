from typing                                                                                      import List
from mgraph_db.mgraph.actions.MGraph__Screenshot                                                 import ENV_NAME__URL__MGRAPH_DB_SERVERLESS
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files                          import Hacker_News__Files
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__S3_DB                          import Hacker_News__S3_DB
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage                import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Timeline__Dot_Code import Hacker_News__File__Timeline__Dot_Code
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Timeline__Png      import Hacker_News__File__Timeline__Png
from myfeeds_ai.providers.cyber_security.hacker_news.mgraphs.Hacker_News__MGraph__Timeline       import Hacker_News__MGraph__Timeline
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article          import Model__Hacker_News__Article
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed       import Model__Hacker_News__Data__Feed
from osbot_utils.helpers.flows.Flow                                                              import Flow
from osbot_utils.helpers.flows.decorators.flow                                                   import flow
from osbot_utils.helpers.flows.decorators.task                                                   import task
from osbot_utils.type_safe.Type_Safe                                                             import Type_Safe
from osbot_utils.utils.Env                                                                       import get_env
from osbot_utils.utils.Misc                                                                      import timestamp_to_datetime

FILE__SCREENSHOT__MGRAPH__TIME_SERIES   = './hacker_news-timeline.png'
FILE_NAME__MGRAPH__TIMELINE             = 'feed-timeline'

class Flow__Hacker_News__2__Create_Articles_Timeline(Type_Safe):
    hacker_news_storage                 : Hacker_News__Storage    
    s3_db                               : Hacker_News__S3_DB
    files                               : Hacker_News__Files
    hacker_news_timeline                : Hacker_News__MGraph__Timeline
    hacker_news_timeline_dot_code       : Hacker_News__File__Timeline__Dot_Code
    hacker_news_timeline_png            : Hacker_News__File__Timeline__Png

    data_feed                           : Model__Hacker_News__Data__Feed      = None
    articles                            : List[Model__Hacker_News__Article]   = None
    #mgraph_timeline                     : MGraph__Time_Chain
    path__now__timeline__mgraph_json    : str = None
    path__latest__timeline__mgraph_json : str = None
    
    # s3_path                             : str
    # s3_path_latest                      : str
    dot_code                            : str
    png_bytes                           : bytes
    output                              : dict

    @task()
    def task__1__load_articles(self):
        self.data_feed = self.files.feed_data__current()
        self.articles  = self.data_feed.feed_data.articles

    @task()
    def task__2__create_mgraph(self):
        if self.hacker_news_timeline.exists():                                                          # if already exists, just load it
            self.hacker_news_timeline.load()
        else:
            with self.hacker_news_timeline.mgraph.create() as _:
                for article in self.articles:                                                           # for each article in data feed articles
                    timestamp_utc = article.when.timestamp_utc * 1000                                   # normalise the article's timestamp
                    date_time     = timestamp_to_datetime(timestamp_utc)                                # convert timestamp into a date_time
                    _.create_from_datetime(dt=date_time, source_id=article.article_obj_id)              # add that date_time to mgraph_timeline

    @task()
    def task__3__save_mgraph(self):
        if self.hacker_news_timeline.exists() is False:             # only save if hacker_news_timeline doesn't exist
            self.hacker_news_timeline.save()

    @task()
    def task__4__create_dot_code(self):                                  # todo: there is a weird performance issue which only happens on an lambda where this takes about 5 secs to complete (for 50 articles)
        with self.hacker_news_timeline_dot_code as _:
            if _.exists():
                self.dot_code = _.load()
            else:
                mgraph_timeline = self.hacker_news_timeline.mgraph
                self.dot_code   = self.hacker_news_timeline_dot_code.create_dot_code(mgraph_timeline=mgraph_timeline)
                _.save_data(self.dot_code)



    @task()
    def task__5__create_png(self):
        if self.hacker_news_timeline_png.exists() is False:
            with self.hacker_news_timeline.mgraph.screenshot() as _:
                if get_env(ENV_NAME__URL__MGRAPH_DB_SERVERLESS):
                    self.png_bytes = _.dot_to_png(self.dot_code)
                    self.hacker_news_timeline_png.save_data(file_data=self.png_bytes)


    @task()
    def task__6__create_output(self):
        self.output = dict(articles_processed            = len(self.articles)                       ,
                           hacker_news_timeline          = self.hacker_news_timeline         .info(),
                           hacker_news_timeline_dot_code = self.hacker_news_timeline_dot_code.info(),
                           hacker_news_timeline_png      = self.hacker_news_timeline_png     .info())


    @flow()
    def create_articles_timeline(self) -> Flow:
        self.task__1__load_articles  ()
        self.task__2__create_mgraph  ()
        self.task__3__save_mgraph    ()
        self.task__4__create_dot_code()
        self.task__5__create_png     ()
        self.task__6__create_output  ()
        return self.output

    def run(self) -> Flow:
        return self.create_articles_timeline().execute_flow()