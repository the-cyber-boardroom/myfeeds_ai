from unittest import TestCase

from myfeeds_ai.personas.actions.My_Feeds__Persona__Digest import My_Feeds__Persona__Digest
from tests.integration.data_feeds__objs_for_tests import myfeeds_tests__setup_local_stack


class test__int__My_Feeds__Persona__Digest(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.persona_digest = My_Feeds__Persona__Digest()

