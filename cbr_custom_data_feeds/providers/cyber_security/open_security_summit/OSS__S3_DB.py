from cbr_custom_data_feeds.data_feeds.Data_Feeds__S3_DB                         import Data_Feeds__S3_DB
from cbr_custom_data_feeds.data_feeds.Data__Feeds__Shared_Constants             import S3_FILE_NAME__RAW__CONTENT
from cbr_custom_data_feeds.data_feeds.models.Model__Data_Feeds__Providers       import Model__Data_Feeds__Providers
from cbr_custom_data_feeds.data_feeds.models.Model__Data_Feeds__Raw_Data        import Model__Data_Feeds__Raw_Data
from osbot_utils.decorators.methods.type_safe                                   import type_safe


class OSS__S3_DB(Data_Feeds__S3_DB):
    provider_name = Model__Data_Feeds__Providers.OPEN_SECURITY_SUMMIT

    @type_safe
    def raw_content__save(self, raw_data:Model__Data_Feeds__Raw_Data):
        s3_path               = self.s3_path__raw_content__now()
        s3_key                = self.s3_key__for_provider_path(s3_path)
        raw_data.storage_path = s3_path
        file_data             = raw_data.json()
        self.s3_save_data(file_data, s3_key)
        return dict(s3_path=s3_path)

    def raw_content__load__now(self):
        s3_path   = self.s3_path__raw_content__now()
        s3_key    = self.s3_key__for_provider_path(s3_path)
        file_data = self.s3_file_data(s3_key)
        return Model__Data_Feeds__Raw_Data.from_json(file_data)



    def s3_path__raw_content__now(self):
        return self.s3_key_generator.s3_path__now(file_id=S3_FILE_NAME__RAW__CONTENT)
