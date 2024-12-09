from cbr_custom_data_feeds.data_feeds.Data_Feeds__S3_DB             import Data_Feeds__S3_DB
from osbot_utils.decorators.methods.type_safe                       import type_safe


class OSS__S3_DB(Data_Feeds__S3_DB):

    @type_safe
    def raw_content__save(self, raw_data:list):
        return len(raw_data)
