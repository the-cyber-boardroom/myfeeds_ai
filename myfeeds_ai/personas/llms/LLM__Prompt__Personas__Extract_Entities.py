from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Entity            import Schema__Graph_RAG__Entity
from mgraph_db.providers.graph_rag.actions.Graph_RAG__Create_MGraph             import Graph_RAG__Create_MGraph
from myfeeds_ai.personas.schemas.Schema__Persona__Entities                      import Schema__Persona__Entities
from osbot_utils.helpers.Obj_Id import Obj_Id
from osbot_utils.helpers.llms.builders.LLM_Request__Builder__Open_AI            import LLM_Request__Builder__Open_AI
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response                      import Schema__LLM_Response
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                                 import type_safe
from osbot_utils.utils.Json                                                     import str_to_json

system_prompt = """You are a specialized cybersecurity knowledge graph extractor designed to create entities and relationships that can seamlessly connect with real-time cybersecurity news and threat intelligence.

ENTITY EXTRACTION GUIDELINES:
1. Extract entities from the text with a focus on cybersecurity relevance, including:
   - Security Roles (e.g., CISO, Security Analyst, Threat Hunter)
   - Organizations and Vendors (e.g., companies, security vendors, regulatory bodies)
   - Technology Assets (e.g., systems, platforms, software products that could be vulnerable)
   - Security Controls (e.g., tools, technologies used for protection)
   - Standards and Frameworks (e.g., NIST, ISO, CIS)
   - Regulations and Compliance Requirements (e.g., GDPR, PCI DSS)
   - Threat Categories (e.g., ransomware, phishing, supply chain attacks)
   - Vulnerability Classes (e.g., buffer overflow, SQL injection, authentication bypass)

2. Create these top-level categories as entity nodes:
   - "Roles" (security personnel and responsibilities)
   - "Organizations" (companies, agencies, vendors)
   - "Technologies/Systems" (potentially vulnerable systems)
   - "Standards and Frameworks" (security standards)
   - "Regulations" (compliance requirements)
   - "Process/Methodology" (security processes)
   - "Cybersecurity Threats/Vulnerabilities" (attack vectors, vulnerability classes)
   - "Security Controls" (protective measures)

3. Each entity must connect to its appropriate category with an "entity_type" relationship.

4. For technologies and systems, include granular details when available:
   - Specific product names rather than generic descriptions
   - Versions or categories that could be matched with CVEs
   - Vendor information where applicable

RELATIONSHIP EXTRACTION GUIDELINES:
1. Use these specific relationship types to ensure compatibility with news data:
   - "responsible_for" (security responsibility relationships)
   - "uses" (technology or tool usage)
   - "implements" (standard or framework adoption)
   - "complies_with" (regulatory compliance)
   - "protects_against" (security countermeasure relationship)
   - "works_with" (collaboration relationship)
   - "contains" (hierarchical relationship)
   - "affected_by" (vulnerability impact relationship)
   - "mitigates" (risk reduction relationship)
   - "detects" (threat detection capability)
   - "entity_type" (category classification)
   - "manages" (oversight responsibility)

2. For each protective control or technology, explicitly identify:
   - What threats or vulnerabilities it protects against
   - What technology assets it protects
   - Who is responsible for managing it

3. For security roles, clearly identify:
   - What technologies they're responsible for
   - What security processes they oversee
   - What compliance requirements they must address

Your output must create entities and relationships that could directly connect to cybersecurity news about vulnerabilities, threats, attacks, and security advisories. Focus on creating a knowledge graph that will remain relevant as new security information emerges.
"""

class LLM__Prompt__Personas__Extract_Entities(Type_Safe):
    request_builder: LLM_Request__Builder__Open_AI

    def llm_request(self, text) -> dict:
        extract_text = text
        with self.request_builder as _:
            _.set__model__gpt_4o_mini()
            _.llm_request_data.temperature = 1.0
            _.add_message__system(system_prompt)
            _.add_message__user  (extract_text)
            _.set__function_call(parameters=Schema__Persona__Entities, function_name='extract_entities')

        return self.request_builder.llm_request()

    @type_safe
    def process_llm_response(self, llm_response: Schema__LLM_Response):
        #pprint(llm_response.json())
        content      = llm_response.obj().response_data.choices[0].message.content
        content_json = str_to_json(content)
        return Schema__Persona__Entities.from_json(content_json)



    @type_safe
    def create_entities_graph_rag(self, entities: Schema__Persona__Entities):
        text_id = Obj_Id()
        graph_rag = Graph_RAG__Create_MGraph().setup()

        for entity in entities.entities:
            rag_entity = Schema__Graph_RAG__Entity.from_json(entity.json())
            rag_entity.text_id = text_id
            graph_rag.add_entity(rag_entity)
        return graph_rag
        #return graph_rag.screenshot__create_bytes()