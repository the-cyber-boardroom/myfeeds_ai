from myfeeds_ai.personas.llms.Schema__Persona__Digest_Articles                  import Schema__Persona__Digest_Articles
from myfeeds_ai.personas.schemas.Schema__Persona                                import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__Articles__Connected_Entities  import Schema__Persona__Articles__Connected_Entities
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI            import LLM_Request__Builder__Open_AI
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request                       import Schema__LLM_Request
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response                      import Schema__LLM_Response
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                                 import type_safe
from osbot_utils.utils.Json                                                     import str_to_json

SYSTEM_PROMPT__CREATE_DIGEST = """You are a specialized cybersecurity news analyst creating highly personalized digests for professionals across various security and leadership roles.

Your primary task is to analyze the semantic relationships between news articles and the recipient's knowledge graph to create a role-tailored briefing that connects directly to their specific domains of interest and responsibility.

For the executive summary structure:
   - An introductory paragraph providing a high-level overview of key developments relevant to this persona
   - 2-3 domain-specific paragraphs organized by key responsibility areas relevant to this persona, each with:    
       * A clear section header using a title that is relevant to the current persona/role
       * A paragraph that connects the news to specific entities and responsibilities from the persona description
   - Information emphasis and terminology matched to this persona's role and decision-making needs
   - Factual information without assumptions about internal implementation state

For each article:
    - A clear, persona-relevant headline
    - Extract the key information most relevant to the persona's specific focus areas       
    - Concise summary highlighting only the most relevant information
    - Brief explanation of why this specifically matters to this persona
    - Role-specific action recommendations based on this news
   
Your digest should:
    - Adapt its structure, terminology, and emphasis based on the specific persona type
    - Prioritize articles based on their relevance score and critical nature
    - Provide insights relevant to the persona's decision-making context (strategic for executives, tactical for practitioners, etc.)
    - Match the level of technical detail to the persona's expertise and information needs
    - Maintain a professional tone appropriate for the persona's organizational level
    - Conclude with strategic implications connecting these news items to the persona's responsibilities
    - When available, make sure to include the author, article source, image link and when it was published 

This news digest must be professional and focused exclusively on what matters to this specific persona's role and responsibilities.
"""

USER_PROMPT__CREATE_DIGEST = """\
Create a personalized cybersecurity news digest based on the system prompt instructions for the following persona and articles:

PERSONA TYPE: {persona_type}

======================== PERSONA DESCRIPTION ========================:
<Start>
{persona_description}
<END>
========================================================================



These articles have been selected as relevant to this persona with the following matching data:

====================== How the articles relate to the persona ==========
<Start>
{connected_entities_data}
<END>
=========================================================================

====================== Full article contents (in Markdown): ==========

<Start>
{articles_content}
<END>
=========================================================================
"""


class LLM__Prompt__Personas__Create_Digest(Type_Safe):
    request_builder: LLM_Request__Builder__Open_AI

    def format_articles_content(self, persona_connected_entities: Schema__Persona__Articles__Connected_Entities) -> str:  # Format all the article markdown content into a structured text for the prompt.
        content_sections = []

        for article_id, article_markdown in persona_connected_entities.articles_markdown.items():
            content_sections.append(f"ARTICLE ID: {article_id}\n{article_markdown}")

        return "\n\n-----\n\n".join(content_sections)

    def format_connected_entities_data(self, persona_connected_entities: Schema__Persona__Articles__Connected_Entities) -> str:   # Format the entity connection data for better LLM understanding.
        sections = []

        for connected_entity in persona_connected_entities.connected_entities:
            section  = f"ARTICLE ID: {      connected_entity.article_id}\n"
            section += f"RELEVANCE SCORE: { connected_entity.overall_score}/10\n"
            section += f"PRIORITY LEVEL: {  connected_entity.priority_level}\n"
            section += f"PRIMARY RELEVANCE AREAS: {', '.join(connected_entity.primary_relevance)}\n"
            section += f"RELEVANCE SUMMARY: {connected_entity.relevance_summary}\n"
            section += "KEY ENTITY MATCHES:\n"
            for match in connected_entity.entity_matches:
                section += f"- Persona's '{match.persona_entity}' connects to article's '{match.article_entity}'\n"
                section += f"  Context: {match.persona_context} → {match.article_context}\n"

            sections.append(section)

        return "\n\n".join(sections)

    @type_safe
    def llm_request(self, persona                   : Schema__Persona,
                          persona_connected_entities: Schema__Persona__Articles__Connected_Entities,
                     ) -> Schema__LLM_Request:                                                      # Generate LLM request for creating a personalized digest."""
        system_prompt           = SYSTEM_PROMPT__CREATE_DIGEST
        persona_description     = persona.description
        persona_type            = persona.persona_type
        connected_entities_data = self.format_connected_entities_data(persona_connected_entities)
        articles_content        = self.format_articles_content       (persona_connected_entities)

        user_prompt = USER_PROMPT__CREATE_DIGEST.format(persona_description     = persona_description    ,
                                                        persona_type            = persona_type.value     ,
                                                        connected_entities_data = connected_entities_data,
                                                        articles_content        = articles_content       )

        with self.request_builder as _:
            _.set__model__gpt_4o()                               # For this final step use the more expensive GPT-4o
            #_.set__model__gpt_4_1()                              # trying the new 4.1 model
            #_.set__model__gpt_4_1_mini()
            _.add_message__system    (system_prompt)
            _.add_message__user      (user_prompt)
            _.set__function_call     (parameters=Schema__Persona__Digest_Articles, function_name='create_digest')

        return self.request_builder.llm_request()

    @type_safe
    def process_llm_response(self, llm_response: Schema__LLM_Response) -> Schema__Persona__Digest_Articles:             # Process the LLM response into a structured digest.
        content = llm_response.obj().response_data.choices[0].message.content
        content_json = str_to_json(content)
        return Schema__Persona__Digest_Articles.from_json(content_json)