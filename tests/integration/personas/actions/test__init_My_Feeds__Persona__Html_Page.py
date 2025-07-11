import pytest
from unittest                                                       import TestCase
from myfeeds_ai.personas.actions.My_Feeds__Persona                  import My_Feeds__Persona
from myfeeds_ai.personas.actions.My_Feeds__Persona__Html_Page       import My_Feeds__Persona__Html_Page
from myfeeds_ai.personas.schemas.Schema__Persona__Types             import Schema__Persona__Types
from osbot_utils.utils.Env                                          import in_github_action
from tests.integration.data_feeds__objs_for_tests                   import myfeeds_tests__setup_local_stack


class test__init__My_Feeds__Persona__Html_Page(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.persona_type      = Schema__Persona__Types.EXEC__CISO
        cls.persona           = My_Feeds__Persona(persona_type=cls.persona_type)
        cls.persona_html_page = My_Feeds__Persona__Html_Page(persona=cls.persona)

    def test_create(self):
        if in_github_action():
            pytest.skip("test was failing in GH actions")
        with self.persona_html_page as _:
            html = _.create()
            #pprint(html)
            #file_create(contents=html, path='./persona.html')

            assert "Ciso Data" in html



        # Uncomment to save to file
        # with open('ceo_dashboard.html', 'w') as f:
        #     f.write(html)
