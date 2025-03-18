from unittest import TestCase

from myfeeds_ai.personas.actions.My_Feeds__Personas import My_Feeds__Personas
from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage import My_Feeds__Personas__Storage
from myfeeds_ai.personas.files.My_Feeds__Personas__File import My_Feeds__Personas__File
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News import FILE_ID__PERSONA__CISO
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File import Hacker_News__File
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Now import Hacker_News__File__Now
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import base_types
from tests.integration.data_feeds__objs_for_tests import myfeeds_tests__setup_local_stack


class test_My_Feeds__Personas(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.personas = My_Feeds__Personas()

    def test__init__(self):
        with self.personas as _:
            assert type(_)         is My_Feeds__Personas
            assert type(_.storage) is My_Feeds__Personas__Storage

    def test_file__persona__ciso(self):
        with self.personas.file__persona__ciso() as _:
            assert type(_) is My_Feeds__Personas__File
            assert _.path_now() == f'{_.folder__path_now()}/{FILE_ID__PERSONA__CISO}.json'

    def test_files_in__latest(self):
        with self.personas as _:
            pprint(_.files_in__latest())

    def test_files_in__now(self):
        with self.personas as _:
            pprint(_.files_in__now())
            


