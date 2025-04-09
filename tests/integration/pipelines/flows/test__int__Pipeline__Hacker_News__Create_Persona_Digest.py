from unittest import TestCase

import pytest

from myfeeds_ai.personas.schemas.Schema__Persona__Types import Schema__Persona__Types
from myfeeds_ai.pipelines.flows.Pipeline__Hacker_News__Create_Persona_Digest import Pipeline__Hacker_News__Create_Persona_Digest
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI import ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.utils.Env import get_env
from tests.integration.data_feeds__objs_for_tests import myfeeds_tests__setup_local_stack


class test__int__Pipeline__Hacker_News__Create_Persona_Digest(TestCase):

    @classmethod
    def setUpClass(cls):
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip('This test requires OpenAI API Key to run')
        myfeeds_tests__setup_local_stack()

        cls.pipline_create_persona_digest = Pipeline__Hacker_News__Create_Persona_Digest()
        cls.target_persona                = Schema__Persona__Types.EXEC__CISO

    def test_create_persona_digest(self):
        with self.pipline_create_persona_digest as _:
            #_.task__1__execute_flow_1__create_persona    ()
            #_.task__2__execute_flow_2__connected_entities()
            _.task__3__execute_flow_3__create_digest     ()
            _.task__n__create_output                     ()

            from osbot_utils.utils.Dev import pprint
            pprint(_.output)