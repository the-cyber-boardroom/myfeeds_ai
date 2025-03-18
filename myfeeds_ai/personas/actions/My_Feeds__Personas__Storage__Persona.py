from typing import List

from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Providers import Model__Data_Feeds__Providers
from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage import My_Feeds__Personas__Storage
from myfeeds_ai.personas.schemas.Schema__Persona__Types import Schema__Persona__Types
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage   import Hacker_News__Storage
from osbot_utils.decorators.methods.cache_on_self                                   import cache_on_self
from osbot_utils.helpers.Safe_Id                                                    import Safe_Id

PROVIDER_NAME__PERSONAS = 'personas'

class My_Feeds__Personas__Storage__Persona(My_Feeds__Personas__Storage):
    persona_type: Schema__Persona__Types

    @cache_on_self
    def areas(self) -> List[Safe_Id]:
        return [Safe_Id(self.persona_type.value)]