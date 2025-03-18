from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                    import S3_Key__File_Extension
from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage import My_Feeds__Personas__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage__Article  import Hacker_News__Storage__Article
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File import Hacker_News__File
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Now           import Hacker_News__File__Now
from osbot_utils.helpers.Obj_Id                                                             import Obj_Id
from osbot_utils.helpers.Safe_Id                                                            import Safe_Id


class My_Feeds__Personas__File(Hacker_News__File):

    def __init__(self,  **kwargs):
        self.hacker_news_storage = My_Feeds__Personas__Storage()
        super().__init__(**kwargs)