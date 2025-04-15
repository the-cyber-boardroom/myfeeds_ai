import pytest
from unittest                                                               import TestCase
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                    import S3_Key__File__Extension
from myfeeds_ai.personas.actions.My_Feeds__Persona                          import My_Feeds__Persona
from myfeeds_ai.personas.config.Config__My_Feeds__Personas                  import FILE_ID__PERSONA, FILE_ID__PERSONA__ENTITIES
from myfeeds_ai.personas.files.My_Feeds__Personas__File import My_Feeds__Personas__File
from myfeeds_ai.personas.files.My_Feeds__Personas__File__Now                import My_Feeds__Personas__File__Now
from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__1__Create__Persona import Flow__My_Feeds__Personas__1__Create__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__Types                     import Schema__Persona__Types
from osbot_utils.helpers.Safe_Id                                            import Safe_Id
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI           import ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.helpers.safe_str.Safe_Str__Hash                            import safe_str_hash
from osbot_utils.utils.Env                                                  import get_env
from tests.integration.data_feeds__objs_for_tests                           import myfeeds_tests__setup_local_stack

class test_Flow__My_Feeds__Personas__1__Create__Persona(TestCase):

    @classmethod
    def setUpClass(cls):
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip('This test requires OpenAI API Key to run')
        myfeeds_tests__setup_local_stack()
        cls.persona_type        = Schema__Persona__Types.EXEC__CISO
        cls.flow_create_persona = Flow__My_Feeds__Personas__1__Create__Persona()
        cls.path__folder_now    = My_Feeds__Personas__File__Now(persona_type=cls.persona_type).hacker_news_storage.path__folder_now()

    def test_task__1__load_persona_data(self):
        with self.flow_create_persona as _:
            _.task__1__load_persona_data()

            assert type(_.persona             )  is My_Feeds__Persona
            assert type(_.persona_type        )  is Schema__Persona__Types

        with self.flow_create_persona.persona as _:
            assert _.exists() is True

        with self.flow_create_persona.persona.file__persona() as _:
            assert type(_)          is My_Feeds__Personas__File
            assert type(_.file_id)  is Safe_Id
            assert _.path_now   ()  == f'{self.path__folder_now}/{FILE_ID__PERSONA}.{S3_Key__File__Extension.JSON.value}'
            assert _.path_latest()  == f'latest/{self.persona_type.value}__{FILE_ID__PERSONA}.{S3_Key__File__Extension.JSON.value}'
            assert _.file_id        == FILE_ID__PERSONA

        with self.flow_create_persona.persona.file__persona_entities() as _:
            assert type(_) is My_Feeds__Personas__File__Now
            assert _.path_now() == f'{self.path__folder_now}/{FILE_ID__PERSONA__ENTITIES}.{S3_Key__File__Extension.JSON.value}'


    def test_task__2__set_persona_details(self):
        with self.flow_create_persona as _:
            _.task__1__load_persona_data()
            _.task__2__set_persona_details()
            with _.persona.data() as data:
                assert data.description__hash == safe_str_hash(data.description)

    def test_task__3__create_entities(self):
        with self.flow_create_persona as _:
            _.task__1__load_persona_data  ()
            _.task__3__create_entities()
            with _.persona as persona:
                assert type(persona)                             is My_Feeds__Persona
                assert persona.file__persona_entities().exists() is True
                assert persona.data().path__persona__entities    == persona.file__persona_entities().path_now()
                assert persona.persona__entities().text          == _.persona.description()


    def test_test__4__create_tree_values(self):
        with self.flow_create_persona as _:
            _.task__1__load_persona_data()
            _.task__4__create_tree_values()

            with _.persona as persona:
                assert persona.data().path__persona__entities__tree_values == persona.file__persona_entities__tree_values().path_now()

        with self.flow_create_persona.persona.file__persona_entities__tree_values() as _:
            tree_values = _.data()
            assert _.exists()            is True
            assert type(tree_values)     is bytes
            assert len (tree_values)     > 10
            assert tree_values.decode()  == self.flow_create_persona.persona.persona__entities__tree_values()


    def test_task__5__create_description_png(self):

        with self.flow_create_persona as _:
            _.task__1__load_persona_data()
            _.task__5__create_description_png()

            file__persona_entities__png = _.persona.file__persona_entities__png()

            assert file__persona_entities__png.exists()          is True
            assert _.persona.data().path__persona__entities__png == file__persona_entities__png.path_now()

    def test_task__6__save_persona(self):
        with self.flow_create_persona as _:
            _.task__1__load_persona_data     ()
            _.task__2__set_persona_details   ()
            _.task__3__create_entities       ()
            _.task__4__create_tree_values    ()
            _.task__5__create_description_png()
            _.task__6__create_output         ()

        assert self.flow_create_persona.output == { 'persona'   : _.persona.data().json() ,
                                                    'persona_id': self.persona_type       }

