from unittest                                                                                   import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.llms.Hacker_News__Execute_LLM__With_Cache  import Hacker_News__Execute_LLM__With_Cache
from myfeeds_ai.providers.cyber_security.hacker_news.llms.prompts.LLM__Prompt__Extract_Entities import LLM__Prompt__Extract_Entities
from osbot_utils.helpers.llms.schemas.Schema__LLM_Response                                      import Schema__LLM_Response
from tests.integration.data_feeds__objs_for_tests                                               import myfeeds_tests__setup_local_stack


class test_LLM__Prompt__Extract_Entities(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        #load_dotenv()
        cls.prompt_extract_entities = LLM__Prompt__Extract_Entities()
        cls.execute_llm_with_cache  = Hacker_News__Execute_LLM__With_Cache().setup()

    def test_llm_request(self):
        with self.prompt_extract_entities as _:
            text = "There was a GDPR fine issued in Lisbon, to a FinTech organisation in Mar 2025."
            #text = "There was a GDPR fine"
            llm_request = _.llm_request(text)

            llm_response = self.execute_llm_with_cache.execute__llm_request(llm_request)
            if llm_response:
                assert type(llm_response) is Schema__LLM_Response
                entities = _.process_llm_response(llm_response)
                #entities.entities = entities.entities[0:4]
                #pprint(entities.json())
                #_.create_graph(entities)




