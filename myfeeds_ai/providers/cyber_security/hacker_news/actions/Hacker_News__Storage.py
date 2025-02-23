from datetime import datetime, timezone
from typing                                                              import Dict, Optional

from myfeeds_ai.data_feeds.Data_Feeds__Shared_Constants import S3_FOLDER_NAME__LATEST
from osbot_utils.helpers.Safe_Id                                         import Safe_Id
from osbot_utils.type_safe.Type_Safe                                     import Type_Safe
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                 import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__S3_DB  import Hacker_News__S3_DB

class Hacker_News__Storage(Type_Safe):
    s3_db : Hacker_News__S3_DB

    def delete_from__latest(self, file_id: Safe_Id, extension: S3_Key__File_Extension) -> str:
        with self.s3_db as _:
            s3_path = _.s3_path__latest(file_id=file_id, extension=extension)
            _.s3_path__delete(s3_path)
            return s3_path

    def delete_from__now(self, file_id: Safe_Id, extension: S3_Key__File_Extension) -> str:
        with self.s3_db as _:
            s3_path = _.s3_path__now(file_id=file_id, extension=extension)
            _.s3_path__delete(s3_path)
            return s3_path

    def files_in__date_time(self, date_time:datetime):
        with self.s3_db as _:
            path__latest = _.s3_folder__for_date_time(date_time)
            return _.s3_path__files(path__latest)

    def files_in__latest(self):
        with self.s3_db as _:
            path__latest = _.s3_folder__for_latest()
            return _.s3_path__files(path__latest)

    def files_in__now(self):
        with self.s3_db as _:
            path__now_utc = _.s3_path__now_utc()
            return _.s3_path__files(path__now_utc)

    def save_to__path(self, data: Dict      ,
                            path : str      ,
                            file_id: Safe_Id,
                            extension: S3_Key__File_Extension
                       ) -> str:
        date_time = self.path_to__date_time(path)
        return self.save_to__date_time(data=data, date_time=date_time, file_id=file_id, extension=extension)

    def save_to__date_time(self, data     : Dict     ,
                                 date_time: datetime ,
                                 file_id  : Safe_Id  ,
                                 extension: S3_Key__File_Extension
                            ) -> str:
        with self.s3_db as _:
            s3_path = _.s3_key_generator.s3_path__date_time(date_time=date_time, file_id=file_id, extension=extension)
            _.s3_path__save_data(data=data, s3_path=s3_path)
            return s3_path

    def save_to__now(self, data     : Dict                    ,                  # Save data with current timestamp
                           file_id  : Safe_Id                 ,
                           extension: S3_Key__File_Extension
                      ) -> str:
        with self.s3_db as _:
            s3_path = _.s3_key_generator.s3_path__now(file_id=file_id, extension=extension)
            _.s3_path__save_data(data=data, s3_path=s3_path)
            return s3_path

    def save_to__latest(self, data     : Dict                    ,                # Save data to latest version
                              file_id  : Safe_Id                 ,
                              extension: S3_Key__File_Extension
                         ) -> str:
        with self.s3_db as _:
            s3_path = _.s3_path__latest(file_id=file_id, extension=extension)
            _.s3_path__save_data(data=data, s3_path=s3_path)
            return s3_path

    def load_from__path(self, path: str, file_id: Safe_Id, extension: S3_Key__File_Extension) -> Optional[Dict]:
        if path:
            date_time = self.path_to__date_time(path)
            return self.load_from__date_time(date_time=date_time, file_id=file_id, extension=extension)

    def load_from__date_time(self, date_time: datetime, file_id: Safe_Id, extension: S3_Key__File_Extension) -> Optional[Dict]:
        with self.s3_db as _:
            s3_path = _.s3_key_generator.s3_path__date_time(date_time=date_time, file_id=file_id, extension=extension)
            return _.s3_path__load_Data(s3_path)

    def load_from__latest(self, file_id: Safe_Id, extension: S3_Key__File_Extension) -> Optional[Dict]:
        with self.s3_db as _:
            s3_path = _.s3_path__latest(file_id=file_id, extension=extension)
            return _.s3_path__load_Data(s3_path)

    def load_from__now(self, file_id: Safe_Id, extension: S3_Key__File_Extension) -> Optional[Dict]:
        with self.s3_db as _:
            s3_path = _.s3_path__now(file_id=file_id, extension=extension)
            return _.s3_path__load_Data(s3_path)

    def path_to__date_time(self, path):
        try:
            date_format = '%Y/%m/%d/%H'                         # Format corresponding to yyyy/mm/dd/hh
            date_time   = datetime.strptime(path, date_format)  # Convert to datetime object
            date_time   = date_time.replace(tzinfo=timezone.utc)
            return date_time
        except Exception:
            return None

    def path_to__now_utc(self):
        return self.s3_db.s3_path__now_utc()

    # def load_by__article_id(self, article_id: Obj_Id                  ,           # Load article-specific data
    #                              extension : S3_Key__File_Extensions ) -> Optional[Dict]:
    #     with self.s3_db as _:
    #         s3_key = _.s3_key___article__feed_article__now(article_id)
    #         return _.s3_file_data(s3_key)