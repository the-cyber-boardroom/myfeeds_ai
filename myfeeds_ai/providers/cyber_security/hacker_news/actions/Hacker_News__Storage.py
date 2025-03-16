from datetime                                                            import datetime
from typing                                                              import Dict, Optional, List, Any
from mgraph_db.mgraph.MGraph                                             import MGraph
from myfeeds_ai.utils.My_Feeds__Utils                                    import path_to__date_time
from osbot_utils.decorators.methods.cache_on_self                        import cache_on_self
from osbot_utils.helpers.Safe_Id                                         import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path                   import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                                     import Type_Safe
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                 import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__S3_DB  import Hacker_News__S3_DB
from osbot_utils.type_safe.decorators.type_safe                          import type_safe


class Hacker_News__Storage(Type_Safe):
    s3_db : Hacker_News__S3_DB

    @cache_on_self
    def areas(self) -> List[Safe_Id]:
        return []

    def delete_from__latest(self, file_id: Safe_Id, extension: S3_Key__File_Extension) -> str:
        s3_path = self.path__latest(file_id=file_id, extension=extension)
        if self.delete_from__path(s3_path):
            return s3_path
        return False

    def delete_from__path(self, s3_path) -> bool:
        if self.path__exists(s3_path):
            return  self.s3_db.s3_path__delete(s3_path)
        return False

    def delete_from__now(self, file_id: Safe_Id, extension: S3_Key__File_Extension) -> str:
        s3_path = self.path__now(file_id=file_id, extension=extension)
        if self.delete_from__path(s3_path):
            return s3_path

    def file_info_in__latest(self, file_id: Safe_Id, extension: S3_Key__File_Extension) -> Dict:
        s3_path = self.path__latest(file_id=file_id, extension=extension)
        return self.path__file_info(s3_path)

    def file_info_in__now(self, file_id: Safe_Id, extension: S3_Key__File_Extension) -> Dict:
        s3_path = self.path__now(file_id=file_id, extension=extension)
        return self.path__file_info(s3_path)

    def files_in__date_time(self, date_time:datetime, include_sub_folders=False):
        with self.s3_db as _:
            path__latest = _.s3_folder__for_date_time(date_time)
            return _.s3_path__files(path__latest, include_sub_folders=include_sub_folders)

    def files_in__latest(self):
        with self.s3_db as _:
            path__latest = _.s3_folder__for_latest()
            return _.s3_path__files(path__latest)

    # todo: add @type_safe to this method
    def files_in__path(self, path: Safe_Str__File__Path, include_sub_folders=False):
        with self.s3_db as _:
            date_time = path_to__date_time(path)
            return self.files_in__date_time(date_time, include_sub_folders=include_sub_folders)

    def files_in__now(self, include_sub_folders=False):
        with self.s3_db as _:
            path__now_utc =self.path__folder_now()
            return _.s3_path__files(path__now_utc,include_sub_folders=include_sub_folders)

    def save_to__path(self, data: Dict      ,
                            path : str      ,
                            file_id: Safe_Id,
                            extension: S3_Key__File_Extension,
                            content_type : str  = None
                       ) -> str:
        date_time = path_to__date_time(path)
        return self.save_to__date_time(data=data, date_time=date_time, file_id=file_id, extension=extension, content_type=content_type)

    def save_to__date_time(self, data     : Dict     ,
                                 date_time: datetime ,
                                 file_id  : Safe_Id  ,
                                 extension: S3_Key__File_Extension,
                                 content_type: str = None
                            ) -> str:
        with self.s3_db as _:
            s3_path = self.path__date_time(date_time=date_time, file_id=file_id, extension=extension)
            _.s3_path__save_data(data=data, s3_path=s3_path, content_type=content_type)
            return s3_path

    @type_safe
    def save_to__now(self, data         : Any                     ,                  # Save data with current timestamp
                           file_id      : Safe_Id                 ,
                           extension    : S3_Key__File_Extension  ,
                           content_type : str           = None    ,
                           now          : datetime      = None
                      ) -> str:
        with self.s3_db as _:
            s3_path = self.path__now(file_id=file_id, extension=extension, now=now)
            _.s3_path__save_data    (data=data, s3_path=s3_path, content_type=content_type)
            return s3_path

    # def save_to__now__json(self, data: Dict, file_id: Safe_Id) -> str:          # Save json data with current timestamp
    #     return self.save_to__now(data=data, file_id=file_id, extension=S3_Key__File_Extension.JSON)

    @type_safe
    def save_to__now__mgraph(self, mgraph: MGraph, file_id: Safe_Id, now: datetime=None) -> str:          # Save json data with current timestamp
        data = mgraph.json__compress()
        return self.save_to__now(data=data, file_id=file_id, extension=S3_Key__File_Extension.MGRAPH__JSON, now=now)

    def save_to__latest(self, data        : Dict                    ,                # Save data to latest version
                              file_id     : Safe_Id                 ,
                              extension   : S3_Key__File_Extension  ,
                              content_type: str = None
                         ) -> str:
        with self.s3_db as _:
            s3_path = _.s3_path__latest(file_id=file_id, extension=extension)
            _.s3_path__save_data(data=data, s3_path=s3_path, content_type=content_type)
            return s3_path

    @type_safe
    def save_to__latest__mgraph(self, mgraph: MGraph, file_id: Safe_Id) -> str:          # Save json data with current timestamp
        data = mgraph.json__compress()
        return self.save_to__latest(data=data, file_id=file_id, extension=S3_Key__File_Extension.MGRAPH__JSON)

    def load_from__path(self, path: str, file_id: Safe_Id, extension: S3_Key__File_Extension) -> Optional[Dict]:
        if path:
            date_time = path_to__date_time(path)
            return self.load_from__date_time(date_time=date_time, file_id=file_id, extension=extension)

    def load_from__date_time(self, date_time: datetime, file_id: Safe_Id, extension: S3_Key__File_Extension) -> Optional[Dict]:
        s3_path = self.path__date_time(date_time=date_time, file_id=file_id, extension=extension)
        data    = self.path__load_data(s3_path)
        return data


    def load_from__latest(self, file_id: Safe_Id, extension: S3_Key__File_Extension, content_type:str=None) -> Optional[Dict]:
        s3_path = self.s3_db.s3_path__latest(file_id=file_id, extension=extension)
        data    = self.path__load_data(s3_path, content_type=content_type)
        return data

    def load_from__now(self, file_id     : Safe_Id               ,
                             extension   : S3_Key__File_Extension,
                             content_type: str      = None       ,
                             now         : datetime = None
                        ) -> Optional[Dict]:
        s3_path = self.path__now      (file_id=file_id, extension=extension, now=now)
        data    = self.path__load_data(s3_path, content_type=content_type)
        return data

    def path__exists(self, s3_path:str) -> bool:
        return self.s3_db.s3_path__exists(s3_path)

    def path__exists__path(self, path: str,
                                 file_id  : Safe_Id                = None,
                                 extension: S3_Key__File_Extension = None
                            ) -> str:
        s3_path = self.path__path(path=path,file_id=file_id, extension=extension)
        return self.path__exists(s3_path)

    def path__file_info(self, s3_path):
        return self.s3_db.s3_path__file_info(s3_path)

    def path__latest(self, file_id: Safe_Id, extension: S3_Key__File_Extension) -> str:
        return self.s3_db.s3_path__latest(file_id=file_id, extension=extension)

    def path__load_bytes(self, s3_path):
        return self.s3_db.s3_path__load_bytes(s3_path)

    def path__load_data(self, s3_path, content_type=None):
        if content_type:
            return self.s3_db.s3_path__load_bytes(s3_path)
        else:
            return self.s3_db.s3_path__load_data(s3_path)

    def path__folder_now(self, now: datetime=None):
        if now:
            return self.s3_db.s3_path__date_time(date_time=now, areas=self.areas())
        else:
            return self.s3_db.s3_path__now(areas=self.areas())

    def path__folder_root(self, now: datetime=None):                                    # path without any of the areas
        if now:
            return self.s3_db.s3_path__date_time(date_time=now)
        else:
            return self.s3_db.s3_path__now()

    def path__now(self, file_id: Safe_Id, extension: S3_Key__File_Extension, now: datetime=None) -> str:
        if now:
            return self.s3_db.s3_path__date_time(date_time=now, file_id=file_id, extension=extension, areas=self.areas())
        else:
            return self.s3_db.s3_path__now(file_id=file_id, extension=extension, areas=self.areas())

    def path__date_time(self, date_time: datetime,
                              file_id  : Safe_Id                = None,
                              extension: S3_Key__File_Extension = None
                         ) -> str:
        kwargs = dict(date_time  = date_time    ,
                      areas      = self.areas() ,
                      file_id    = file_id      ,
                      extension  = extension    )
        return self.s3_db.s3_key_generator.s3_path__date_time(**kwargs)

    def path__path(self, path: str,
                         file_id  : Safe_Id                = None,
                         extension: S3_Key__File_Extension = None
                    ) -> str:
        date_time = path_to__date_time(path)
        s3_path   = self.path__date_time(date_time=date_time, file_id=file_id, extension=extension)
        return s3_path
    # def load_by__article_id(self, article_id: Obj_Id                  ,           # Load article-specific data
    #                              extension : S3_Key__File_Extensions ) -> Optional[Dict]:
    #     with self.s3_db as _:
    #         s3_key = _.s3_key___article__feed_article__now(article_id)
    #         return _.s3_file_data(s3_key)