from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                            import S3_Key__File__Extension
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Now   import Hacker_News__File__Now
from myfeeds_ai.providers.cyber_security.owasp.files.Owasp__Storage                 import Owasp__Storage
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Projects__Folders     import Owasp__Projects__Folders
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Category      import Owasp__Top_10__Category
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Years                 import Owasp__Years
from osbot_utils.helpers.Safe_Id                                                    import Safe_Id

DEFAULT__AREA__PROJECT  = Safe_Id(Owasp__Projects__Folders.TOP_10                         .value)
DEFAULT__AREA__YEAR     = Safe_Id(Owasp__Years            .YEAR__2021                     .value)
DEFAULT__AREA__CATEGORY = Owasp__Top_10__Category.A01_2021__BROKEN_ACCESS_CONTROL

class Owasp__File__Top_10(Hacker_News__File__Now):
    extension            : S3_Key__File__Extension      = S3_Key__File__Extension.JSON
    project              : Safe_Id                      = DEFAULT__AREA__PROJECT
    year                 : Safe_Id                      = DEFAULT__AREA__YEAR
    category             : Owasp__Top_10__Category      = DEFAULT__AREA__CATEGORY

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hacker_news_storage = Owasp__Storage(project=self.project, year=self.year, category=self.category)