from mgraph_db.mgraph.actions.MGraph__Diff import MGraph__Diff

from mgraph_db.mgraph.schemas.Schema__MGraph__Diff import Schema__MGraph__Diff

from mgraph_db.providers.time_chain.MGraph__Time_Chain import MGraph__Time_Chain
from osbot_utils.context_managers.capture_duration import capture_duration
from osbot_utils.context_managers.print_duration import print_duration
from osbot_utils.helpers.flows.Flow             import Flow
from osbot_utils.helpers.flows.decorators.flow  import flow
from osbot_utils.helpers.flows.decorators.task import task
from osbot_utils.type_safe.Type_Safe            import Type_Safe
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Http import GET, GET_json

MY_FEEDS__SERVER              = 'https://dev.myfeeds.ai'
WEB_PATH__PUBLIC__HACKER_NEWS = "public-data/hacker-news"

class Schema__Feeds_New_Articles(Type_Safe):
    path__timeline__current     : str                  = None
    path__timeline__previous    : str                  = None
    timeline_diff               : Schema__MGraph__Diff = None

class Flow__Hacker_News__Process_New_Articles(Type_Safe):
    output                      : dict
    new_articles                : Schema__Feeds_New_Articles
    path__timeline__current     : str = None
    path__timeline__previous    : str = None
    mgraph__diff                : MGraph__Diff
    mgraph__timeline__current   : MGraph__Time_Chain          = None
    mgraph__timeline__previous  : MGraph__Time_Chain          = None
    duration__load_timeline_data: float
    durations                   : dict
    timeline_diff               : Schema__MGraph__Diff

    @task()
    def load_and_diff_timeline_data(self):
        with self.new_articles as _:
            if _.path__timeline__current is None:
                raise ValueError("in load_timeline_data, the new_articles.path__timeline__current was not set")
            if _.path__timeline__previous is None:
                raise ValueError("in load_timeline_data, the new_articles.path__timeline__previous was not set")

            url__timeline_current   = f"{MY_FEEDS__SERVER}/{WEB_PATH__PUBLIC__HACKER_NEWS}/{_.path__timeline__current }"
            url__timeline_previous  = f"{MY_FEEDS__SERVER}/{WEB_PATH__PUBLIC__HACKER_NEWS}/{_.path__timeline__previous}"
            with capture_duration() as duration:
                data__timeline_current  = GET_json(url__timeline_current)
                data__timeline_previous = GET_json(url__timeline_previous)
                self.mgraph__timeline__current  = MGraph__Time_Chain.from_json__compressed(data__timeline_current )
                self.mgraph__timeline__previous = MGraph__Time_Chain.from_json__compressed(data__timeline_previous)
                self.mgraph__diff               = MGraph__Diff(graph_a = self.mgraph__timeline__current.graph ,
                                                               graph_b = self.mgraph__timeline__previous.graph)
                self.timeline_diff              = self.mgraph__diff.diff_graphs()

        self.duration__load_timeline_data = duration.seconds

    @task()
    def process_diff(self):
        print("process diff will go here")
    @task()
    def create_output(self):
        return {}


    @flow()
    def process_rss(self) -> Flow:
        with self as _:
            _.load_and_diff_timeline_data()
            # _.fetch_rss_feed()
            # _.create_timeline()
            # _.save_timeline()
            # _.invalidate_cache()
            _.create_output()

        return self.output

    def run(self):
        return self.process_rss().execute_flow()