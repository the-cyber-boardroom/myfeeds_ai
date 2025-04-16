import pytest
from unittest                                                                                   import TestCase
from myfeeds_ai.personas.actions.My_Feeds__Persona                                              import My_Feeds__Persona
from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__2__LLM__Connected_Entities             import Flow__My_Feeds__Personas__2__LLM__Connected_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Articles__Connected_Entities                  import Schema__Persona__Articles__Connected_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                                         import Schema__Persona__Types
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Feed__Text_Entities   import Hacker_News__Feed__Text_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Text_Entities__Files import Schema__Feed__Text_Entities__Files
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI                               import ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.type_safe.Type_Safe__List                                                      import Type_Safe__List
from osbot_utils.utils.Env                                                                      import get_env
from tests.integration.data_feeds__objs_for_tests                                               import myfeeds_tests__setup_local_stack

class test_Flow__My_Feeds__Personas__2__LLM__Connected_Entities(TestCase):

    @classmethod
    def setUpClass(cls):
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip('This test requires OpenAI API Key to run')
        myfeeds_tests__setup_local_stack()
        cls.persona_type          = Schema__Persona__Types.EXEC__CISO
        cls.flow_connect_entities = Flow__My_Feeds__Personas__2__LLM__Connected_Entities(persona_type=cls.persona_type)

    def test_task__1__load_persona_data(self):
        with self.flow_connect_entities as _:
            _.task__1__load_persona_data()

            assert type(_.persona)             is My_Feeds__Persona
            assert _.persona.persona_type      == Schema__Persona__Types.EXEC__CISO
            assert type(_.persona_graph_tree)  is str                             # data should be bytes
            assert len(_.persona_graph_tree )  > 100                                 # and have some values


    def test_task__2__load_articles_data(self):

        with self.flow_connect_entities.feed_text_entities as _:
            assert type(_                       ) is Hacker_News__Feed__Text_Entities
            assert type(_.text_entities__files()) is Schema__Feed__Text_Entities__Files

        with self.flow_connect_entities as _:
            _.task__1__load_persona_data()
            _.task__2__load_articles_data()

            if _.text_entities_changed:
                assert 'article_entity' in _.articles_graph_tree
                if _.persona__articles__connected_entities.paths__feed__text_entities:
                    assert _.paths__feed__text_entities.json() == _.persona__articles__connected_entities.paths__feed__text_entities.json()


    def test_task__3__create_connected_entities(self):
        with self.flow_connect_entities as _:
            _.task__1__load_persona_data               ()
            _.task__2__load_articles_data              ()
            _.task__3__create_connected_entities       ()

        with _.persona.file__persona_articles__connected_entities().data() as data:
            #assert _.persona.data().path__persona__articles__connected_entities == data.path__now           # todo: review the save workflow since there is a small race condition here caused by the use of @cache_on_self on the My_Feeds__Persona.data()
            assert type(data)                                                   is Schema__Persona__Articles__Connected_Entities
            assert type(data.connected_entities)                                is Type_Safe__List

            assert data.paths__feed__text_entities.json() == self.flow_connect_entities.paths__feed__text_entities.json()


    def test_task__4__collect_articles_markdown(self):
        with self.flow_connect_entities as _:
            _.task__1__load_persona_data               ()
            _.task__4__collect_articles_markdown       ()

            with _.persona.file__persona_articles__connected_entities().data() as data:
                assert len(data.articles_markdown) > 0
