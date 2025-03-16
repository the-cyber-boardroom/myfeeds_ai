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
from osbot_utils.utils.Threads                                                                     import execute_in_thread_pool

FLOW__HACKER_NEWS__4__MAX__ARTICLES_TO_SAVE = 1

class Flow__Hacker_News__4__Article__Step_1__Create_Article_Files(Type_Safe):
    articles_to_process   : List[Schema__Feed__Article]
    articles_to_save      : dict
    file_articles_all     : Hacker_News__File__Articles__All
    file_articles_current : Hacker_News__File__Articles__Current
    hacker_news_data      : Hacker_News__Data
    max_articles_to_save  : int                                         = FLOW__HACKER_NEWS__4__MAX__ARTICLES_TO_SAVE
    output                : dict
    status_changes        : List[Schema__Feed__Article__Status__Change]

    from_status           : Schema__Feed__Article__Status = Schema__Feed__Article__Status.TO_PROCESS
    to_status             : Schema__Feed__Article__Status = Schema__Feed__Article__Status.PROCESSING

    from_step             : Schema__Feed__Article__Step   = Schema__Feed__Article__Step  .STEP__1__SAVE__ARTICLE
    to_step               : Schema__Feed__Article__Step   = Schema__Feed__Article__Step  .STEP__2__MARKDOWN__FOR_ARTICLE


    @task()
    def task__1__load_articles_to_process(self):
        with self.file_articles_current as _:
            _.load()
            self.articles_to_process = _.next_step__1__save_article()
            print(f'there are {len(self.articles_to_process)} articles to process')

    @task()
    def task__2__find_articles_to_safe(self):
        for article in self.articles_to_process[0:self.max_articles_to_save]:
            location         = article.path__folder__source
            if location:
                article_id       = article.article_id
                articles_by_id   = self.hacker_news_data.articles_by_id__in_path(path=location, load_from_live=True)        # note: this value is cached so this has good performance
                article_data     = articles_by_id.get(article_id)
                if article_data:
                    self.articles_to_save[article] = article_data


    @task()
    def task__3__create_missing_article_files(self):

        calls = [ ((article, article_data), {})                                     # Each call has positional args but no keyword args
                  for article, article_data in self.articles_to_save.items() ]
        execute_in_thread_pool(target_function=self.task__3a__process_article, calls=calls)

        self.file_articles_current.save()



    @task()
    def task__3a__process_article(self, article, article_data):
        article_id                       = article.article_id
        hacker_news_article              = Hacker_News__Article(article_id=article_id)
        file_article                     = hacker_news_article.file_article()
        article.path__file__feed_article = hacker_news_article.article_data__save(article_data)
        article.path__folder__data       = file_article.folder__path_root()
        article.status                   = self.to_status
        article.next_step                = self.to_step
        article_change_status            = Schema__Feed__Article__Status__Change(article=article, from_status=self.from_status, from_step=self.from_step)
        self.status_changes.append(article_change_status)
        self.file_articles_all.add_article(article)


    @task()
    def task__4__create_output(self):
        self.output = dict(articles_to_process = len(self.articles_to_process),
                           status_changes     =  self.status_changes.json()  )


    @flow()
    def process_articles(self) -> Flow:
        with self as _:
            _.task__1__load_articles_to_process    ()
            _.task__2__find_articles_to_safe       ()
            _.task__3__create_missing_article_files()
            _.task__4__create_output               ()
        return self.output


    def run(self):
        return self.process_articles().execute_flow()