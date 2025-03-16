from typing                                                                                         import List
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Article                   import Hacker_News__Article
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Article__Entities         import Hacker_News__Article__Entities
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current     import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article                  import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status__Change  import Schema__Feed__Article__Status__Change
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step            import Schema__Feed__Article__Step
from osbot_utils.helpers.flows.Flow                                                                 import Flow
from osbot_utils.helpers.flows.decorators.flow                                                      import flow
from osbot_utils.helpers.flows.decorators.task                                                      import task
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.utils.Threads                                                                      import execute_in_thread_pool

FLOW__HACKER_NEWS__6__MAX__ARTICLES_TO_CREATE = 1

class Flow__Hacker_News__6__Article__Step_3__LLM_Text_To_Entities(Type_Safe):
    file_articles_current : Hacker_News__File__Articles__Current
    output                : dict
    articles_to_process   : List[Schema__Feed__Article                ]
    status_changes        : List[Schema__Feed__Article__Status__Change]
    max_articles_to_create: int = FLOW__HACKER_NEWS__6__MAX__ARTICLES_TO_CREATE

    @task()
    def task__1__load_articles_to_process(self):
        with self.file_articles_current as _:
            _.load()
            self.articles_to_process = _.next_step__3__llm_text_to_entities()

    @task()
    def task__2__llm__text_to_graph(self):
        articles = self.articles_to_process[0:self.max_articles_to_create]

        calls = [((article,), {}) for article in articles]              # args and kwargs (args need to be tuple))

        execute_in_thread_pool(self.task__2a__process_article, calls=calls)

        self.file_articles_current.save()

    @task()
    def task__2a__process_article(self, article):
        from_step   = Schema__Feed__Article__Step.STEP__3__LLM__TEXT_TO_ENTITIES
        to_step     = Schema__Feed__Article__Step.STEP__4__CREATE__TEXT_ENTITIES_GRAPHS

        article_id                         = article.article_id
        path_folder_data                   = article.path__folder__data
        hacker_news_article                = Hacker_News__Article          (article_id=article_id, path__folder__data=path_folder_data)
        hacker_news_article_entities       = Hacker_News__Article__Entities(article_id=article_id, path__folder__data=path_folder_data)
        file___text__entities__title       = hacker_news_article_entities.file___text__entities__title()
        file___text__entities__description = hacker_news_article_entities.file___text__entities__description()
        file_article                       = hacker_news_article.file_article().contents()
        text__title                        = file_article.get('title'      )
        text__description                  = file_article.get('description')

        if file___text__entities__title.exists() is False:
            text_entities__title = hacker_news_article.extract_entities_from_text(text__title)
            file___text__entities__title.save_data(file_data=text_entities__title.json())

        if file___text__entities__description.exists() is False:
            text_entities__description = hacker_news_article.extract_entities_from_text(text__description)
            file___text__entities__description.save_data(file_data=text_entities__description.json())


        article.path__file__text_entities__title       = file___text__entities__title.path_now      ()
        article.path__file__text_entities__description = file___text__entities__description.path_now()

        article.next_step            = to_step
        article_change_status        = Schema__Feed__Article__Status__Change(article=article, from_step=from_step)
        self.status_changes.append(article_change_status)

    @task()
    def task__3__create_output(self):
        self.output = dict(articles_to_process = len(self.articles_to_process),
                           status_changes     =  self.status_changes.json())

    @flow()
    def process_articles(self) -> Flow:
        with self as _:
            _.task__1__load_articles_to_process ()
            _.task__2__llm__text_to_graph       ()
            _.task__3__create_output            ()
        return self.output


    def run(self):
        return self.process_articles().execute_flow()