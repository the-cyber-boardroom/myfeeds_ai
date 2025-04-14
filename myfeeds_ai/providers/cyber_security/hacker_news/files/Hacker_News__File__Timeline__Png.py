from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                            import S3_Key__File__Extension, S3_Key__File__Content_Type
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News     import FILE_ID__TIMELINE__MGRAPH
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File        import Hacker_News__File


class Hacker_News__File__Timeline__Png(Hacker_News__File):
    file_id      = FILE_ID__TIMELINE__MGRAPH
    extension    = S3_Key__File__Extension.MGRAPH__PNG
    content_type = S3_Key__File__Content_Type.PNG