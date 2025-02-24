from mgraph_db.mgraph.actions.MGraph__Diff                                                      import MGraph__Diff
from mgraph_db.mgraph.actions.MGraph__Diff__Values                                              import Schema__MGraph__Diff__Values, MGraph__Diff__Values
from mgraph_db.providers.time_chain.MGraph__Time_Chain                                          import MGraph__Time_Chain
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types                   import Time_Chain__Year, Time_Chain__Month, Time_Chain__Day, Time_Chain__Hour, Time_Chain__Source
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                        import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data                  import Hacker_News__Data, FILE_NAME__NEW_ARTICLES, FILE_NAME__CURRENT_ARTICLES
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Live_Data             import Hacker_News__Live_Data
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage               import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Config__New_Articles import Schema__Feed__Config__New_Articles
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Current_Articles     import Schema__Feed__Current_Articles, Schema__Feed__Current_Article
from osbot_utils.context_managers.capture_duration                                              import capture_duration
from osbot_utils.helpers.Obj_Id                                                                 import Obj_Id
from osbot_utils.helpers.flows.Flow                                                             import Flow
from osbot_utils.helpers.flows.decorators.flow                                                  import flow
from osbot_utils.helpers.flows.decorators.task                                                  import task
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe

FILE_NAME__FEED_TIMELINE_MGRAPH = 'feed-timeline.mgraph.json'


class Flow__Hacker_News__Process_New_Articles(Type_Safe):
    hacker_news_storage            : Hacker_News__Storage
    hacker_news_live_data          : Hacker_News__Live_Data
    hacker_news_data               : Hacker_News__Data

    current__articles              : Schema__Feed__Current_Articles     = None
    current__config_new_articles   : Schema__Feed__Config__New_Articles = None
    current__path                  : str                                = None

    previous__path                 : str                                = None
    new__config_new_articles       : Schema__Feed__Config__New_Articles = None

    output                         : dict
    mgraph__diff                   : MGraph__Diff
    mgraph__timeline__current      : MGraph__Time_Chain          = None
    mgraph__timeline__previous     : MGraph__Time_Chain          = None
    duration__load_timeline_data   : float
    durations                      : dict
    timeline_diff                  : Schema__MGraph__Diff__Values = None
    path__new_articles__current    : str
    path__new_articles__latest     : str
    path__current_articles         : str

    @task()
    def resolve__previous__path(self):
        self.current__config_new_articles = self.hacker_news_data.new_articles()  # get latest version
        if self.previous__path is None:
            self.previous__path           = self.current__config_new_articles.path__current
        if self.current__path is None:
            self.current__path =  self.hacker_news_storage.path_to__now_utc()

    @task()
    def load_and_diff_timeline_data(self):

        with capture_duration() as duration:
            data__timeline_current  = self.hacker_news_live_data.get_json(self.current__path , FILE_NAME__FEED_TIMELINE_MGRAPH)
            data__timeline_previous = self.hacker_news_live_data.get_json(self.previous__path, FILE_NAME__FEED_TIMELINE_MGRAPH)
            self.mgraph__timeline__current  = MGraph__Time_Chain.from_json__compressed(data__timeline_current )
            self.mgraph__timeline__previous = MGraph__Time_Chain.from_json__compressed(data__timeline_previous)

            differ = MGraph__Diff__Values(graph1=self.mgraph__timeline__current,
                                          graph2=self.mgraph__timeline__previous)

            self.timeline_diff = differ.compare([ Time_Chain__Year,Time_Chain__Month, Time_Chain__Day, Time_Chain__Hour, Time_Chain__Source])


            self.duration__load_timeline_data = duration.seconds

    @task()
    def update_current_articles(self):
        current_articles = self.hacker_news_data.current_articles() or Schema__Feed__Current_Articles()
        new_articles_ids     = self.timeline_diff.added_values  .get(Time_Chain__Source, set())
        removed_articles_ids = self.timeline_diff.removed_values.get(Time_Chain__Source, set())
        for new_article_id in new_articles_ids:
            #print('added', removed_articles_ids)
            kwargs = dict(location = self.current__path)
            current_article = Schema__Feed__Current_Article(**kwargs)
            if Obj_Id(new_article_id) not in current_articles.articles:
                current_articles.articles[Obj_Id(new_article_id)] = current_article

        for removed_article_id in removed_articles_ids:
            if Obj_Id(removed_article_id) in current_articles.articles:
                #print('removed', removed_article_id)
                del current_articles.articles[Obj_Id(removed_article_id)]

        data      = current_articles.json()
        file_id   = FILE_NAME__CURRENT_ARTICLES
        extension = S3_Key__File_Extension.JSON.value
        with self.hacker_news_storage as _:
            self.path__current_articles = _.save_to__latest(data=data, file_id=file_id, extension=extension)
        self.current__articles = current_articles

    @task()
    def save__config_new_articles__current(self):
        if self.current__path:
            kwargs = dict(path__current    = self.current__path                                           ,
                          path__previous   = self.previous__path                                          ,
                          timeline_diff    = self.timeline_diff                                           ,
                          #new_articles     = self.timeline_diff.added_values  .get(Time_Chain__Source, set()),
                          #removed_articles = self.timeline_diff.removed_values.get(Time_Chain__Source, set())
                          )

            self.new__config_new_articles = Schema__Feed__Config__New_Articles(**kwargs)          # create new object
            data        = self.new__config_new_articles.json()
            file_id     = FILE_NAME__NEW_ARTICLES
            extension   = S3_Key__File_Extension.JSON.value
            with self.hacker_news_storage as _:
                self.path__new_articles__current = _.save_to__path(data=data, path=self.current__path, file_id=file_id, extension=extension)

    @task()
    def save__config_new_articles__latest(self):
        # todo add logic to only update latest when we are in now

        data        = self.new__config_new_articles.json()
        file_id     = FILE_NAME__NEW_ARTICLES
        extension   = S3_Key__File_Extension.JSON.value
        with self.hacker_news_storage as _:
            self.path__new_articles__latest = _.save_to__latest(data=data, file_id=file_id, extension=extension)

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
        with self as _:
            _.resolve__previous__path           ()
            _.load_and_diff_timeline_data       ()
            _.update_current_articles           ()
            #_.create_screenshot                ()
            _.save__config_new_articles__current()
            _.save__config_new_articles__latest ()
            #_.create_output                     ()

        #return self.timeline_diff
        #return self.output
        return self.new__config_new_articles.json()

    def run(self):
        flow = self.process_rss()
        flow.flow_config.print_error_stack_trace = True
        return flow.execute_flow()