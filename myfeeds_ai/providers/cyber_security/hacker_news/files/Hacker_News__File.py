from typing                                                                       import Any
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                          import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage import Hacker_News__Storage
from osbot_utils.helpers.Safe_Id                                                  import Safe_Id
from osbot_utils.type_safe.Type_Safe                                              import Type_Safe


class Hacker_News__File(Type_Safe):
    hacker_news_storage : Hacker_News__Storage
    file_id             : Safe_Id
    file_data           : Any
    extension           : S3_Key__File_Extension

    def delete__latest(self) -> bool: return self.hacker_news_storage.delete_from__path (s3_path = self.path_latest())
    def delete__now   (self) -> bool: return self.hacker_news_storage.delete_from__path (s3_path = self.path_now   ())
    def exists        (self) -> bool : return self.exists__now() and self.exists__latest()
    def exists__latest(self) -> bool: return self.hacker_news_storage.path__exists      (s3_path = self.path_latest())
    def exists__now   (self) -> bool: return self.hacker_news_storage.path__exists      (s3_path = self.path_now   ())
    def path_now      (self) -> str : return self.hacker_news_storage.path__now         (file_id = self.file_id      , extension=self.extension)
    def path_latest   (self) -> str : return self.hacker_news_storage.path__latest      (file_id = self.file_id      , extension=self.extension)

    def file_name(self):
        return f'{self.file_id}.{self.extension.value}'

    def load(self):
        self.file_data = self.hacker_news_storage.load_from__now(file_id=self.file_id, extension=self.extension)
        return self.file_data

    def save(self):
        if not self.file_data:
            raise ValueError(f"in Hacker_News__File.save, there was no data to save, self.file_data was empty")

        with self.hacker_news_storage as _:
            saved__path_now   = _.save_to__now   (data=self.file_data, file_id=self.file_id, extension=self.extension)
            save__path_latest = _.save_to__latest(data=self.file_data, file_id=self.file_id, extension=self.extension)
            if saved__path_now != self.path_now():
                raise ValueError(f"in Hacker_News__MGraph.save, the saved__path_now was '{saved__path_now}' and it was expected to be '{self.path_now()}'")
            if save__path_latest != self.path_latest():
                raise ValueError(f"in Hacker_News__MGraph.save, the save__path_latest was '{save__path_latest}' and it was expected to be '{self.path_latest()}'")

    def save_data(self, file_data):
        self.file_data = file_data
        self.save()

