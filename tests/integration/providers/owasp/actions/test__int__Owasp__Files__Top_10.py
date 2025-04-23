from unittest import TestCase

import pytest

from myfeeds_ai.providers.cyber_security.owasp.actions.Owasp__Files__Top_10 import Owasp__Files__Top_10
from myfeeds_ai.providers.cyber_security.owasp.llms.prompts.LLM__Prompt__Extract__Ontology import Schema__RDF__Ontology
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Category import Owasp__Top_10__Category
from myfeeds_ai.providers.cyber_security.owasp.schemas.Schema__Owasp__Top_10__Category import \
    Schema__Owasp__Top_10__Category
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI import ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.utils.Env import get_env
from tests.integration.data_feeds__objs_for_tests import myfeeds_tests__setup_local_stack


class test__int__test_Owasp__Files__Top_10(TestCase):

    @classmethod
    def setUpClass(cls):
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip('This test requires OpenAI API Key to run')
        myfeeds_tests__setup_local_stack()
        cls.owasp_files_top_10 = Owasp__Files__Top_10()
        cls.category           = Owasp__Top_10__Category.A01_2021__BROKEN_ACCESS_CONTROL

    def test_a01__broken_access_control__raw_data__json(self):

        with self.owasp_files_top_10 as _:
            raw_data_json =  _.a01__broken_access_control__raw_data__json()
            assert type(raw_data_json) is Schema__Owasp__Top_10__Category

    def test_ontology(self):
        ontology = self.owasp_files_top_10.ontology(category=self.category)
        assert type(ontology) is Schema__RDF__Ontology

    # def test_taxonomy(self):
    #     ontology = self.owasp_files_top_10.ontology(category=self.category)
    #     #assert type(ontology) is Schema__RDF__Taxonomy