import pytest
from unittest                                                           import TestCase
from myfeeds_ai.personas.actions.My_Feeds__Persona                      import My_Feeds__Persona
from myfeeds_ai.personas.actions.My_Feeds__Persona__Files               import My_Feeds__Persona__Files
from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage__Persona   import My_Feeds__Personas__Storage__Persona
from myfeeds_ai.personas.files.My_Feeds__Personas__File                 import My_Feeds__Personas__File
from myfeeds_ai.personas.schemas.Default_Data__My_Feeds__Personas       import Default_Data__My_Feeds__Personas
from myfeeds_ai.personas.schemas.Schema__Persona                        import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__Entities              import Schema__Persona__Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Text__Entities        import Schema__Persona__Text__Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                 import Schema__Persona__Types
from myfeeds_ai.utils.shared_schemas.Str__Description                   import Str__Description
from osbot_utils.helpers.safe_str.Safe_Str__Hash                        import safe_str_hash
from osbot_utils.utils.Misc                                             import random_text
from osbot_utils.utils.Objects                                          import __
from tests.integration.data_feeds__objs_for_tests                       import myfeeds_tests__setup_local_stack

class test__int__My_Feeds__Persona(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.persona_type = Schema__Persona__Types.EXEC__CISO
        cls.persona      = My_Feeds__Persona(persona_type=cls.persona_type)
        if cls.persona.exists() is False:
            pytest.skip(f"test needs data to exist for persona: {cls.persona_type} ")

    def test__init__(self):
        with self.persona as _:
            assert type(_              ) is My_Feeds__Persona
            assert type(_.persona_files) is My_Feeds__Persona__Files
            assert type(_.persona_type ) is Schema__Persona__Types
            assert _.persona_type        is Schema__Persona__Types.EXEC__CISO

    def test_data(self):
        assert type(self.persona.data()) is Schema__Persona

    def test_delete(self):
        test_persona  = Schema__Persona__Types.TEST__PERSONA
        with My_Feeds__Persona(persona_type=test_persona).create() as _:
            assert _.exists() is True
            assert _.delete() is True
            assert _.exists() is False


    def test_persona(self):
        with self.persona as _:
            data_persona = _.persona()
            assert type(data_persona) is Schema__Persona
            assert data_persona.json() == _.data().json()

    def test_persona__entities(self):
        with self.persona as _:
            if _.file__persona_entities().exists():
                persona_entities = _.persona__entities()
                assert type(persona_entities              ) is Schema__Persona__Text__Entities
                assert type(persona_entities.text_entities) is Schema__Persona__Entities

    def test_persona__entities__png(self):
        with self.persona as _:
            if _.file__persona_entities__png().exists():
                png_bytes = _.persona__entities__png()
                assert type(png_bytes ) is bytes
                assert png_bytes.startswith(b'\x89PNG\r\n')

    def test_persona__entities__tree_values(self):
        with self.persona as _:
            if _.file__persona_entities__tree_values().exists():
                tree_values = _.persona__entities__tree_values()
                assert type(tree_values ) is str
                assert 'entity:' in tree_values


    def test_description(self):
        with self.persona as _:
            description = _.description()
            assert type(description)         is Str__Description
            assert len(description)          > 0
            assert description               == _.data().description
            assert safe_str_hash(description) == _.data().description__hash

    def test_description__change_value_and_reset_paths(self):
        test_persona        = Schema__Persona__Types.TEST__PERSONA                  # use the test account here so that we don't impact the current persona
        with My_Feeds__Persona(persona_type=test_persona).create() as _:
            new_description      = random_text('This is a new description')
            new_description_hash = safe_str_hash(new_description)
            assert _.description__change_value_and_reset_paths(new_description=new_description) is True

            assert _.data().obj() == __(description                                 = new_description             ,
                                        description__hash                           = new_description_hash        ,
                                        path__now                                   = _.file__persona().path_now(),
                                        path__persona__articles__connected_entities = None  ,
                                        path__persona__digest                       = None  ,
                                        path__persona__digest__html                 = None  ,
                                        path__persona__entities                     = ''    ,
                                        path__persona__entities__png                = ''    ,
                                        path__persona__entities__tree_values        = ''    ,
                                        path__persona__latest                       = 'latest/test-persona__persona.json',
                                        persona_type                                = 'TEST__PERSONA')

            assert _.file__persona().load() == _.data().json()

    def test_description__reset_to_default_value(self):
        test_persona        = Schema__Persona__Types.TEST__PERSONA
        description__random = random_text('This is a new description')
        description_test_persona = Default_Data__My_Feeds__Personas.get(test_persona).get('description')
        with My_Feeds__Persona(persona_type=test_persona).create() as _:
            assert _.data().description                                             == description_test_persona     # creates sets the description value to the default
            assert _.description__change_value_and_reset_paths(description__random) is True                         # changing should work
            assert _.data().description                                             != description_test_persona     # now values should not match
            assert _.description__reset_to_default_value      ()                    is True                         # reset to default value should work
            assert _.data().description                                             == description_test_persona     # values should be equal again

    def test_exists(self):
        with self.persona as _:
            assert _.exists() is True

    def test_file__persona(self):
        with self.persona.file__persona() as _:
            assert type(_)                            is My_Feeds__Personas__File
            assert _.data_type                        is Schema__Persona
            assert str(_.extension)                   == 'json'
            assert _.file_id                          == 'persona'
            assert _.latest_prefix                    == 'exec-ciso'
            assert _.now                              is None
            assert _.hacker_news_storage.persona_type == self.persona_type

    def test_file_contents(self):
        with self.persona as _:
            data      = _.data()
            path__now = data.path__now
            assert _.file_contents(path__now) == data.json()

    def test_storage(self):
        with self.persona as _:
            storage = _.storage()
            assert type(storage) is My_Feeds__Personas__Storage__Persona
            assert storage.json() == _.file__persona().hacker_news_storage.json()
            assert storage.persona_type == self.persona_type
