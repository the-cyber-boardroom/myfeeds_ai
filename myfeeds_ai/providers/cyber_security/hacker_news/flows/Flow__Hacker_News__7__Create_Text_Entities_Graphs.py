from typing                                                                                         import List
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Article__Entities         import Hacker_News__Article__Entities
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current     import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article                  import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status__Change  import Schema__Feed__Article__Status__Change
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step            import Schema__Feed__Article__Step
from osbot_utils.helpers.flows.Flow                                                                 import Flow
from osbot_utils.helpers.flows.decorators.flow                                                      import flow
from osbot_utils.helpers.flows.decorators.task                                                      import task
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe

FLOW__HACKER_NEWS__7__MAX__ARTICLES_TO_CREATE = 1

class Flow__Hacker_News__7__Create_Text_Entities_Graphs(Type_Safe):
    file_articles_current : Hacker_News__File__Articles__Current
    output                : dict
    articles_to_process   : List[Schema__Feed__Article                ]
    status_changes        : List[Schema__Feed__Article__Status__Change]

    @task()
    def task__1__load_articles_to_process(self):
        with self.file_articles_current as _:
            _.load()
            self.articles_to_process = _.next_step__4__create_text_entities_graphs()

    #@task()
    def task__2__llm__create_text_entities_graphs(self):
        from_step   = Schema__Feed__Article__Step.STEP__4__CREATE__TEXT_ENTITIES_GRAPHS
        to_step     = Schema__Feed__Article__Step.STEP__5__MERGE__TEXT_ENTITIES_GRAPHS

        for article in self.articles_to_process[0:FLOW__HACKER_NEWS__7__MAX__ARTICLES_TO_CREATE]:
            article_id                         = article.article_id
            path_folder_data                   = article.path__folder__data
            hacker_news_article_entities       = Hacker_News__Article__Entities(article_id=article_id, path__folder__data=path_folder_data)

            result__text_entities__title       = hacker_news_article_entities.create_text_entities_graph__title      ()
            result__text_entities__description = hacker_news_article_entities.create_text_entities_graph__description()


            article.path__file__text_entities__title__mgraph       = result__text_entities__title.path__file__text_entities__mgraph
            article.path__file__text_entities__title__png          = result__text_entities__title.path__file__text_entities__png
            article.path__file__text_entities__description__mgraph = result__text_entities__title.path__file__text_entities__mgraph
            article.path__file__text_entities__description__png    = result__text_entities__title.path__file__text_entities__png
            article.next_step = to_step
            #path__file__text_entities__description__png   = hacker_news_article_entities.create_text_entities_graph__description()

            # if path__file__text_entities__title__png:# and path__file__text_entities__description__png:
            #     article.path__file__text_entities__title__png       = path__file__text_entities__title__png
            #     #article.path__file__text_entities__description__png = path__file__text_entities__description__png
            #
            #     article.next_step            = to_step
            # else:
            #     article.status = Schema__Feed__Article__Status.ERROR__FAILED_TASK
            article_change_status        = Schema__Feed__Article__Status__Change(article=article, from_step=from_step)
            self.status_changes.append(article_change_status)

        #self.file_articles_current.save()

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