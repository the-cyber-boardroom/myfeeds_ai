from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                        import S3_Key__File_Extension
from myfeeds_ai.data_feeds.Data_Feeds__Shared_Constants                                         import S3_FILE_NAME__RAW__FEED_DATA
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Live_Data             import Hacker_News__Live_Data
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage               import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed      import Model__Hacker_News__Data__Feed
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Config__New_Articles import Schema__Feed__Config__New_Articles
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Current_Articles     import Schema__Feed__Current_Articles
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe

FILE_NAME__CURRENT_ARTICLES   = 'current-articles'
FILE_NAME__NEW_ARTICLES       = 'new-articles'
FILE_ID__NEW_ARTICLES         = FILE_NAME__NEW_ARTICLES
EXTENSION__NEW_ARTICLES       = S3_Key__File_Extension.JSON.value
EXTENSION__CURRENT_ARTICLES   = S3_Key__File_Extension.JSON.value

class Hacker_News__Data(Type_Safe):
    storage               : Hacker_News__Storage
    hacker_news_live_data : Hacker_News__Live_Data

    def feed_data__in_path(self, path, load_from_live=False) -> Model__Hacker_News__Data__Feed:
        if load_from_live:
            file_name = f'{S3_FILE_NAME__RAW__FEED_DATA}.{S3_Key__File_Extension.JSON.value}'
            data      = self.hacker_news_live_data.get_json(path, file_name)
        else:
            data      = self.storage.load_from__path(path, S3_FILE_NAME__RAW__FEED_DATA, S3_Key__File_Extension.JSON.value)
        if data:
            return Model__Hacker_News__Data__Feed.from_json(data)

    def new_articles          (self      ) -> Schema__Feed__Config__New_Articles:           #remove usage of cast_to__new_articles
        return self.cast_to__new_articles(self.storage.load_from__latest(file_id=FILE_ID__NEW_ARTICLES, extension=EXTENSION__NEW_ARTICLES           ))

    def new_articles__for_path(self, path) -> Schema__Feed__Config__New_Articles:
        return self.cast_to__new_articles(self.storage.load_from__path  (file_id=FILE_ID__NEW_ARTICLES, extension=EXTENSION__NEW_ARTICLES, path=path))


    def current_articles(self) -> Schema__Feed__Current_Articles:
        current_articles = self.storage.load_from__latest(file_id=FILE_NAME__CURRENT_ARTICLES, extension=EXTENSION__CURRENT_ARTICLES           )
        return Schema__Feed__Current_Articles.from_json(current_articles)

    def cast_to__new_articles(self, json_data) -> Schema__Feed__Config__New_Articles:       # todo: remove method
        return Schema__Feed__Config__New_Articles.from_json(json_data)
