from mgraph_db.mgraph.actions.MGraph__Diff                                          import MGraph__Diff
from mgraph_db.mgraph.actions.MGraph__Diff__Values                                  import Schema__MGraph__Diff__Values, MGraph__Diff__Values
from mgraph_db.providers.time_chain.MGraph__Time_Chain                              import MGraph__Time_Chain
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types       import Time_Chain__Year, Time_Chain__Month, Time_Chain__Day, Time_Chain__Hour, Time_Chain__Source
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                            import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data      import Hacker_News__Data, FILE_NAME__NEW_ARTICLES
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage   import Hacker_News__Storage
from osbot_utils.context_managers.capture_duration                                  import capture_duration
from osbot_utils.helpers.flows.Flow                                                 import Flow
from osbot_utils.helpers.flows.decorators.flow                                      import flow
from osbot_utils.helpers.flows.decorators.task                                      import task
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.utils.Http                                                         import GET_json

MY_FEEDS__SERVER              = 'https://dev.myfeeds.ai'
WEB_PATH__PUBLIC__HACKER_NEWS = "public-data/hacker-news"


class Schema__Feed__Config__New_Articles(Type_Safe):
    path__current               : str                          = None
    path__previous              : str                          = None
    path__timeline__current     : str                          = None           # todo: remove since we can figure this value out from the _.path__current
    path__timeline__previous    : str                          = None
    timeline_diff               : Schema__MGraph__Diff__Values = None

class Flow__Hacker_News__Process_New_Articles(Type_Safe):
    hacker_news_storage            : Hacker_News__Storage
    hacker_news_data               : Hacker_News__Data
    output                         : dict
    config_new_articles            : Schema__Feed__Config__New_Articles
    # path__timeline__current     : str = None
    # path__timeline__previous    : str = None
    mgraph__diff                   : MGraph__Diff
    mgraph__timeline__current      : MGraph__Time_Chain          = None
    mgraph__timeline__previous     : MGraph__Time_Chain          = None
    duration__load_timeline_data   : float
    durations                      : dict
    timeline_diff                  : Schema__MGraph__Diff__Values = None
    path__new_articles__current    : str
    path__new_articles__latest     : str

    @task()
    def load_and_diff_timeline_data(self):

        with self.config_new_articles as _:
            if _.path__timeline__current is None:
                raise ValueError("in load_timeline_data, the new_articles.path__timeline__current was not set")
            if _.path__timeline__previous is None:
                raise ValueError("in load_timeline_data, the new_articles.path__timeline__previous was not set")
            json__config_new_articles = self.hacker_news_data.new_articles__for_path(_.path__current)                           # check if already exists
            if json__config_new_articles:
                self.config_new_articles = Schema__Feed__Config__New_Articles.from_json(json__config_new_articles)                  # if it does just deserialise it
            else:
                url__timeline_current   = f"{MY_FEEDS__SERVER}/{WEB_PATH__PUBLIC__HACKER_NEWS}/{_.path__timeline__current }"        # todo: change this to be from the local server
                url__timeline_previous  = f"{MY_FEEDS__SERVER}/{WEB_PATH__PUBLIC__HACKER_NEWS}/{_.path__timeline__previous}"
                with capture_duration() as duration:
                    data__timeline_current  = GET_json(url__timeline_current)                                                       # todo: since we really shouldn't be getting this data from the dev server
                    data__timeline_previous = GET_json(url__timeline_previous)
                    self.mgraph__timeline__current  = MGraph__Time_Chain.from_json__compressed(data__timeline_current )
                    self.mgraph__timeline__previous = MGraph__Time_Chain.from_json__compressed(data__timeline_previous)

                    differ = MGraph__Diff__Values(graph1=self.mgraph__timeline__current,
                                                  graph2=self.mgraph__timeline__previous)

                    self.config_new_articles.timeline_diff = differ.compare([ Time_Chain__Year,Time_Chain__Month, Time_Chain__Day, Time_Chain__Hour, Time_Chain__Source])


                self.duration__load_timeline_data = duration.seconds

    @task()
    def save__config_new_articles__current(self):
        data        = self.config_new_articles.json()
        file_id     = FILE_NAME__NEW_ARTICLES
        extension   = S3_Key__File_Extension.JSON.value
        with self.hacker_news_storage as _:
            self.path__new_articles__current = _.save_to__path(data=data, path=self.config_new_articles.path__current, file_id=file_id, extension=extension)

    @task()
    def save__config_new_articles__latest(self):
        # todo add logic to only update latest when we are in now

        data        = self.config_new_articles.json()
        file_id     = FILE_NAME__NEW_ARTICLES
        extension   = S3_Key__File_Extension.JSON.value
        with self.hacker_news_storage as _:
            self.path__new_articles__latest = _.save_to__latest(data=data, file_id=file_id, extension=extension)

    @task()
    def process_diff(self):
        #pprint(self.config_new_articles)
        #print("process diff will go here")
        pass



    @task()
    def create_screenshot(self):
        #pprint(self.timeline_diff.json())
        #print("creating screenshot")
        # with self.mgraph__diff.screenshot() as _:
        #     if get_env(ENV_NAME__URL__MGRAPH_DB_SERVERLESS):
        #         self.png_bytes = _.dot_to_png(self.dot_code)
        pass

    @task()
    def create_output(self):
        #return {}
        pass


    @flow()
    def process_rss(self) -> Flow:
        #with Flow_Events__To__Open_Observe():
            with self as _:
                _.load_and_diff_timeline_data       ()
                _.process_diff                      ()
                _.create_screenshot                 ()
                _.save__config_new_articles__current()
                _.save__config_new_articles__latest ()
                _.create_output                     ()

        #return self.timeline_diff
        #return self.output

    def run(self):
        flow = self.process_rss()
        flow.flow_config.print_error_stack_trace = True
        return flow.execute_flow()