from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Now import Hacker_News__File__Now
from osbot_utils.utils.Misc                                                       import str_to_bytes

class Hacker_News__File(Hacker_News__File__Now):

    def delete__latest   (self) -> bool: return self.hacker_news_storage.delete_from__path (s3_path = self.path_latest())
    def exists           (self) -> bool : return self.exists__now() and self.exists__latest()
    def exists__latest   (self) -> bool: return self.hacker_news_storage.path__exists      (s3_path = self.path_latest())
    def file_info__latest(self) -> dict: return self.hacker_news_storage.path__file_info   (s3_path = self.path_latest())
    def not_exists       (self) -> bool: return not self.exists()
    def path_latest      (self) -> str : return self.hacker_news_storage.path__latest      (file_id = self.file_id      , extension=self.extension)

    def info(self) -> dict:                                     # Return standardized dictionary with exists, path_latest and path_now information.
        return dict(exists      = self.exists     (),
                    path_latest = self.path_latest(),
                    path_now    = self.path_now   ())


    def load(self):                                                                             # load file data from 'latest' path
        self.file_data = self.hacker_news_storage.load_from__latest(file_id=self.file_id, extension=self.extension, content_type=self.content_type)
        return self.file_data

    def save(self):                     # todo, refactor with the code in super().save() , make sure we don't need to call str_to_bytes (since that has some performance impact)
        if not self.file_data:
            raise ValueError(f"in Hacker_News__File.save, there was no data to save, self.file_data was empty")

        if type(self.file_data) is str and self.content_type:                       # if the data is a string and we have set the content-type
            data = str_to_bytes(self.file_data)                                     # then save it as bytes, since if not the data will be saved as json-dumps of this value (and the content type will not be set)
        else:
            data = self.file_data
        with self.hacker_news_storage as _:
            saved__path_now   = _.save_to__now   (data=data, file_id=self.file_id, extension=self.extension, content_type=self.content_type)
            save__path_latest = _.save_to__latest(data=data, file_id=self.file_id, extension=self.extension, content_type=self.content_type)
            if saved__path_now != self.path_now():
                raise ValueError(f"in Hacker_News__MGraph.save, the saved__path_now was '{saved__path_now}' and it was expected to be '{self.path_now()}'")
            if save__path_latest != self.path_latest():
                raise ValueError(f"in Hacker_News__MGraph.save, the save__path_latest was '{save__path_latest}' and it was expected to be '{self.path_latest()}'")

