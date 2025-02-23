from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                        import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage               import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Config__New_Articles import Schema__Feed__Config__New_Articles
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe

FILE_NAME__NEW_ARTICLES       = 'new-articles'
FILE_ID__NEW_ARTICLES         = FILE_NAME__NEW_ARTICLES
EXTENSION__NEW_ARTICLES       = S3_Key__File_Extension.JSON.value

class Hacker_News__Data(Type_Safe):
    storage : Hacker_News__Storage

    def new_articles          (self      ) -> Schema__Feed__Config__New_Articles: return self.cast_to__new_articles(self.storage.load_from__latest(file_id=FILE_ID__NEW_ARTICLES, extension=EXTENSION__NEW_ARTICLES           ))
    def new_articles__for_path(self, path) -> Schema__Feed__Config__New_Articles: return self.cast_to__new_articles(self.storage.load_from__path  (file_id=FILE_ID__NEW_ARTICLES, extension=EXTENSION__NEW_ARTICLES, path=path))

    def cast_to__new_articles(self, json_data) -> Schema__Feed__Config__New_Articles:
        #return json_data
        return Schema__Feed__Config__New_Articles.from_json(json_data)
