from cbr_custom_data_feeds.config.Custom_News__Shared_Constants import S3_BUCKET_PREFIX__DATA_FEEDS, S3_BUCKET_SUFFIX__HACKER_NEWS
from osbot_aws.aws.s3.S3__DB_Base                               import S3__DB_Base


class Data_Feeds__S3_DB(S3__DB_Base):
    bucket_name__prefix   : str                = S3_BUCKET_PREFIX__DATA_FEEDS
    bucket_name__suffix   : str                = S3_BUCKET_SUFFIX__HACKER_NEWS
    save_as_gz            : bool