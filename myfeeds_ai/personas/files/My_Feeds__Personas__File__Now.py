from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage__Persona             import My_Feeds__Personas__Storage__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__Types                           import Schema__Persona__Types
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Now import Hacker_News__File__Now


class My_Feeds__Personas__File__Now(Hacker_News__File__Now):

    def __init__(self,  persona_type: Schema__Persona__Types, **kwargs):
        self.hacker_news_storage = My_Feeds__Personas__Storage__Persona(persona_type=persona_type)
        super().__init__(**kwargs)