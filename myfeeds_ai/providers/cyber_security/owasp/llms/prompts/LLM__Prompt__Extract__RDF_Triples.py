from typing                                                          import List, Dict, Any, Optional
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI import LLM_Request__Builder__Open_AI
from osbot_utils.type_safe.Type_Safe                                 import Type_Safe
from osbot_utils.utils.Json                                          import str_to_json


class Schema__RDF__Entity(Type_Safe):
    """An entity in the RDF graph with explicit typing"""
    value: str  # The entity name
    type: str   # The ontological type


class Schema__RDF__Triple(Type_Safe):
    """A typed RDF triple with subject and object having explicit types"""
    subject: Schema__RDF__Entity
    predicate: str
    object: Schema__RDF__Entity


class Schema__RDF__Triples(Type_Safe):
    """Collection of typed RDF triples"""
    triples: List[Schema__RDF__Triple]


system_prompt = """
You are a knowledge graph engineer specializing in cybersecurity. Your task is to extract semantic triples from the provided text using the previously defined ontology and taxonomy.

REQUIREMENTS:
1. Generate RDF triples that conform to the ontology's class and relationship definitions.
2. Ensure entities are properly typed according to the ontology classes.
3. Follow the domain and range constraints of relationships defined in the ontology.
4. Use the taxonomy to ensure consistent naming of similar concepts.
5. Ensure the knowledge graph is fully connected without isolated nodes.
6. Use Upper Snake Case for entity names (Like_This)
7. Use lower_snake_case for relationship names (like_this)

RELATIONSHIP DIRECTIONALITY:
For each relationship type, follow the specified domain and range constraints from the ontology exactly.

Your output must be a list of semantic triples where subjects and objects are properly typed according to the ontology.
"""


class LLM__Prompt__Extract__RDF_Triples(Type_Safe):
    request_builder: LLM_Request__Builder__Open_AI

    def llm_request(self, text_content: str, ontology: Dict[str, Any], taxonomy: Dict[str, Any]) -> dict:
        input_message = f"""
Text to analyze:
{text_content}

Previously extracted ontology:
{ontology}

Previously extracted taxonomy:
{taxonomy}

Based on this text, ontology, and taxonomy, 
extract RDF triples that form a consistent and complete knowledge graph.
"""

        with self.request_builder as _:
            _.set__model__gpt_4_1()
            #_.set__model__gpt_4_1_mini()
            #_.set__model__gpt_4o()
            _.add_message__system(system_prompt)
            _.add_message__user(input_message)
            _.set__function_call(parameters=Schema__RDF__Triples, function_name='extract_rdf_triples')

        return self.request_builder.llm_request()

    def process_llm_response(self, llm_response):
        """Process the LLM response to extract the RDF triples"""
        content = llm_response.obj().response_data.choices[0].message.content
        content_json = str_to_json(content)
        #return content_json
        return Schema__RDF__Triples.from_json(content_json)