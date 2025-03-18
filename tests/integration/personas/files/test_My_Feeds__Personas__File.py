from unittest                                                                       import TestCase
from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage                        import My_Feeds__Personas__Storage
from myfeeds_ai.personas.files.My_Feeds__Personas__File                             import My_Feeds__Personas__File
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage   import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File        import Hacker_News__File
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Now   import Hacker_News__File__Now
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.utils.Objects                                                      import base_types


class test_My_Feeds__Personas__File(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.personas_file = My_Feeds__Personas__File()

    def test__init__(self):
        with self.personas_file as _:
            assert type(_)                           is My_Feeds__Personas__File
            assert type(_.hacker_news_storage)       is My_Feeds__Personas__Storage
            assert base_types(_)                     == [Hacker_News__File     , Hacker_News__File__Now, Type_Safe, object]
            assert base_types(_.hacker_news_storage) == [Hacker_News__Storage  , Type_Safe, object]

            assert _.exists() is False



