from unittest                                                                                        import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Article__Entities          import Hacker_News__Article__Entities
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Article__Text_Entities import Hacker_News__File__Article__Text_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Now                    import Hacker_News__File__Now
from osbot_utils.type_safe.Type_Safe                                                                 import Type_Safe
from osbot_utils.utils.Objects                                                                       import base_types


class test_Hacker__News__Article__Entities(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.article_id          = '9153bba8'
        cls.path__folder__data = '1955/11/12/22'
        cls.article_entities   = Hacker_News__Article__Entities(article_id=cls.article_id, path__folder__data=cls.path__folder__data)

    def test__init__(self):
        with self.article_entities as _:
            assert type(_)       is Hacker_News__Article__Entities
            assert base_types(_) == [Type_Safe, object]

    def test_file___text__entities__title(self):
        with self.article_entities.file___text__entities__title() as _:
            assert type(_) == Hacker_News__File__Article__Text_Entities
            assert base_types(_) == [Hacker_News__File__Now , Type_Safe, object]
            assert _.exists() is False
            assert _.path_now() == f'{self.path__folder__data}/articles/{self.article_id}/entities/text-entities-title.json'
            assert _.content_type == ''

    def test_file___text__entities__title__png(self):
        with self.article_entities.file___text__entities__title__png() as _:
            assert type(_) == Hacker_News__File__Article__Text_Entities
            assert base_types(_) == [Hacker_News__File__Now , Type_Safe, object]
            assert _.exists() is False
            assert _.path_now() == f'{self.path__folder__data}/articles/{self.article_id}/entities/text-entities-title.png'
            assert _.content_type == 'image/png'
