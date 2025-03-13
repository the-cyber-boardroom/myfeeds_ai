from unittest import TestCase

from myfeeds_ai.providers.cyber_security.hacker_news.llms.LLM__Prompt__Extract_Entities import \
    LLM__Prompt__Extract_Entities
from osbot_utils.utils.Dev import pprint


class test_LLM__Prompt__Extract_Entities(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.prompt_extract_entities = LLM__Prompt__Extract_Entities()

    def test_llm_payload(self):
        with self.prompt_extract_entities as _:
            llm_payload = _.llm_payload()
            assert llm_payload == {'messages': [], 'model': ''}
            #pprint(llm_payload)
