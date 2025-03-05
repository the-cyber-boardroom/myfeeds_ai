from typing                                                                                        import List
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data                     import Hacker_News__Data
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News                    import FILE_ID__FEED_ARTICLE
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Article              import Hacker_News__File__Article
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Current_Articles     import Hacker_News__File__Current_Articles
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Current_Article__Status import Schema__Feed__Current_Article__Step
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Current_Articles        import Schema__Feed__Current_Article, Schema__Feed__Current_Article__Status, Schema__Feed__Current_Article__Status__Change
from osbot_utils.helpers.flows.Flow                                                                import Flow
from osbot_utils.helpers.flows.decorators.flow                                                     import flow
from osbot_utils.helpers.flows.decorators.task                                                     import task
from osbot_utils.type_safe.Type_Safe                                                               import Type_Safe

FLOW__HACKER_NEWS__4__MAX__ARTICLES_TO_SAVE = 1

class Flow__Hacker_News__4__Create_Article_Files(Type_Safe):
    file_current_articles : Hacker_News__File__Current_Articles
    output                : dict
    articles_to_process   : List[Schema__Feed__Current_Article                ]
    status_changes        : List[Schema__Feed__Current_Article__Status__Change]
    hacker_news_data      : Hacker_News__Data

    @task()
    def task__1__load_articles_to_process(self):
        with self.file_current_articles as _:
            _.load()
            self.articles_to_process = _.next_step__1__save_article()
            #print(f"There are {len(self.articles_to_process)} articles to process")

    @task()
    def task__2__create_missing_article_files(self):
        from_status = Schema__Feed__Current_Article__Status.TO_PROCESS
        from_step   = Schema__Feed__Current_Article__Step.STEP__1__SAVE_ARTICLE
        to_status   = Schema__Feed__Current_Article__Status.PROCESSING
        to_step     = Schema__Feed__Current_Article__Step.STEP__2__LLM__TEXT_TO_GRAPH

        articles_to_save = {}
        for article in self.articles_to_process[0:FLOW__HACKER_NEWS__4__MAX__ARTICLES_TO_SAVE]:
            location         = article.source_location                               # we need to
            if location:
                article_id       = article.article_id
                articles_by_id   = self.hacker_news_data.articles_by_id__in_path(path=location, load_from_live=True)        # note: this value is cached so this has good performance
                article_data     = articles_by_id.get(article_id)
                if article_data:
                    articles_to_save[article] = article_data

        for article, article_data in articles_to_save.items():
            article_id                 = article.article_id
            file_article               = Hacker_News__File__Article(article_id=article_id, file_id=FILE_ID__FEED_ARTICLE)
            data                       = article_data.json()
            article.path__feed_article = file_article.save_data(data)
            article.status             = to_status
            article.next_step          = to_step
            article_change_status      = Schema__Feed__Current_Article__Status__Change(article=article, from_status=from_status, from_step=from_step)
            self.status_changes.append(article_change_status)
            break


        self.file_current_articles.save()

        #     articles_by_article_id = articles_by_location.get(location)

        #     if articles_by_article_id is None:                              # only load once
        #         print(f'loading data for location: {location}')
        #         path_data              = self.hacker_news_data.feed_data__in_path(path=location, load_from_live=True)
        #         articles_list          = path_data.feed_data.json().get('articles')
        #         articles_by_article_id = list_index_by(articles_list, 'article_obj_id')
        #         articles_by_location[location] = articles_by_article_id
        #
        #     if article_id in articles_by_article_id:
        #         article_storage             = Hacker_News__Storage__Article(article_id=article_id)
        #         s3_path                     = article_storage.path__path(path=location, file_id=S3_FILE_NAME__ARTICLE__FEED_ARTICLE, extension=S3_Key__File_Extension.JSON)
        #         article.path__feed_article  = s3_path
        #         file_exists                 = article_storage.path__exists(s3_path=s3_path)
        #         if file_exists is False:
        #             #s3_path = article_storage.path__path(path=location, file_id=S3_FILE_NAME__ARTICLE__FEED_ARTICLE, extension=S3_Key__File_Extension.JSON)
        #             article_data = articles_by_article_id.get(article_id)
        #             s3_path      = article_storage.save_to__path(data=article_data, path=location, file_id=S3_FILE_NAME__ARTICLE__FEED_ARTICLE, extension=S3_Key__File_Extension.JSON)
        #             print(f"created file {s3_path}")
        #
        #             #pprint(article_storage.load_from__path(location, S3_FILE_NAME__ARTICLE__FEED_ARTICLE, S3_Key__File_Extension.JSON))
        #         article.status = Schema__Feed__Current_Article__Status.TO_EXTRACT_TEXT
        #
        # self.hacker_news_edit.save__current_articles(self.current_articles)

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