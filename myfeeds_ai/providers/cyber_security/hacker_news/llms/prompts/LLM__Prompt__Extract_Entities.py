from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity            import Schema__Graph_RAG__Entity
from mgraph_db.providers.graph_rag.actions.Graph_RAG__Create_MGraph             import Graph_RAG__Create_MGraph
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entities__LLMs    import Schema__Graph_RAG__Entities__LLMs
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI            import LLM_Request__Builder__Open_AI
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response                      import Schema__LLM_Response
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                                 import type_safe
from osbot_utils.utils.Json                                                     import str_to_json

system_prompt = """You are a comprehensive knowledge extractor that maps entities 
into a rich semantic network.

For each entity:
    1. Identify its core essence and domain classifications
    2. Map its functional roles (keep these brief and specific)
    3. Identify its technical ecosystem and standards
    4. Map both direct relationships (from the text) and broader knowledge relationships

Be specific and precise. Avoid descriptions - focus on relationships and classifications.

Extract at least 5 entities
"""

class LLM__Prompt__Extract_Entities(Type_Safe):
    request_builder: LLM_Request__Builder__Open_AI

    def llm_request(self, text) -> dict:
        #extract_text = f'Extract key entities from this text: {text}'
        extract_text = text
        with self.request_builder as _:
            _.set__model__gpt_4o_mini()
            _.add_message__system(system_prompt)
            _.add_message__user  (extract_text)
            _.set__function_call(parameters=Schema__Graph_RAG__Entities__LLMs, function_name='extract_entities')

        return self.request_builder.llm_request()

    @type_safe
    def process_llm_response(self, llm_response: Schema__LLM_Response):
        #pprint(llm_response.json())
        content      = llm_response.obj().response_data.choices[0].message.content
        content_json = str_to_json(content)
        return Schema__Graph_RAG__Entities__LLMs.from_json(content_json)

    # text_hash         = str_md5(text  )[:SIZE__TEXT__HASH]
    #         for entity_data in entities_data:
    #             entity           = Schema__Graph_RAG__Entity.from_json(entity_data)
    #             entity.text_hash = text_hash
    #             entity.text_id   = text_id
    #             entity.source_id = source_id
    #             entities.append(entity)

    @type_safe
    def create_entities_graph_rag(self, entities: Schema__Graph_RAG__Entities__LLMs):
        graph_rag = Graph_RAG__Create_MGraph().setup()

        for entity in entities.entities:
            rag_entity = Schema__Graph_RAG__Entity.from_json(entity.json())
            graph_rag.add_entity(rag_entity)
        return graph_rag
        #return graph_rag.screenshot__create_bytes()