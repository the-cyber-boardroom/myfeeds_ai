from typing                                                          import List, Dict, Any, Optional
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI import LLM_Request__Builder__Open_AI
from osbot_utils.type_safe.Type_Safe                                 import Type_Safe
from osbot_utils.utils.Json                                          import str_to_json


class Schema__RDF__Taxonomy__Node(Type_Safe):
    """A node in the taxonomy hierarchy"""
    name         : str                          # Category name (e.g., "Broken_Access_Control")
    definition   : str                          # Definition of this category
    subcategories: List[str]                    # Array of child categories


class Schema__RDF__Taxonomy__Root(Type_Safe):
    """Root of a taxonomy hierarchy"""
    root: str                               # Root concept name (e.g., "Vulnerability_Category")
    description: str                        # Description of this taxonomy hierarchy
    hierarchy: Schema__RDF__Taxonomy__Node  # Nested hierarchy of concepts


class Schema__RDF__Taxonomy(Type_Safe):
    """Complete taxonomy with multiple hierarchies"""
    taxonomies: List[Schema__RDF__Taxonomy__Root]


system_prompt = """
You are a cybersecurity taxonomy specialist. Your task is to create a hierarchical taxonomy for cybersecurity concepts from the provided text and previously defined ontology.
 
REQUIREMENTS:
1. Create hierarchical classifications for each major class in the ontology.
2. Ensure consistent naming and relationships between parent and child concepts.
3. Use industry-standard terminology where applicable (OWASP, MITRE, etc.).
4. Use Upper Snake Case for all taxonomy terms (Like_This)
5. Return the taxonomy in a structured format.

Your taxonomy should organize concepts in logical hierarchies with clean parent-child relationships.

IMPORTANT: Base your taxonomy on the provided ontology, ensuring that all taxonomy terms are consistent with the ontology classes.
"""


class LLM__Prompt__Extract__Taxonomy(Type_Safe):
    request_builder: LLM_Request__Builder__Open_AI

    def llm_request(self, text_content: str, ontology: dict) -> dict:

        input_message = f"""
Text to analyze:
{text_content}

Previously extracted ontology:
{ontology}

Based on this text and ontology, create a comprehensive taxonomy. 
"""
        with self.request_builder as _:
            _.set__model__gpt_4_1()
            #_.set__model__gpt_4_1_mini()
            #_.set__model__gpt_4o()
            _.add_message__system(system_prompt)
            _.add_message__user(input_message)
            _.set__function_call(parameters=Schema__RDF__Taxonomy, function_name='extract_taxonomy')

        return self.request_builder.llm_request()

    def process_llm_response(self, llm_response):
        """Process the LLM response to extract the taxonomy"""
        content = llm_response.obj().response_data.choices[0].message.content
        content_json = str_to_json(content)
        return Schema__RDF__Taxonomy.from_json(content_json)
        #return content_json
