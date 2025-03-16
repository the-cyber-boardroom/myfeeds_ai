from typing                                                                                         import List
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage                   import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current     import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article                  import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status__Change  import Schema__Feed__Article__Status__Change
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step            import Schema__Feed__Article__Step
from osbot_utils.helpers.flows.Flow                                                                 import Flow
from osbot_utils.helpers.flows.decorators.flow                                                      import flow
from osbot_utils.helpers.flows.decorators.task                                                      import task
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.utils.Threads                                                                      import execute_in_thread_pool

#from osbot_utils.utils.Dev import pprint

FLOW__HACKER_NEWS__9__MAX__GRAPHS_TO_MERGE = 1

class Flow__Hacker_News__9__Article__Step_6__Merge_Day_Entities_Graphs(Type_Safe):
    file_articles_current : Hacker_News__File__Articles__Current
    hacker_news_storage   : Hacker_News__Storage
    output                : dict
    articles_to_process   : List[Schema__Feed__Article                ]
    status_changes        : List[Schema__Feed__Article__Status__Change]
    max_graphs_to_merge   : int = FLOW__HACKER_NEWS__9__MAX__GRAPHS_TO_MERGE
    from_step             : Schema__Feed__Article__Step               = Schema__Feed__Article__Step.STEP__6__MERGE__DAY_ENTITIES_GRAPHS
    to_step               : Schema__Feed__Article__Step               = Schema__Feed__Article__Step.STEP__7__MERGE__FEED_ENTITIES_GRAPHS
    days_to_process       : set
    files_in_day          : dict

    @task()
    def task__1__load_articles_to_process(self):
        with self.file_articles_current as _:
            _.load()
            self.articles_to_process = _.next_step__6__merge_day_entities_graphs()

    @task()
    def task__2__find_days_to_process(self):
        for article in self.articles_to_process[0:self.max_graphs_to_merge]:
            path__folder__data = article.path__folder__data
            self.days_to_process.add(path__folder__data)


    @task()
    def task__3__llm__merge_day_entities_graphs(self):
        calls    = [((day,), {}) for day in self.days_to_process]                                        # args and kwargs (args need to be tuple))

        execute_in_thread_pool(self.task__3a__llm__merge_day_entities_graphs, calls=calls, max_workers=10)

        #self.file_articles_current.save()

    def task__3a__llm__merge_day_entities_graphs(self, day):
        files_in_day = self.hacker_news_storage.files_in__path(day, include_sub_folders=True)
        self.files_in_day[day] = files_in_day
        #pprint(files_in_day)
        #pass

    def task__4__create_output(self):
        self.output = dict(articles_to_process = len(self.articles_to_process) ,
                           days_to_process     = self.days_to_process          ,
                           files_in_day        = self.files_in_day             ,
                           status_changes      =  self.status_changes   .json())

    @flow()
    def process_articles(self) -> Flow:
        with self as _:
            _.task__1__load_articles_to_process      ()
            _.task__2__find_days_to_process          ()
            _.task__3__llm__merge_day_entities_graphs()
            _.task__4__create_output                 ()
        return self.output

    def run(self):
        return self.process_articles().execute_flow()