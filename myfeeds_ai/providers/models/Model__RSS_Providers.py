from typing                                          import Dict
from osbot_utils.helpers.Safe_Id                     import Safe_Id
from myfeeds_ai.providers.models.Model__RSS_Provider import Model__RSS_Provider
from osbot_utils.type_safe.Type_Safe                  import Type_Safe

class Model__RSS_Providers(Type_Safe):
    providers: Dict[Safe_Id,Model__RSS_Provider]