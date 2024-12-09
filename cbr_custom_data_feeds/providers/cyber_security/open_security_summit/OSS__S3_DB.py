from cbr_custom_data_feeds.config.Custom_News__Shared_Constants import S3_FILE_NAME__RAW__CONTENT
from cbr_custom_data_feeds.data_feeds.Data_Feeds__S3_DB             import Data_Feeds__S3_DB
from cbr_custom_data_feeds.data_feeds.models.Model__Data_Feeds__Providers import Model__Data_Feeds__Providers
from osbot_utils.decorators.methods.type_safe                       import type_safe
from osbot_utils.utils.Http import url_join_safe


class OSS__S3_DB(Data_Feeds__S3_DB):

    @type_safe
    def raw_content__save(self, raw_data:list):
        s3_path = self.s3_path__raw_content__now()
        s3_key = self.s3_key__for_path__oss_data(s3_path)
        self.s3_save_data(raw_data, s3_key)
        return dict(s3_path=s3_path)

    # methods for s3 folders and files

    def s3_folder__for_oss_data(self):
        return self.s3_key_generator.s3_folder__for_area(area=Model__Data_Feeds__Providers.OPEN_SECURITY_SUMMIT)

    def s3_path__raw_content__now(self):
        return self.s3_key_generator.s3_path__now(file_id=S3_FILE_NAME__RAW__CONTENT)

    def s3_key__for_path__oss_data(self, s3_path):
        return url_join_safe(self.s3_folder__for_oss_data(), s3_path)