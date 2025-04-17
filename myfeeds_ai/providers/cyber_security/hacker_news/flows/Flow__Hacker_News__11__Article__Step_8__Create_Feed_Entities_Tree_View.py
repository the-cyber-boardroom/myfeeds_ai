from typing                                                                                             import List
from mgraph_db.mgraph.MGraph                                                                            import MGraph
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Feed__Text_Entities           import Hacker_News__Feed__Text_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage                       import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Text_Entities                 import Node_Type__Article_Id
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File                            import Hacker_News__File
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current         import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article                      import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status__Change      import Schema__Feed__Article__Status__Change
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step                import Schema__Feed__Article__Step
from osbot_utils.helpers.flows.Flow                                                                     import Flow
from osbot_utils.helpers.flows.decorators.flow                                                          import flow
from osbot_utils.helpers.flows.decorators.task                                                          import task
from osbot_utils.type_safe.Type_Safe                                                                    import Type_Safe



FLOW__HACKER_NEWS__8__MAX__ARTICLES_TO_MOVE = 10

class Flow__Hacker_News__11__Article__Step_8__Create_Feed_Entities_Tree_View(Type_Safe):
    file_articles_current                    : Hacker_News__File__Articles__Current
    file__feed_text_entities__files          : Hacker_News__File
    articles_to_process                      : List[Schema__Feed__Article                ]
    status_changes                           : List[Schema__Feed__Article__Status__Change]
    output                                   : dict
    from_step                                : Schema__Feed__Article__Step               = Schema__Feed__Article__Step.STEP__8__CREATE__FEED_ENTITIES_TREE_VIEW
    to_step                                  : Schema__Feed__Article__Step               = Schema__Feed__Article__Step.STEP__9__CREATE__PERSONAS_MAPPINGS
    storage                                  : Hacker_News__Storage
    feed_text_entities                       : Hacker_News__Feed__Text_Entities
    max_articles_to_move                     : int                                       = FLOW__HACKER_NEWS__8__MAX__ARTICLES_TO_MOVE
    path_latest__text_entities__titles__tree : str
    path_now__text_entities__titles__tree    : str

    @task()
    def task__1__load_articles_to_process(self):
        with self.file_articles_current as _:
            _.load()
            self.articles_to_process = _.next_step__8__create_feed_entities_tree_view()
        self.file__feed_text_entities__files = self.feed_text_entities.file__feed_text_entities__files()

    @task()
    def task__2__create_file_with_feed_text_entities_tree_view(self):
        if self.articles_to_process:
            article                                 = self.articles_to_process[0]                                       # we only need one article
            path__file__feed__text_entities__titles = article.path__file__feed__text_entities__titles                   # since we are going to use the version for the "hour now" (which if we got here from the previous step should be the latest)
            file__feed_text_entities_titles__tree   = self.feed_text_entities.file__feed_text_entities_titles__tree()
            json_data                               = self.storage.path__load_data(path__file__feed__text_entities__titles)
            with MGraph.from_json(json_data) as _:
                articles_ids = list(_.index().get_nodes_by_type(Node_Type__Article_Id))       # we should get 50 articles here
                mgraph_tree  = _.export().export_tree_values().as_text(articles_ids)
                file__feed_text_entities_titles__tree.save_data(mgraph_tree)
                self.path_latest__text_entities__titles__tree = file__feed_text_entities_titles__tree.path_latest()
                self.path_now__text_entities__titles__tree    = file__feed_text_entities_titles__tree.path_now()

    @task()
    def task__3__update__feed_text_entities__files(self):
        if self.articles_to_process:
            with self.file__feed_text_entities__files as _:
                data = _.data()
                data.path_latest__text_entities__titles__tree = self.path_latest__text_entities__titles__tree
                data.path_now__text_entities__titles__tree    = self.path_now__text_entities__titles__tree
                _.save_data(data)

    @task()
    def task__4__move_articles_to_next_step(self):
        if self.articles_to_process:
            for article in self.articles_to_process[0:self.max_articles_to_move]:
                article.next_step                                     = self.to_step
                article_change_status                                 = Schema__Feed__Article__Status__Change(article=article, from_step=self.from_step)
                article.path__file__feed__text_entities__titles__tree = self.path_now__text_entities__titles__tree
                self.status_changes.append(article_change_status)

            self.file_articles_current.save()

    @task()
    def task__5__create_output(self):
        self.output = dict(articles_to_process                      = len(self.articles_to_process)                     ,
                           path_feed_text_entities__files           = self.file__feed_text_entities__files.path_now()   ,
                           path_latest__text_entities__titles__tree = self.path_latest__text_entities__titles__tree     ,
                           path_now__text_entities__titles__tree    = self.path_now__text_entities__titles__tree        ,
                           status_changes                           =  self.status_changes.json())


    @flow()
    def process_articles(self) -> Flow:
        with self as _:
            _.task__1__load_articles_to_process                      ()
            _.task__2__create_file_with_feed_text_entities_tree_view ()
            _.task__3__update__feed_text_entities__files             ()
            _.task__4__move_articles_to_next_step                    ()
            _.task__5__create_output                                 ()
        return self.output



    def run(self):
        return self.process_articles().execute_flow()