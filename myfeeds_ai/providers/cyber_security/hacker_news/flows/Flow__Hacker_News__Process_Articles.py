from typing                                                                                 import Dict
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                    import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__S3_DB                     import S3_FILE_NAME__ARTICLE__FEED_ARTICLE
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data              import Hacker_News__Data
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Edit              import Hacker_News__Edit
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage           import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage__Article  import Hacker_News__Storage__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Current_Articles import Schema__Feed__Current_Articles, Schema__Feed__Current_Article, Schema__Feed__Current_Article__Status
from osbot_utils.helpers.Obj_Id                                                             import Obj_Id
from osbot_utils.helpers.flows.Flow                                                         import Flow
from osbot_utils.helpers.flows.decorators.flow                                              import flow
from osbot_utils.helpers.flows.decorators.task                                              import task
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.utils.Lists                                                                import list_index_by

class Flow__Hacker_News__Process_Articles(Type_Safe):
    hacker_news_data      : Hacker_News__Data
    hacker_news_edit      : Hacker_News__Edit
    hacker_news_storage   : Hacker_News__Storage

    current_articles   : Schema__Feed__Current_Articles
    articles_to_process: Dict[Obj_Id,Schema__Feed__Current_Article]

    @task()
    def load_new_articles(self):
        self.current_articles = self.hacker_news_data.current_articles()
        for article_id, article_data in self.current_articles.articles.items():
            if article_data.status == Schema__Feed__Current_Article__Status.TO_PROCESS:
                self.articles_to_process[article_id]=article_data
        print(f"There are {len(self.articles_to_process)} articles to process")

    @task()
    def process_articles__create_article_file(self):
        articles_by_location = {}                                           # todo: refactor this file load cache into a better location
        for article_id, article in self.articles_to_process.items():
            location               = article.location
            articles_by_article_id = articles_by_location.get(location)
            if articles_by_article_id is None:                              # only load once
                print(f'loading data for location: {location}')
                path_data              = self.hacker_news_data.feed_data__in_path(path=location, load_from_live=True)
                articles_list          = path_data.feed_data.json().get('articles')
                articles_by_article_id = list_index_by(articles_list, 'article_obj_id')
                articles_by_location[location] = articles_by_article_id

            if article_id in articles_by_article_id:
                article_storage             = Hacker_News__Storage__Article(article_id=article_id)
                s3_path                     = article_storage.path__path(path=location, file_id=S3_FILE_NAME__ARTICLE__FEED_ARTICLE, extension=S3_Key__File_Extension.JSON)
                article.path__feed_article  = s3_path
                file_exists                 = article_storage.path__exists(s3_path=s3_path)
                if file_exists is False:
                    #s3_path = article_storage.path__path(path=location, file_id=S3_FILE_NAME__ARTICLE__FEED_ARTICLE, extension=S3_Key__File_Extension.JSON)
                    article_data = articles_by_article_id.get(article_id)
                    s3_path      = article_storage.save_to__path(data=article_data, path=location, file_id=S3_FILE_NAME__ARTICLE__FEED_ARTICLE, extension=S3_Key__File_Extension.JSON)
                    print(f"created file {s3_path}")

                    #pprint(article_storage.load_from__path(location, S3_FILE_NAME__ARTICLE__FEED_ARTICLE, S3_Key__File_Extension.JSON))


        self.hacker_news_edit.save__current_articles(self.current_articles)


    @flow()
    def process_articles(self) -> Flow:
        self.load_new_articles()
        self.process_articles__create_article_file()

    def run(self):
        return self.process_articles().execute_flow()