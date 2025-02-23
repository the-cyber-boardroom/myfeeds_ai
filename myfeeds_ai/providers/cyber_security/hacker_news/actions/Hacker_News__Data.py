from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage import Hacker_News__Storage
from osbot_utils.type_safe.Type_Safe                                              import Type_Safe

FILE_NAME__NEW_ARTICLES       = 'new-articles'

class Hacker_News__Data(Type_Safe):
    storage : Hacker_News__Storage

    def new_articles(self):
        file_id   = FILE_NAME__NEW_ARTICLES
        extension = S3_Key__File_Extension.JSON.value
        return self.storage.load_from__latest(file_id=file_id, extension=extension)

