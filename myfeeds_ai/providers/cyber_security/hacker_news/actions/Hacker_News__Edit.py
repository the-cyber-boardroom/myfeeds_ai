from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                    import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data              import FILE_NAME__CURRENT_ARTICLES
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage           import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Articles import Schema__Feed__Articles
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                                             import type_safe


class Hacker_News__Edit(Type_Safe):
    hacker_news_storage : Hacker_News__Storage

    @type_safe
    def save__current_articles(self, current_articles: Schema__Feed__Articles):
        file_id   = FILE_NAME__CURRENT_ARTICLES
        extension = S3_Key__File_Extension.JSON.value
        with self.hacker_news_storage as _:
            data   = current_articles.json()
            s3_path = _.save_to__latest(data=data, file_id=file_id, extension=extension)
            return s3_path