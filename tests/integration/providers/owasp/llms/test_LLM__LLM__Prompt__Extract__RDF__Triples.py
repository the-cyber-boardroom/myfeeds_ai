import pytest
from unittest                                                                                           import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.llms.Hacker_News__Execute_LLM__With_Cache          import Hacker_News__Execute_LLM__With_Cache
from myfeeds_ai.providers.cyber_security.owasp.actions.Owasp__Files__Top_10                             import Owasp__Files__Top_10
from myfeeds_ai.providers.cyber_security.owasp.llms.prompts.LLM__Prompt__Extract__Ontology import \
    LLM__Prompt__Extract__Ontology, Schema__RDF__Ontology
from myfeeds_ai.providers.cyber_security.owasp.llms.prompts.LLM__Prompt__Extract__RDF_Triples import \
    LLM__Prompt__Extract__RDF_Triples, Schema__RDF__Triples
from myfeeds_ai.providers.cyber_security.owasp.llms.prompts.LLM__Prompt__Extract__Taxonomy import \
    LLM__Prompt__Extract__Taxonomy, Schema__RDF__Taxonomy
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Category                          import Owasp__Top_10__Category
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI                                       import ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response                                              import Schema__LLM_Response
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env                                                                              import get_env
from osbot_utils.utils.Json import json_to_str
from tests.integration.data_feeds__objs_for_tests                                                       import myfeeds_tests__setup_local_stack

class test_LLM__LLM__Prompt__Extract__RDF__Triples(TestCase):

    @classmethod
    def setUpClass(cls):
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip('This test requires OpenAI API Key to run')
        myfeeds_tests__setup_local_stack()
        #load_dotenv()
        cls.owasp_files_top_10          = Owasp__Files__Top_10()
        cls.category                  = Owasp__Top_10__Category.A01_2021__BROKEN_ACCESS_CONTROL
        #cls.category                    = Owasp__Top_10__Category.A02_2021__CRYPTOGRAPHIC_FAILURES
        cls.category                    = Owasp__Top_10__Category.A03_2021__INJECTION
        cls.category_markdown_json      = cls.owasp_files_top_10.raw_data__json(cls.category)
        cls.prompt_extract_ontology     = LLM__Prompt__Extract__Ontology   ()
        cls.prompt_extract_taxonomy     = LLM__Prompt__Extract__Taxonomy   ()
        cls.prompt_extract_rdf_triples  = LLM__Prompt__Extract__RDF_Triples()
        cls.execute_llm_with_cache      = Hacker_News__Execute_LLM__With_Cache().setup()

    def get_text_to_parse(self) -> str:

        with self.category_markdown_json as _:
            data_to_parse = dict(name        = _.name              ,
                                 description = _.description.json())
            text_to_parse = json_to_str(data_to_parse)
        return text_to_parse

    def get_text_ontology(self, text_to_parse) -> Schema__RDF__Ontology:
        with self.prompt_extract_ontology as _:
            llm_request  = _.llm_request(text_to_parse)
            llm_response = self.execute_llm_with_cache.execute__llm_request(llm_request)
            ontology     = _.process_llm_response(llm_response)
            return ontology.json()

    def get_text_taxonomy(self, text_to_parse, ontology) -> Schema__RDF__Ontology:
        with self.prompt_extract_taxonomy as _:
            llm_request  = _.llm_request(text_to_parse, ontology)
            llm_response = self.execute_llm_with_cache.execute__llm_request(llm_request)
            taxonomy     = _.process_llm_response(llm_response)
            return taxonomy.json()


    def test_llm_request(self):
        with self.prompt_extract_rdf_triples as _:
            text_to_parse = self.get_text_to_parse()
            ontology      = self.get_text_ontology(text_to_parse)
            taxonomy      = self.get_text_taxonomy(text_to_parse, ontology)

            llm_request = _.llm_request(text_to_parse, ontology, taxonomy)

            llm_response = self.execute_llm_with_cache.execute__llm_request(llm_request)

            if llm_response:
                rdf_triples = _.process_llm_response(llm_response)
                assert type(llm_response)   is Schema__LLM_Response
                assert type(rdf_triples)    is Schema__RDF__Triples
                #pprint(rdf_triples)
                #pprint(taxonomy.json())


