from myfeeds_ai.personas.actions.My_Feeds__Personas                                                 import My_Feeds__Personas
from myfeeds_ai.personas.llms.LLM__Prompt__Personas__Extract_Entities                               import LLM__Prompt__Personas__Extract_Entities
from myfeeds_ai.personas.schemas.Schema__Persona                                                    import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__Text__Entities                                    import Schema__Persona__Text__Entities
from myfeeds_ai.providers.cyber_security.hacker_news.llms.Hacker_News__Execute_LLM__With_Cache      import Hacker_News__Execute_LLM__With_Cache
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Text__Entities  import Schema__Feed__Article__Text__Entities
from osbot_utils.decorators.methods.cache_on_self                                                   import cache_on_self
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe

from osbot_utils.utils.Dev import pprint


class My_Feeds__Personas__Create(Type_Safe):
    prompt_extract_entities : LLM__Prompt__Personas__Extract_Entities
    personas                : My_Feeds__Personas

    def create_persona__ciso(self) -> Schema__Persona:
        file__persona__ciso = self.personas.file__persona__ciso()
        with self.personas.file__persona__ciso__load() as _:
            _.description           = PERSONA__DESCRIPTION__CISO
            _.path_now              = file__persona__ciso.path_now   ()
            _.path_latest           = file__persona__ciso.path_latest()
            _.description__entities = self.extract_entities_from_text(_.description).text_entities

            file__persona__ciso.save_data(_.json())
            return _

    @cache_on_self
    def execute_llm_with_cache(self) -> Hacker_News__Execute_LLM__With_Cache:
        return Hacker_News__Execute_LLM__With_Cache().setup()

    def extract_entities_from_text(self, text) -> Schema__Persona__Text__Entities:                                     # todo: move this to a separate class
        execute_llm_with_cache  = self.execute_llm_with_cache()
        llm_request             = self.prompt_extract_entities.llm_request                        (text       )
        llm_response            = execute_llm_with_cache .execute__llm_request                    (llm_request)
        text_entities           = self.prompt_extract_entities.process_llm_response               (llm_response)
        cache_entry             = execute_llm_with_cache.llm_cache.get__cache_entry__from__request(llm_request)
        cache_id                = cache_entry.cache_id
        request_duration        = cache_entry.request__duration
        timestamp               = cache_entry.timestamp
        kwargs_text_entities = dict(cache_id      = cache_id        ,
                                    duration      = request_duration,
                                    text          = text            ,
                                    text_entities = text_entities   ,
                                    timestamp     = timestamp       )
        article_text_entities = Schema__Persona__Text__Entities(**kwargs_text_entities)
        return article_text_entities


PERSONA__DESCRIPTION__CISO = ("The Chief Information Security Officer (CISO), who reports to the CEO,  at a FinTech company collaborates closely "
                              "with compliance officers and risk assessors to manage cybersecurity risks. "
                              "The company leverages Digital Payment Platforms, Mobile Banking Solutions, "
                              "and Identity and Access Management Systems, aligning with ISO/IEC 27001 and NIST Cybersecurity Framework. "
                              "They actively employ Intrusion Detection Systems, Data Loss Prevention Tools, Incident Management Tools, "
                              "and Security Information and Event Management (SIEM) platforms. Ensuring data protection through Privacy "
                              "Policies, Data Encryption, and Anonymisation Techniques, the CISO maintains regulatory compliance adhering to "
                              "GDPR, SOX, PCI DSS, and NIST SP 800-53 standards. Additionally, they utilize Threat Intelligence and Incident "
                              "Response strategies, supported by Security Analysts, Incident Responders, and Threat Hunters, to proactively "
                              "manage operational risks and information assurance.")