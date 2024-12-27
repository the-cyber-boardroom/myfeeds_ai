from osbot_aws.aws.cloud_front.Cloud_Front import Cloud_Front

from osbot_utils.utils.Env import get_env

from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator         import Data_Feeds__S3__Key_Generator
from myfeeds_ai.data_feeds.Data_Feeds__Shared_Constants          import S3_FOLDER_NAME__LATEST, S3_BUCKET_PREFIX__DATA_FEEDS, S3_BUCKET_SUFFIX__HACKER_NEWS, S3_FILE_NAME__LATEST__VERSIONS
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Providers   import Model__Data_Feeds__Providers
from osbot_aws.aws.s3.S3__DB_Base                                           import S3__DB_Base
from osbot_utils.decorators.methods.type_safe                               import type_safe
from osbot_utils.helpers.Safe_Id                                            import Safe_Id
from osbot_utils.utils.Http                                                 import url_join_safe

ENV_NAME__AWS__CLOUDFRONT__DISTRIBUTION_ID = 'AWS__CLOUDFRONT__DISTRIBUTION_ID'

class Data_Feeds__S3_DB(S3__DB_Base):
    bucket_name__prefix   : str                          = S3_BUCKET_PREFIX__DATA_FEEDS
    bucket_name__suffix   : str                          = S3_BUCKET_SUFFIX__HACKER_NEWS
    save_as_gz            : bool
    provider_name         : Model__Data_Feeds__Providers
    s3_key_generator      : Data_Feeds__S3__Key_Generator

    def provider__all_files(self):
        return sorted(self.s3_folder_files__all(folder=self.s3_folder__for_provider(), full_path=False))

    # todo: refactor this to a better location and wire this up to the latest folder
    def invalidate_cache(self):
        distribution_id = get_env(ENV_NAME__AWS__CLOUDFRONT__DISTRIBUTION_ID)
        target_path = '/public-data/hacker-news/latest/*'
        cloud_front = Cloud_Front()
        result = cloud_front.invalidate_path(distribution_id, target_path)
        return result.get('Invalidation')

    # methods for s3 folders and files
    def s3_folder__for_provider(self):
        return self.s3_key_generator.s3_folder__for_area(area=self.provider_name)

    def s3_folder__for_latest(self):
        return S3_FOLDER_NAME__LATEST

    def s3_path__exists(self, s3_path):
        s3_key= self.s3_key__for_provider_path(s3_path)
        return self.s3_file_exists(s3_key)

    @type_safe
    def s3_path__in_latest(self, file_id: Safe_Id):
        return url_join_safe(self.s3_folder__for_latest(), file_id + '.json')

    def s3_path__latest_versions(self):
        return url_join_safe(self.s3_folder__for_latest(), S3_FILE_NAME__LATEST__VERSIONS + '.json')

    def s3_key__for_provider_path(self, s3_path):
        return url_join_safe(self.s3_folder__for_provider(), s3_path)
