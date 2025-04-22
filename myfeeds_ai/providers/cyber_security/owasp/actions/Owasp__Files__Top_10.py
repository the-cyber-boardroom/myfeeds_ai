from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator import S3_Key__File__Extension, S3_Key__File__Content_Type
from myfeeds_ai.providers.cyber_security.owasp.config.Config__Owasp import FILE_ID__RAW_DATA
from myfeeds_ai.providers.cyber_security.owasp.files.Owasp__File__Top_10 import Owasp__File__Top_10
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Category import Owasp__Top_10__Category
from osbot_utils.helpers.Safe_Id import Safe_Id
from osbot_utils.type_safe.Type_Safe import Type_Safe


class Owasp__Files__Top_10(Type_Safe):

    def file__category(self, category: Owasp__Top_10__Category):
        kwargs_file= dict(category     = category                           ,
                          file_id      = FILE_ID__RAW_DATA                  ,
                          extension    = S3_Key__File__Extension.MARKDOWN   ,
                          content_type = S3_Key__File__Content_Type.MARKDOWN)

        return Owasp__File__Top_10(**kwargs_file)

    def file__a01__broken_access_control__raw_Data(self):
        return self.file__category(Owasp__Top_10__Category.A01_2021__BROKEN_ACCESS_CONTROL)


