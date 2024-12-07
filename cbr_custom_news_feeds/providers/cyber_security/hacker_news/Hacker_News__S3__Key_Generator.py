from osbot_aws.aws.s3.S3__Key_Generator         import S3__Key_Generator
from osbot_utils.decorators.methods.type_safe   import type_safe
from osbot_utils.helpers.Safe_Id                import Safe_Id

S3_FOLDER__ROOT_FOLDER__HACKER_NEWS = 'hacker-news__rss-feed'

class Hacker_News__S3__Key_Generator(S3__Key_Generator):
    root_folder        = S3_FOLDER__ROOT_FOLDER__HACKER_NEWS
    split_when  : bool = True
    use_minutes : bool = False

    @type_safe
    def s3_path(self, year: int, month: int, day: int, hour: int, file_id: Safe_Id):
        return f'{year:04}/{month:02}/{day:02}/{hour:02}/{file_id}.json'

    def s3_path__now(self, file_id: Safe_Id):
        year, month, day, hour = self.path__for_date_time__now_utc().split('/')
        return self.s3_path(year, month, day, hour, file_id)


