from osbot_aws.aws.s3.S3__Key_Generator         import S3__Key_Generator
from osbot_aws.aws.s3.S3__DB_Base       import S3__DB_Base

S3_BUCKET_PREFIX__NEWS_FEEDS  = 'news-feeds'
S3_BUCKET_SUFFIX__HACKER_NEWS = 'hacker-news'


class Hacker_News__S3_DB(S3__DB_Base):
    bucket_name__prefix   : str                = S3_BUCKET_PREFIX__NEWS_FEEDS
    bucket_name__suffix   : str                = S3_BUCKET_SUFFIX__HACKER_NEWS
    save_as_gz            : bool
    s3_key_generator      : S3__Key_Generator