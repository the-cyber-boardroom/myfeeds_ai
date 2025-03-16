from typing                                                                                     import Dict
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                        import S3_Key__File_Extension
from myfeeds_ai.data_feeds.Data_Feeds__Shared_Constants                                         import S3_FILE_NAME__RAW__FEED_DATA
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Live_Data             import Hacker_News__Live_Data
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage               import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article         import Model__Hacker_News__Article
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed      import Model__Hacker_News__Data__Feed
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Config__New_Articles import Schema__Feed__Config__New_Articles
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Articles             import Schema__Feed__Articles
from osbot_utils.decorators.methods.cache_on_self                                               import cache_on_self
from osbot_utils.helpers.Obj_Id                                                                 import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe

FILE_NAME__CURRENT_ARTICLES   = 'current-articles'
FILE_NAME__NEW_ARTICLES       = 'new-articles'
FILE_ID__NEW_ARTICLES         = FILE_NAME__NEW_ARTICLES
EXTENSION__NEW_ARTICLES       = S3_Key__File_Extension.JSON
EXTENSION__CURRENT_ARTICLES   = S3_Key__File_Extension.JSON

class Hacker_News__Data(Type_Safe):
    storage               : Hacker_News__Storage
    hacker_news_live_data : Hacker_News__Live_Data

    # todo: refactor into new file__* data/class structure
    @cache_on_self  # this method is cached, since this data really shouldn't change and this method is called quite a number of times when trying to load a number of article's data
    def articles_by_id__in_path(self, path: str, load_from_live) -> Dict[Obj_Id, Model__Hacker_News__Article]:
        path_data      = self.feed_data__in_path(path=path, load_from_live=load_from_live)
        articles_by_id = dict()
        for article in path_data.feed_data.articles:
            articles_by_id[article.article_obj_id] = article
        return articles_by_id
        # articles_list          = path_data.feed_data.json().get('articles')
        # articles_by_article_id = list_index_by(articles_list, 'article_obj_id')
        # articles_by_location[location] = articles_by_article_id

    # todo: refactor into new file__* data/class structure
    def feed_data__in_path(self, path, load_from_live=False) -> Model__Hacker_News__Data__Feed:
        if load_from_live:
            file_name = f'{S3_FILE_NAME__RAW__FEED_DATA}.{S3_Key__File_Extension.JSON.value}'
            data      = self.hacker_news_live_data.get_json(path, file_name)
        else:
            data      = self.storage.load_from__path(path, S3_FILE_NAME__RAW__FEED_DATA, S3_Key__File_Extension.JSON)
        if data:
            return Model__Hacker_News__Data__Feed.from_json(data)

    # todo: refactor to use the new file_new_articles
    def new_articles          (self      ) -> Schema__Feed__Config__New_Articles:           #remove usage of cast_to__new_articles
        return self.cast_to__new_articles(self.storage.load_from__latest(file_id=FILE_ID__NEW_ARTICLES, extension=EXTENSION__NEW_ARTICLES           ))

    def new_articles__for_path(self, path) -> Schema__Feed__Config__New_Articles:
        return self.cast_to__new_articles(self.storage.load_from__path  (file_id=FILE_ID__NEW_ARTICLES, extension=EXTENSION__NEW_ARTICLES, path=path))

    # todo: refactor to use the new file_current_articles
    def current_articles(self) -> Schema__Feed__Articles:
        current_articles = self.storage.load_from__latest(file_id=FILE_NAME__CURRENT_ARTICLES, extension=EXTENSION__CURRENT_ARTICLES           )
        return Schema__Feed__Articles.from_json(current_articles)

    def cast_to__new_articles(self, json_data) -> Schema__Feed__Config__New_Articles:       # todo: remove method
        return Schema__Feed__Config__New_Articles.from_json(json_data)
