from myfeeds_ai.data_feeds.Data_Feeds__Shared_Constants import S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA
from osbot_aws.aws.s3.S3__Key_Generator                 import S3__Key_Generator
from osbot_utils.decorators.methods.type_safe           import type_safe
from osbot_utils.helpers.Safe_Id                        import Safe_Id

class Data_Feeds__S3__Key_Generator(S3__Key_Generator):                # todo: refactor this to a generic class (for multiple feeds)
    root_folder            = S3_FOLDER__ROOT_FOLDER__PUBLIC_DATA
    split_when      : bool = True
    use_minutes     : bool = False

    @type_safe
    def s3_path(self, year: int, month: int, day: int, hour: int, file_id: Safe_Id):
        return f'{year:04}/{month:02}/{day:02}/{hour:02}/{file_id}.json'

    def s3_path__now(self, file_id: Safe_Id):
        year, month, day, hour = self.path__for_date_time__now_utc().split('/')
        return self.s3_path(year, month, day, hour, file_id)


