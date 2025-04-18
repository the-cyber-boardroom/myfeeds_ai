from unittest                                                           import TestCase
from myfeeds_ai.personas.actions.My_Feeds__Personas                     import My_Feeds__Personas
from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage            import My_Feeds__Personas__Storage
from tests.integration.data_feeds__objs_for_tests                       import myfeeds_tests__setup_local_stack


class test_My_Feeds__Personas(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.personas = My_Feeds__Personas()

    def test__init__(self):
        with self.personas as _:
            assert type(_)         is My_Feeds__Personas
            assert type(_.storage) is My_Feeds__Personas__Storage

    def test_files_in__latest(self):
        with self.personas as _:
            _.files_in__latest()

    def test_files_in__now(self):
        with self.personas as _:
            _.files_in__now()


            


