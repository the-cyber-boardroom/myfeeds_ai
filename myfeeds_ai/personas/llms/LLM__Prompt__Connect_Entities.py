from typing                                                                   import Dict, Any

from myfeeds_ai.personas.llms.Schema__Persona__Connected_Entities             import Schema__Persona__Connected_Entities
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI          import LLM_Request__Builder__Open_AI
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request                     import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response                    import Schema__LLM_Response
from osbot_utils.type_safe.Type_Safe                                          import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                               import type_safe
from osbot_utils.utils.Json                                                   import str_to_json

SYSTEM_PROMPT__CONNECT_ENTITIES = """You are a cybersecurity knowledge graph matching expert that determines relevance between 
news articles and professional personas. The key objective is to map out the connections between the two graphs, so that 
a personalised cyber security news feed can be created (with full provenance and explainability)"

Your task is to carefully analyze two knowledge graphs:
1. A persona interest graph - representing the areas of interest, responsibilities, and context for a specific 
   professional role (like a CISO)
2. Multiple news articles entity graphs - representing the entities, concepts, and relationships extracted from recent 
   cybersecurity news articles

For the best 5 to 10 article's scores:
    1. Identify primary entities in the news that match the persona's areas of responsibility
    2. Map key relationships that are relevant to the persona's interests
    3. Determine a relevance score from 0-10, where:
       - 0-2: Not relevant to this persona
       - 3-5: Somewhat relevant but not a priority
       - 6-8: Highly relevant to this persona's role
       - 9-10: Critical information requiring immediate attention
    4. Provide a specific explanation of why this article matters to this persona
    5. Identify which specific persona responsibilities this article is most relevant to

Be specific, precise, and focus on semantic matches even when terminology differs.
"""

USER_PROMPT__CONNECT_ENTITIES = """\
Analyze the following persona interest graph and news articles graph to determine relevance:

======================== PERSONA INTEREST GRAPH ========================:
<Start>
{persona_graph_tree}
<END>
========================================================================

======================== NEWS ARTICLES GRAPH ============================:
<Start>
{articles_graph_tree}
<END>
========================================================================


For the top 5 to 10 articles, identify:
1. Primary entities in the news that match the persona's areas of responsibility
2. Key relationships that are relevant to the persona's interests
3. A relevance score from 0-10 with explanation
4. Which specific persona responsibilities this article is most relevant to
5. Identify the Article ID (the root node of each tree)
"""

class LLM__Prompt__Connect_Entities(Type_Safe):
    request_builder: LLM_Request__Builder__Open_AI

    def llm_request(self, persona_graph_tree: str, articles_graph_tree: str) -> Schema__LLM_Request:
        system_prompt = SYSTEM_PROMPT__CONNECT_ENTITIES
        user_prompt   = USER_PROMPT__CONNECT_ENTITIES.format(**dict(persona_graph_tree=persona_graph_tree, articles_graph_tree=articles_graph_tree))

        with self.request_builder as _:
            _.set__model__gpt_4o_mini()  # Using GPT-4o for advanced reasoning
            _.add_message__system(system_prompt)
            _.add_message__user  (user_prompt)
            _.set__function_call(parameters=Schema__Persona__Connected_Entities, function_name='assess_relevance')

        return self.request_builder.llm_request()

    @type_safe
    def process_llm_response(self, llm_response: Schema__LLM_Response) -> Schema__Persona__Connected_Entities: # Process the LLM response into a structured relevance assessment.
        content = llm_response.obj().response_data.choices[0].message.content
        content_json = str_to_json(content)
        return Schema__Persona__Connected_Entities.from_json(content_json)