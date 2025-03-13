from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI import LLM_Request__Builder__Open_AI
from osbot_utils.type_safe.Type_Safe                                 import Type_Safe

content_prompt = """You are a comprehensive knowledge extractor that maps entities into a rich semantic network.
For each entity:
    1. Identify its core essence and domain classifications
    2. Map its functional roles (keep these brief and specific)
    3. Identify its technical ecosystem and standards
    4. Map both direct relationships (from the text) and broader knowledge relationships

Be specific and precise. Avoid descriptions - focus on relationships and classifications.
Return only valid JSON with no additional text.
"""

class LLM__Prompt__Extract_Entities(Type_Safe):
    request_builder: LLM_Request__Builder__Open_AI

    def llm_request(self, text) -> dict:
        with self.request_builder as _:
            _.set__model__gpt_4o_mini()
            _.add_message__user(text)
        return self.request_builder.llm_request()