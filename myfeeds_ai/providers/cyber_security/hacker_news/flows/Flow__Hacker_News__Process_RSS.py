from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files                                         import Hacker_News__Files
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


class Flow__Hacker_News__Process_RSS(Type_Safe):
    files                    : Hacker_News__Files
    data_feed                : Model__Hacker_News__Data__Feed
    output                   : dict
    flow_timeline            : Flow__Hacker_News__Create_MGraph__Articles__Timeline
    flow_timeline__traces    : str
    duration__fetch_rss_feed : float
    duration__create_timeline: float
    duration__create_output  : float

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
        with Trace_Call__Config() as _:
            _.capture(starts_with=['myfeeds_ai', 'osbot_utils'])
            _.duration(bigger_than=1, padding=150)
            _.up_to_depth(10)
            #_.print_on_exit(True)
            trace_call = Trace_Call(config=_)

        with trace_call:
            with capture_duration() as duration:
                with self.flow_timeline as _:
                    _.setup(data_feed=self.data_feed)
                    _.execute_flow()
            self.duration__create_timeline = duration.seconds
        with Stdout() as stdout:
            trace_call.print()
        self.flow_timeline__traces = stdout.value()

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
        self.output['durations'] = dict(fetch_rss_feed  = self.duration__fetch_rss_feed ,
                                        create_timeline = self.duration__create_timeline,
                                        create_output   = self.duration__create_output  )

    @flow()
    def process_rss(self) -> Flow:
        with self as _:
            _.fetch_rss_feed ()
            _.create_timeline()
            _.create_output  ()
        return self.output

    def run(self):
        return self.process_rss().execute_flow()