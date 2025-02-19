from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator import S3_Key__File_Extensions
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files                                         import Hacker_News__Files
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__S3_DB import Hacker_News__S3_DB
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed                      import Model__Hacker_News__Data__Feed
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__Create_MGraph__Articles__Timeline import Flow__Hacker_News__Create_MGraph__Articles__Timeline
from osbot_utils.context_managers.capture_duration                                                              import capture_duration
from osbot_utils.helpers.flows.Flow                                                                             import Flow
from osbot_utils.helpers.flows.decorators.flow                                                                  import flow
from osbot_utils.helpers.flows.decorators.task                                                                  import task
from osbot_utils.helpers.trace.Trace_Call import Trace_Call
from osbot_utils.helpers.trace.Trace_Call__Config import Trace_Call__Config
from osbot_utils.testing.Stdout import Stdout
from osbot_utils.type_safe.Type_Safe                                                                            import Type_Safe
from osbot_utils.utils.Misc import str_to_bytes

S3_FILE_NAME__FEED__TIMELINE = 'feed-timeline'

class Flow__Hacker_News__Process_RSS(Type_Safe):
    s3_db                              : Hacker_News__S3_DB
    files                              : Hacker_News__Files
    data_feed                          : Model__Hacker_News__Data__Feed
    output                             : dict
    flow_timeline                      : Flow__Hacker_News__Create_MGraph__Articles__Timeline
    flow_timeline__traces              : str
    duration__fetch_rss_feed           : float
    duration__create_timeline          : float
    duration__create_timeline__setup   : float
    duration__create_timeline__execute : float
    duration__create_output            : float
    s3_png_bytes__path__now            : str
    s3_png_bytes__path__latest         : str
    s3_dot_code__path__now             : str
    s3_dot_code__path__latest          : str

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
    def create_timeline(self):
        with capture_duration() as duration:
            with self.flow_timeline as _:
                with capture_duration() as duration__setup:
                    _.setup(data_feed=self.data_feed)
                with capture_duration() as duration__execute:
                    _.execute_flow()
        self.duration__create_timeline          = duration.seconds
        self.duration__create_timeline__setup   = duration__setup.seconds
        self.duration__create_timeline__execute = duration__execute.seconds

    @task()
    def save_timeline(self):
        png_bytes = self.flow_timeline.png_bytes
        with self.s3_db as _:
            self.s3_png_bytes__path__now    = _.s3_key_generator.s3_path__now(file_id=S3_FILE_NAME__FEED__TIMELINE, extension=S3_Key__File_Extensions.MGRAPH__PNG)
            self.s3_png_bytes__path__latest = _.s3_path__latest              (file_id=S3_FILE_NAME__FEED__TIMELINE, extension=S3_Key__File_Extensions.MGRAPH__PNG)
            s3_key__now                     = _.s3_key__for_provider_path(self.s3_png_bytes__path__now   )
            s3_key__latest                  = _.s3_key__for_provider_path(self.s3_png_bytes__path__latest)
            png__metadata = {"Content-Type":"image/png"}
            _.s3_save_data(png_bytes, s3_key__now   , metadata=png__metadata)
            _.s3_save_data(png_bytes, s3_key__latest, metadata=png__metadata)

        dot_code       = self.flow_timeline.dot_code
        dot_code_bytes = str_to_bytes(dot_code)
        with self.s3_db as _:
            self.s3_dot_code__path__now    = _.s3_key_generator.s3_path__now(file_id=S3_FILE_NAME__FEED__TIMELINE, extension=S3_Key__File_Extensions.MGRAPH__DOT)
            self.s3_dot_code__path__latest = _.s3_path__latest              (file_id=S3_FILE_NAME__FEED__TIMELINE, extension=S3_Key__File_Extensions.MGRAPH__DOT)
            s3_key__dot_code__now          = _.s3_key__for_provider_path(self.s3_dot_code__path__now   )
            s3_key__dot_code__latest       = _.s3_key__for_provider_path(self.s3_png_bytes__path__latest)
            #dot__metadata = {"Content-Type":"text/vnd.graphviz"}
            dot__metadata = {"Content-Type" : 'text/plain'}
            _.s3_save_data(dot_code_bytes, s3_key__dot_code__now   , metadata=dot__metadata)
            _.s3_save_data(dot_code_bytes, s3_key__dot_code__latest, metadata=dot__metadata)


    @task()
    def create_output(self):
        with capture_duration() as duration:
            feed__s3_path__now        = self.files.s3_db.s3_path__raw_data__feed_xml__now       ()
            feed__s3_path__latest     = self.files.s3_db.s3_path__raw_data__feed_data__latest   ()
            timeline__s3_path__now    = self.flow_timeline.s3_path
            timeline__s3_path__latest = self.flow_timeline.s3_path_latest
            timeline__stats           = self.flow_timeline.mgraph_timeseries.index().stats()
            timeline__dot_code__size  = len(self.flow_timeline.dot_code )
            timeline__png__size       = len(self.flow_timeline.png_bytes)
            timeline__durations       = self.flow_timeline.durations
            self.output               = dict(articles_loaded = len(self.data_feed.feed_data.articles),
                                             feed__s3_path__latest     = feed__s3_path__latest       ,
                                             feed__s3_path__now        = feed__s3_path__now          ,
                                             timeline__dot_code__size  = timeline__dot_code__size    ,
                                             timeline__durations       = timeline__durations         ,
                                             timeline__png__size       = timeline__png__size         ,
                                             timeline__s3_path__latest = timeline__s3_path__latest   ,
                                             timeline__s3_path__now    = timeline__s3_path__now      ,
                                             timeline__stats           = timeline__stats             ,
                                             flow_timeline__traces     = self.flow_timeline__traces)
        self.duration__create_output = duration.seconds
        self.output['durations'] = dict(fetch_rss_feed                     = self.duration__fetch_rss_feed           ,
                                        create_timeline                    = self.duration__create_timeline          ,
                                        duration__create_timeline__setup   = self.duration__create_timeline__setup   ,
                                        duration__create_timeline__execute = self.duration__create_timeline__execute ,
                                        create_output                      = self.duration__create_output            )

    @flow()
    def process_rss(self) -> Flow:
        with self as _:
            _.fetch_rss_feed ()
            _.create_timeline()
            _.save_timeline  ()
            _.create_output  ()
        return self.output

    def run(self):
        return self.process_rss().execute_flow()