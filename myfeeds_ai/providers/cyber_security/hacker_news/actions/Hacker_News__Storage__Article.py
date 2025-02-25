from datetime import datetime, timezone
from typing import Dict, Optional, List

from myfeeds_ai.data_feeds.Data_Feeds__Shared_Constants import S3_FOLDER_NAME__LATEST
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage import Hacker_News__Storage
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.Obj_Id import Obj_Id
from osbot_utils.helpers.Safe_Id                                         import Safe_Id
from osbot_utils.type_safe.Type_Safe                                     import Type_Safe
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                 import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__S3_DB  import Hacker_News__S3_DB

S3_FOLDER_NAME__ARTICLES = 'articles'

class Hacker_News__Storage__Article(Hacker_News__Storage):
    article_id : Obj_Id

    @cache_on_self
    def areas(self) -> List[Safe_Id]:
        return [Safe_Id(S3_FOLDER_NAME__ARTICLES), Safe_Id(self.article_id)]

    def s3_path__date_time(self, **kwargs):
        s3_path = super().s3_path__date_time(**kwargs)
        print('s3_path', s3_path)
        return s3_path

    # @cache_on_self
    # def article_areas(self) -> List[Safe_Id]:
    #
    #
    # def s3_path__date_time(self, date_time: datetime,
    #                              areas    : List[Safe_Id]          = None,
    #                              file_id  : Safe_Id                = None,
    #                              extension: S3_Key__File_Extension = None
    #                         ) -> str:
    #     article_areas = self.article_areas()
    #     s3_path = super().s3_path__date_time(date_time=date_time, areas=article_areas, file_id=file_id, extension=extension)
    #     return s3_path

    # def s3_path__now(self, file_id: Safe_Id, extension: S3_Key__File_Extension):
    #     original_path = super().s3_path__now(file_id=file_id, extension=extension)
    #     return original_path