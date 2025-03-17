from typing                                                                                             import List
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current         import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article                      import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status__Change      import Schema__Feed__Article__Status__Change
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step                import Schema__Feed__Article__Step
from osbot_utils.helpers.flows.Flow                                                                     import Flow
from osbot_utils.helpers.flows.decorators.flow                                                          import flow
from osbot_utils.helpers.flows.decorators.task                                                          import task
from osbot_utils.type_safe.Type_Safe                                                                    import Type_Safe


class Flow__Hacker_News__11__Article__Step_8__Create_Feed_Entities_Tree_View(Type_Safe):
    file_articles_current: Hacker_News__File__Articles__Current
    articles_to_process  : List[Schema__Feed__Article                ]
    status_changes       : List[Schema__Feed__Article__Status__Change]
    output               : dict
    from_step            : Schema__Feed__Article__Step               = Schema__Feed__Article__Step.STEP__8__CREATE__FEED_ENTITIES_TREE_VIEW
    to_step              : Schema__Feed__Article__Step               = Schema__Feed__Article__Step.STEP__9__CREATE__PERSONAS_MAPPINGS

    @task()
    def task__1__load_articles_to_process(self):
        with self.file_articles_current as _:
            _.load()
            self.articles_to_process = _.next_step__8__create_feed_entities_tree_view()

    @task()
    def task__2__create_file_with_feed_text_entities_mgraph(self):
        ...

    @flow()
    def process_articles(self) -> Flow:
        with self as _:
            _.task__1__load_articles_to_process                   ()
            _.task__2__create_file_with_feed_text_entities_mgraph ()
            _.task__3__create_output                              ()
        return self.output


    def task__3__create_output(self):
        self.output = dict(articles_to_process = len(self.articles_to_process),
                           status_changes     =  self.status_changes.json())

    def run(self):
        return self.process_articles().execute_flow()