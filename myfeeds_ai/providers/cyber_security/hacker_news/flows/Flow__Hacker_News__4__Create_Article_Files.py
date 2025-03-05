from typing                                                                                        import List

from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Article                  import Hacker_News__Article
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data                     import Hacker_News__Data
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__All        import Hacker_News__File__Articles__All
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles__Current    import Hacker_News__File__Articles__Current
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status         import Schema__Feed__Article__Status
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status__Change import Schema__Feed__Article__Status__Change
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step           import Schema__Feed__Article__Step
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Articles                import Schema__Feed__Article
from osbot_utils.helpers.flows.Flow                                                                import Flow
from osbot_utils.helpers.flows.decorators.flow                                                     import flow
from osbot_utils.helpers.flows.decorators.task                                                     import task
from osbot_utils.type_safe.Type_Safe                                                               import Type_Safe

FLOW__HACKER_NEWS__4__MAX__ARTICLES_TO_SAVE = 1

class Flow__Hacker_News__4__Create_Article_Files(Type_Safe):
    file_articles_all     : Hacker_News__File__Articles__All
    file_articles_current : Hacker_News__File__Articles__Current
    output                : dict
    articles_to_process   : List[Schema__Feed__Article                ]
    status_changes        : List[Schema__Feed__Article__Status__Change]
    hacker_news_data      : Hacker_News__Data

    @task()
    def task__1__load_articles_to_process(self):
        with self.file_articles_current as _:
            _.load()
            self.articles_to_process = _.next_step__1__save_article()
            #print(f"There are {len(self.articles_to_process)} articles to process")

    #@task()
    def task__2__create_missing_article_files(self):
        from_status = Schema__Feed__Article__Status.TO_PROCESS
        from_step   = Schema__Feed__Article__Step.STEP__1__SAVE_ARTICLE
        to_status   = Schema__Feed__Article__Status.PROCESSING
        to_step     = Schema__Feed__Article__Step.STEP__2__MARKDOWN__FOR_ARTICLE

        articles_to_save = {}
        for article in self.articles_to_process[0:FLOW__HACKER_NEWS__4__MAX__ARTICLES_TO_SAVE]:
            location         = article.path__folder__source                               # we need to
            if location:
                article_id       = article.article_id
                articles_by_id   = self.hacker_news_data.articles_by_id__in_path(path=location, load_from_live=True)        # note: this value is cached so this has good performance
                article_data     = articles_by_id.get(article_id)
                if article_data:
                    articles_to_save[article] = article_data

        for article, article_data in articles_to_save.items():
            article_id                       = article.article_id
            hacker_news_article              = Hacker_News__Article(article_id=article_id)
            file_article                     = hacker_news_article.file_article()
            article.path__file__feed_article = hacker_news_article.article_data__save(article_data)
            article.path__folder__data       = file_article.folder__path_root()
            article.status                   = to_status
            article.next_step                = to_step
            article_change_status            = Schema__Feed__Article__Status__Change(article=article, from_status=from_status, from_step=from_step)
            self.status_changes.append(article_change_status)
            self.file_articles_all.add_article(article)


        #self.file_articles_current.save()

    def task__5__create_output(self):
        self.output = dict(articles_to_process = len(self.articles_to_process),
                           status_changes     =  self.status_changes.json()  )

    @flow()
    def process_articles(self) -> Flow:
        with self as _:
            _.task__1__load_articles_to_process    ()
            _.task__2__create_missing_article_files()
            _.task__5__create_output               ()
        return self.output


    def run(self):
        return self.process_articles().execute_flow()