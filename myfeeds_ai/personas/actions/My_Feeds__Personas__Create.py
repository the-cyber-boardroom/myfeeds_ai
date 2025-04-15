from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Nodes import Schema__MGraph__RAG__Node__Text_Id
from myfeeds_ai.personas.actions.My_Feeds__Personas                                                 import My_Feeds__Personas
from myfeeds_ai.personas.llms.LLM__Prompt__Personas__Extract_Entities                               import LLM__Prompt__Personas__Extract_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Text__Entities                                    import Schema__Persona__Text__Entities
from myfeeds_ai.providers.cyber_security.hacker_news.llms.Hacker_News__Execute_LLM__With_Cache      import Hacker_News__Execute_LLM__With_Cache
from osbot_utils.decorators.methods.cache_on_self                                                   import cache_on_self
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe

from osbot_utils.utils.Dev import pprint


class My_Feeds__Personas__Create(Type_Safe):
    prompt_extract_entities : LLM__Prompt__Personas__Extract_Entities
    personas                : My_Feeds__Personas

    def create_tree_values_from_entities(self, text_entities):
        if text_entities:
            root_id_type = Schema__MGraph__RAG__Node__Text_Id
            graph_rag    = self.prompt_extract_entities.create_entities_graph_rag(text_entities)
            text_ids     = graph_rag.mgraph_entity.index().get_nodes_by_type(root_id_type)
            tree_values  = graph_rag.mgraph_entity.export().export_tree_values().as_text(list(text_ids))
            return tree_values

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