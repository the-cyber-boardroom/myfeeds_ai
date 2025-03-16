from datetime                                                                       import datetime
from typing                                                                         import Any
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                            import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage   import Hacker_News__Storage
from osbot_utils.helpers.Safe_Id                                                    import Safe_Id
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.utils.Misc                                                         import str_to_bytes

class Hacker_News__File__Now(Type_Safe):
    hacker_news_storage : Hacker_News__Storage
    file_id             : Safe_Id
    file_data           : Any
    extension           : S3_Key__File_Extension
    content_type        : str
    now                 : datetime

    def delete__now      (self) -> bool: return self.hacker_news_storage.delete_from__path (s3_path = self.path_now   ())
    def folder__path_now (self) -> str : return self.hacker_news_storage.path__folder_now  (now=self.now)
    def folder__path_root(self) -> str : return self.hacker_news_storage.path__folder_root (now=self.now)
    def exists           (self) -> bool: return self.exists__now()
    def exists__now      (self) -> bool: return self.hacker_news_storage.path__exists      (s3_path = self.path_now   ())
    def file_info__now   (self) -> dict: return self.hacker_news_storage.path__file_info   (s3_path = self.path_now   ())
    def path_now         (self) -> str : return self.hacker_news_storage.path__now         (file_id = self.file_id      , extension=self.extension, now=self.now)

    def contents(self):
        return self.load()

    def info(self) -> dict:
        return dict(exists      = self.exists     (),
                    path_now    = self.path_now   ())

    def file_name(self):
        return f'{self.file_id}.{self.extension.value}'

    def load(self):                                                                             # load file data from 'now' path
        load_kwargs = dict(file_id      = self.file_id     ,
                      extension    = self.extension   ,
                      content_type = self.content_type,
                      now          = self.now         )

        self.file_data = self.hacker_news_storage.load_from__now(**load_kwargs)
        return self.file_data


    def save(self):
        if not self.file_data:
            raise ValueError(f"in Hacker_News__File.save, there was no data to save, self.file_data was empty")

        if type(self.file_data) is str and self.content_type:                       # if the data is a string and we have set the content-type
            data = str_to_bytes(self.file_data)                                     # then save it as bytes, since if not the data will be saved as json-dumps of this value (and the content type will not be set)
        else:
            data = self.file_data
        with self.hacker_news_storage as _:
            save_kwargs = dict(data         = data              ,
                               now          = self.now          ,
                               file_id      = self.file_id      ,
                               extension    = self.extension    ,
                               content_type = self.content_type )
            saved__path_now   = _.save_to__now(**save_kwargs)
            if saved__path_now != self.path_now():
                raise ValueError(f"in Hacker_News__MGraph.save, the saved__path_now was '{saved__path_now}' and it was expected to be '{self.path_now()}'")
            return saved__path_now

    def save_data(self, file_data):
        self.file_data = file_data
        return self.save()