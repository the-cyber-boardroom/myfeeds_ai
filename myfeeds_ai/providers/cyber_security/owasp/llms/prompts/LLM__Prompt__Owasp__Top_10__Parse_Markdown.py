from myfeeds_ai.providers.cyber_security.owasp.schemas.Schema__Owasp__Top_10__Category import Schema__Owasp__Top_10__Category
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI                   import LLM_Request__Builder__Open_AI
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response                             import Schema__LLM_Response
from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                                        import type_safe
from osbot_utils.utils.Json                                                            import str_to_json

system_prompt = """\
You are a specialized OWASP Top 10 parser that extracts structured information 
from OWASP Top 10 category markdown.

Your task is to parse the provided markdown content and extract all relevant 
information for an OWASP Top 10 risk category.

For each category, extract the following:
1. Identifier (e.g., "A01:2021")
2. Name (e.g., "Broken Access Control")
3. Factors (statistical metrics)
4. Overview section
5. Detailed description  (intro paragraph and bullet points)
6. Prevention information (intro paragraph and bullet points)
7. Example attack scenarios with any code examples
8. References (titles and URLs)
9. Mapped CWEs (identifiers, names, and URLs)
10. Previous name if mentioned

Ensure you maintain the original formatting and content where appropriate, 
especially in code examples and descriptions.

Format your response according to the Schema__OWASP__Top10_Risk structure 
with all required fields.
"""

class LLM__Prompt__Owasp__Top_10__Parse_Markdown(Type_Safe):
    request_builder: LLM_Request__Builder__Open_AI

    def llm_request(self, category_markdown) -> dict:
        with self.request_builder as _:
            _.set__model__gpt_4o_mini()
            _.add_message__system(system_prompt)
            _.add_message__user  (category_markdown)
            _.set__function_call(parameters=Schema__Owasp__Top_10__Category, function_name='extract_entities')

        return self.request_builder.llm_request()

    @type_safe
    def process_llm_response(self, llm_response: Schema__LLM_Response):
        content      = llm_response.obj().response_data.choices[0].message.content
        content_json = str_to_json(content)
        return Schema__Owasp__Top_10__Category.from_json(content_json)