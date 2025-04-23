from typing                                                             import List
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI    import LLM_Request__Builder__Open_AI
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from osbot_utils.utils.Json                                             import str_to_json


class Schema__RDF__Ontology__Class(Type_Safe):
    name         : str      # Class name (e.g., "VulnerabilityCategory")
    definition  :  str      # Clear definition of what this class represents
    examples    : List[str] # 2-3 examples of instances of this class

class Schema__RDF__Ontology__Relationship(Type_Safe):
    name      : str         # Relationship name (e.g., "exploitedBy")
    definition: str         # Clear definition of what this relationship represents
    domain    : str         # Source class (e.g., "Vulnerability")
    range     : str         # Target class (e.g., "Attack")
    examples  : List[str]   # 2-3 examples of this relationship

class Schema__RDF__Ontology(Type_Safe):
    classes      : List[Schema__RDF__Ontology__Class       ]
    relationships: List[Schema__RDF__Ontology__Relationship]

system_prompt = """
You are a cybersecurity ontology engineer. Your task is to define a formal ontology for cybersecurity concepts from the provided text.

REQUIREMENTS:
1. Extract entity classes and relationship types from the text.
2. For each entity class, provide a clear definition and example instances.
3. For each relationship type, specify valid domain and range classes.
4. Use Upper Snake Case for all entity (Like_This)
5. Use Lower Snake Case for relationship names (like_this)

Your ontology should be comprehensive yet concise, covering all significant cybersecurity concepts in the text.
"""

class LLM__Prompt__Extract__Ontology(Type_Safe):
    request_builder: LLM_Request__Builder__Open_AI

    def llm_request(self, text_content) -> dict:
        with self.request_builder as _:
            _.set__model__gpt_4_1()
            #_.set__model__gpt_4_1_mini()
            #_.set__model__gpt_4o()
            _.add_message__system(system_prompt)
            _.add_message__user  (text_content )
            _.set__function_call(parameters=Schema__RDF__Ontology, function_name='extract_ontology')

        return self.request_builder.llm_request()

    def process_llm_response(self, llm_response):
        content = llm_response.obj().response_data.choices[0].message.content
        content_json = str_to_json(content)
        return Schema__RDF__Ontology.from_json(content_json)
        #return content_json
        # Alternative: return Schema__Knowledge_Graph.from_json(content_json)