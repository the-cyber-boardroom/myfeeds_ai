from typing                                                                       import List
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.owasp.files.Owasp__S3_DB                 import Owasp__S3_DB
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Category import Owasp__Top_10__Category
from osbot_utils.decorators.methods.cache_on_self                                 import cache_on_self
from osbot_utils.helpers.Safe_Id                                                  import Safe_Id


class Owasp__Storage(Hacker_News__Storage):
    s3_db   : Owasp__S3_DB
    project : Safe_Id
    year    : Safe_Id
    category: Owasp__Top_10__Category


    @cache_on_self
    def areas(self) -> List[Safe_Id]:
        category = Safe_Id(self.category.value)
        return [self.project, self.year, category]
