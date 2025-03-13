from typing                                                                                         import List
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Article                   import Hacker_News__Article
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current     import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article                  import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status__Change  import Schema__Feed__Article__Status__Change
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step            import Schema__Feed__Article__Step
from osbot_utils.helpers.flows.Flow                                                                 import Flow
from osbot_utils.helpers.flows.decorators.flow                                                      import flow
from osbot_utils.helpers.flows.decorators.task                                                      import task
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.utils.Dev import pprint

FLOW__HACKER_NEWS__6__MAX__ARTICLES_TO_CREATE = 1

class Flow__Hacker_News__6__LLM_Text_To_Graph(Type_Safe):
    file_articles_current : Hacker_News__File__Articles__Current
    output                : dict
    articles_to_process   : List[Schema__Feed__Article                ]
    status_changes        : List[Schema__Feed__Article__Status__Change]

    @task()
    def task__1__load_articles_to_process(self):
        with self.file_articles_current as _:
            _.load()
            self.articles_to_process = _.next_step__3__llm_text_to_graph()

    @task()
    def task__2__llm__text_to_graph(self):

        from_step   = Schema__Feed__Article__Step.STEP__3__LLM__TEXT_TO_GRAPH
        to_step     = Schema__Feed__Article__Step.STEP__4__CREATE_GRAPH

        for article in self.articles_to_process[0:FLOW__HACKER_NEWS__6__MAX__ARTICLES_TO_CREATE]:
            article_id                   = article.article_id
            path_folder_data             = article.path__folder__data
            hacker_news_article          = Hacker_News__Article(article_id=article_id, path__folder__data=path_folder_data)
            file_article                 = hacker_news_article.file_article().contents()
            text__title                  = file_article.get('title'      )
            text__description            = file_article.get('description')
            print()
            print(text__title)

            text_graph = hacker_news_article.extract_graph_from_text(text__title)
            #pprint(text_graph.json())

            #pprint(file_article)
            # article.path__file__markdown = hacker_news_article.article_markdown__create()
            # article.next_step            = to_step
            article_change_status        = Schema__Feed__Article__Status__Change(article=article, from_step=from_step)
            self.status_changes.append(article_change_status)

        #self.file_articles_current.save()

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