from typing                                                                         import List
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage   import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage__Article import \
    Hacker_News__Storage__Article
from osbot_utils.decorators.methods.cache_on_self                                   import cache_on_self
from osbot_utils.helpers.Obj_Id                                                     import Obj_Id
from osbot_utils.helpers.Safe_Id                                                    import Safe_Id

S3_FOLDER_NAME__ENTITIES = 'entities'

class Hacker_News__Storage__Article__Entity(Hacker_News__Storage__Article):
    #entity_id : Obj_Id

    @cache_on_self
    def areas(self) -> List[Safe_Id]:
        return super().areas() + [Safe_Id(S3_FOLDER_NAME__ENTITIES)]