import pytest
from unittest                                                                                   import TestCase
from myfeeds_ai.personas.config.Config__My_Feeds__Personas                                      import FILE_ID__PERSONA
from myfeeds_ai.personas.files.My_Feeds__Personas__File                                         import My_Feeds__Personas__File
from myfeeds_ai.personas.files.My_Feeds__Personas__File__Now                                    import My_Feeds__Personas__File__Now
from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__2__LLM__Connected_Entities             import Flow__My_Feeds__Personas__2__LLM__Connected_Entities
from myfeeds_ai.personas.schemas.Schema__Persona                                                import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__LLM__Connect_Entities                         import Schema__Persona__LLM__Connect_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Text__Entities                                import Schema__Persona__Text__Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                                         import Schema__Persona__Types
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File                    import Hacker_News__File
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Text_Entities__Files import Schema__Feed__Text_Entities__Files
from osbot_utils.helpers.Safe_Id                                                                import Safe_Id
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI                               import ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.utils.Env                                                                      import get_env
from tests.integration.data_feeds__objs_for_tests                                               import myfeeds_tests__setup_local_stack

from osbot_utils.utils.Dev import pprint

class test_Flow__My_Feeds__Personas__2__LLM__Connected_Entities(TestCase):

    @classmethod
    def setUpClass(cls):
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip('This test requires OpenAI API Key to run')
        myfeeds_tests__setup_local_stack()
        cls.flow_connect_entities = Flow__My_Feeds__Personas__2__LLM__Connected_Entities()

    def test_task__1__load_persona_data(self):
        with self.flow_connect_entities as _:
            _.task__1__load_persona_data()
            assert type(_.file__persona                      ) is My_Feeds__Personas__File
            assert type(_.file__persona_entities             ) is My_Feeds__Personas__File__Now
            assert type(_.file__persona_entities__tree_values) is My_Feeds__Personas__File__Now
            assert type(_.file__persona_connect_entities     ) is My_Feeds__Personas__File
            assert type(_.file__feed_text_entities__files    ) is Hacker_News__File
            assert type(_.persona                            ) is Schema__Persona
            assert type(_.persona_type                       ) is Schema__Persona__Types
            assert type(_.persona_entities                   ) is Schema__Persona__Text__Entities
            assert type(_.file__persona.file_id              ) is Safe_Id
            assert _.file__persona.file_id                     == FILE_ID__PERSONA

            #pprint(_.persona_entities__tree_values)

    def test_task__2__load_articles_data(self):
        with self.flow_connect_entities as _:
            _.task__1__load_persona_data()
            _.task__2__load_articles_data()

            assert type(_.feed_text_entities__files            ) is Schema__Feed__Text_Entities__Files
            assert type(_.path_now__text_entities__titles__tree) is str
            assert type(_.articles_graph_tree                  ) is str

            assert len(_.path_now__text_entities__titles__tree) > 30
            assert len(_.articles_graph_tree                  ) > 1000




    def test_task__3__create_connected_entities(self):
        with self.flow_connect_entities as _:
            _.task__1__load_persona_data               ()
            _.task__2__load_articles_data              ()
            _.task__3__create_connected_entities       ()
            _.task__5__create_output                   ()
            assert type(_.llm_connect_entities)      is Schema__Persona__LLM__Connect_Entities
            assert type(_.file_llm_connect_entities) is My_Feeds__Personas__File

            # from osbot_utils.utils.Dev import pprint
            # pprint(_.output)

    def test_task__4__collect_articles_markdown(self):
        with self.flow_connect_entities as _:
            _.task__1__load_persona_data               ()
            _.task__4__collect_articles_markdown       ()


            # from osbot_utils.utils.Dev import pprint
            # pprint(_.output)


