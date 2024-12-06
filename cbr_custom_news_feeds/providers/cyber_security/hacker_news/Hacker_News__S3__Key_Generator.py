from osbot_aws.aws.s3.S3__Key_Generator         import S3__Key_Generator

S3_FOLDER__PUBLIC_DATA = 'public-data'

class Hacker_News__S3__Key_Generator(S3__Key_Generator):
    root_folder        = S3_FOLDER__PUBLIC_DATA
    split_when  : bool = True
    use_minutes : bool = False



