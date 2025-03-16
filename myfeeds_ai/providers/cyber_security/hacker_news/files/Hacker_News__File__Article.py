from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                    import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage__Article  import Hacker_News__Storage__Article
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Now           import Hacker_News__File__Now
from osbot_utils.helpers.Obj_Id                                                             import Obj_Id
from osbot_utils.helpers.Safe_Id                                                            import Safe_Id


class Hacker_News__File__Article(Hacker_News__File__Now):
    extension = S3_Key__File_Extension.JSON

    def __init__(self, article_id: Obj_Id, file_id:Safe_Id,  **kwargs):
        self.hacker_news_storage = Hacker_News__Storage__Article(article_id=article_id)
        super().__init__(file_id=file_id, **kwargs)