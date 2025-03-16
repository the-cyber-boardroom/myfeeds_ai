from datetime                                                   import datetime
from typing                                                     import List
from osbot_aws.aws.cloud_front.Cloud_Front                      import Cloud_Front
from osbot_utils.utils.Env                                      import get_env
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator        import Data_Feeds__S3__Key_Generator, S3_Key__File_Extension
from myfeeds_ai.data_feeds.Data_Feeds__Shared_Constants         import S3_FOLDER_NAME__LATEST, S3_BUCKET_PREFIX__DATA_FEEDS, S3_BUCKET_SUFFIX__HACKER_NEWS, S3_FILE_NAME__LATEST__VERSIONS
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Providers  import Model__Data_Feeds__Providers
from osbot_aws.aws.s3.S3__DB_Base                               import S3__DB_Base
from osbot_utils.type_safe.decorators.type_safe                 import type_safe
from osbot_utils.helpers.Safe_Id                                import Safe_Id
from osbot_utils.utils.Http                                     import url_join_safe

ENV_NAME__AWS__CLOUDFRONT__DISTRIBUTION_ID = 'AWS__CLOUDFRONT__DISTRIBUTION_ID'
CLOUDFRONT__INVALIDATION__TARGET_PATH      = '/public-data/hacker-news/latest/*'

class Data_Feeds__S3_DB(S3__DB_Base):
    bucket_name__prefix   : str                          = S3_BUCKET_PREFIX__DATA_FEEDS
    bucket_name__suffix   : str                          = S3_BUCKET_SUFFIX__HACKER_NEWS
    save_as_gz            : bool
    provider_name         : Model__Data_Feeds__Providers
    s3_key_generator      : Data_Feeds__S3__Key_Generator

    def provider__all_files(self):
        return sorted(self.s3_folder_files__all(folder=self.s3_folder__for_provider(), full_path=False))

    def invalidate_cache(self):
        distribution_id = get_env(ENV_NAME__AWS__CLOUDFRONT__DISTRIBUTION_ID)
        target_path     = CLOUDFRONT__INVALIDATION__TARGET_PATH
        cloud_front = Cloud_Front()
        result = cloud_front.invalidate_path(distribution_id, target_path)
        return result.get('Invalidation')

    # methods for paths
    @type_safe
    def s3_path__latest(self, file_id, extension: S3_Key__File_Extension):
        return url_join_safe(S3_FOLDER_NAME__LATEST, file_id + f'.{extension.value}')

    @type_safe
    def s3_path__in_latest(self, file_id: Safe_Id):
        return url_join_safe(self.s3_folder__for_latest(), file_id + '.json')

    def s3_path__latest_versions(self):
        return url_join_safe(self.s3_folder__for_latest(), S3_FILE_NAME__LATEST__VERSIONS + '.json')        # todo remove and use s3_path__in_latest

    @type_safe
    def s3_path__date_time(self, date_time : datetime,
                                 file_id   : Safe_Id               = None,
                                 extension: S3_Key__File_Extension = None,
                                 areas    : List[Safe_Id]          = None) -> str:
        return self.s3_key_generator.s3_path__date_time(date_time=date_time, file_id=file_id, extension=extension, areas=areas)

    @type_safe
    def s3_path__now(self, file_id: Safe_Id=None, extension: S3_Key__File_Extension=None, areas: List[Safe_Id] = None) -> str:
        return self.s3_key_generator.s3_path__now(file_id=file_id, extension=extension, areas=areas)

    # def s3_path__now_utc(self):
    #     return self.s3_key_generator.s3_path__now__utc()

    def s3_path__delete(self, s3_path) -> bool:
        s3_key = self.s3_key__for_provider_path(s3_path)
        result = self.s3_file_delete(s3_key=s3_key)
        return result

    def s3_path__files(self, s3_path, include_sub_folders=False):
        s3_key__now_utc = self.s3_key__for_provider_path(s3_path)
        return sorted(self.s3_folder_files(s3_key__now_utc, include_sub_folders=include_sub_folders))

    def s3_path__save_data(self, data, s3_path, content_type=None):
        s3_key = self.s3_key__for_provider_path(s3_path)
        result = self.s3_save_data(data=data, s3_key=s3_key, content_type=content_type)
        return result

    def s3_path__load_bytes(self, s3_path):
        s3_key = self.s3_key__for_provider_path(s3_path)
        return self.s3_file_bytes(s3_key)

    def s3_path__load_data(self, s3_path):
        s3_key = self.s3_key__for_provider_path(s3_path)
        return self.s3_file_data(s3_key)

    def s3_path__exists(self, s3_path):
        s3_key= self.s3_key__for_provider_path(s3_path)
        return self.s3_file_exists(s3_key)

    def s3_path__file_info(self, s3_path):
        s3_key= self.s3_key__for_provider_path(s3_path)
        return self.s3_file_info(s3_key)

    # methods for s3 folders
    def s3_folder__for_provider(self):
        return self.s3_key_generator.s3_folder__for_area(area=Safe_Id(self.provider_name.value))

    def s3_folder__for_date_time(self, date_time: datetime):
        return self.s3_key_generator.s3_folder__for_date_time(date_time=date_time)

    def s3_folder__for_latest(self):
        return S3_FOLDER_NAME__LATEST

    # methods for s3 keys
    def s3_key__for_provider_path(self, s3_path) -> str:
        return url_join_safe(self.s3_folder__for_provider(), s3_path)
