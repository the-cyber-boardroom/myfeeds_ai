from typing import List

from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current     import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article                  import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status__Change  import Schema__Feed__Article__Status__Change
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step            import Schema__Feed__Article__Step
from osbot_utils.helpers.flows.decorators.flow import flow
from osbot_utils.helpers.flows.decorators.task                                                      import task
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe

FLOW__HACKER_NEWS__8__MAX__ARTICLES_TO_CREATE = 1

class Flow__Hacker_News__8__Merge_Text_Entities_Graphs(Type_Safe):

    file_articles_current : Hacker_News__File__Articles__Current
    output                : dict
    articles_to_process   : List[Schema__Feed__Article                ]
    status_changes        : List[Schema__Feed__Article__Status__Change]

    @task()
    def task__1__load_articles_to_process(self):
        with self.file_articles_current as _:
            _.load()
            self.articles_to_process = _.next_step__4__create_text_entities_graphs()

    @task()
    def task__2__llm__merge_text_entities_graphs(self):
        from_step   = Schema__Feed__Article__Step.STEP__5__MERGE__TEXT_ENTITIES_GRAPHS
        to_step     = Schema__Feed__Article__Step.STEP__6__MERGE__FEED_ENTITIES_GRAPHS

    def task__3__create_output(self):
        self.output = dict(articles_to_process = len(self.articles_to_process),
                           status_changes     =  self.status_changes.json())


    @flow()
    def process_articles(self) -> Flow:
        with self as _:
            _.task__1__load_articles_to_process         ()
            _.task__2__llm__create_text_entities_graphs ()
            _.task__3__create_output                    ()
        return self.output


    def run(self):
        return self.process_articles().execute_flow()