from typing                                                                                         import List
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Text_Entities             import Hacker_News__Text_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current     import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article                  import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status__Change  import Schema__Feed__Article__Status__Change
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step            import Schema__Feed__Article__Step
from osbot_utils.helpers.flows.Flow                                                                 import Flow
from osbot_utils.helpers.flows.decorators.flow                                                      import flow
from osbot_utils.helpers.flows.decorators.task                                                      import task
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.utils.Threads                                                                      import execute_in_thread_pool

FLOW__HACKER_NEWS__8__MAX__GRAPHS_TO_MERGE = 1

class Flow__Hacker_News__8__Article__Step_5__Merge_Text_Entities_Graphs(Type_Safe):

    file_articles_current : Hacker_News__File__Articles__Current
    output                : dict
    articles_to_process   : List[Schema__Feed__Article                ]
    status_changes        : List[Schema__Feed__Article__Status__Change]
    max_graphs_to_merge   : int = FLOW__HACKER_NEWS__8__MAX__GRAPHS_TO_MERGE
    from_step             : Schema__Feed__Article__Step               = Schema__Feed__Article__Step.STEP__5__MERGE__TEXT_ENTITIES_GRAPHS
    to_step               : Schema__Feed__Article__Step               = Schema__Feed__Article__Step.STEP__6__MERGE__DAY_ENTITIES_GRAPHS

    @task()
    def task__1__load_articles_to_process(self):
        with self.file_articles_current as _:
            _.load()
            self.articles_to_process = _.next_step__5__merge_text_entities_graphs()

    @task()
    def task__2__llm__merge_text_entities_graphs(self):
        articles = self.articles_to_process[0:self.max_graphs_to_merge]
        calls    = [((article,), {}) for article in articles]              # args and kwargs (args need to be tuple))

        execute_in_thread_pool(self.task__2s__llm__merge_text_entities_graphs, calls=calls, max_workers=10)

        self.file_articles_current.save()

    #@task()
    def task__2s__llm__merge_text_entities_graphs(self, article):

        article_id                         = article.article_id

        with Hacker_News__Text_Entities().setup() as _:
            article_entities                  = _.article_entities(article_id=article_id)
            mgraph_text_entities__title       = _.mgraph__for_article__text_entities__title      (article_entities=article_entities)
            mgraph_text_entities__description = _.mgraph__for_article__text_entities__description(article_entities=article_entities)

            _.add_text_entities_mgraph(article_id=article_id, mgraph_text_entities=mgraph_text_entities__title      )
            _.add_text_entities_mgraph(article_id=article_id, mgraph_text_entities=mgraph_text_entities__description)

            file__mgraph_text_entities__mgraph = article_entities.file___text__entities__mgraph()
            file__mgraph_text_entities__png    = article_entities.file___text__entities__png   ()

            if file__mgraph_text_entities__mgraph.exists() is False:
                file__mgraph_text_entities__mgraph.save_data(_.mgraph_entities.json())
            if file__mgraph_text_entities__png.exists() is False:
                file__mgraph_text_entities__png.save_data(_.png_bytes__for_mgraph_entities())

            article.path__file__text_entities__mgraph = file__mgraph_text_entities__mgraph.path_now()
            article.path__file__text_entities__png    = file__mgraph_text_entities__png   .path_now()

        article.next_step = self.to_step
        article_change_status = Schema__Feed__Article__Status__Change(article=article, from_step=self.from_step)
        self.status_changes.append(article_change_status)



    def task__3__create_output(self):
        self.output = dict(articles_to_process = len(self.articles_to_process),
                           status_changes     =  self.status_changes.json())



    @flow()
    def process_articles(self) -> Flow:
        with self as _:
            _.task__1__load_articles_to_process         ()
            _.task__2__llm__merge_text_entities_graphs ()
            _.task__3__create_output                    ()
        return self.output


    def run(self):
        return self.process_articles().execute_flow()