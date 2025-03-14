from unittest                                                                                      import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage__Article__Entity import Hacker_News__Storage__Article__Entity


class test_Hacker_News__Storage__Article__Entity(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.storage_article_entity = Hacker_News__Storage__Article__Entity()

    def test__init__(self):
        with self.storage_article_entity as _:
            path_now = _.s3_db.s3_path__now()
            assert _.areas() == ['articles', _.article_id, 'entities']
            assert _.path__folder_now() == f'{path_now}/articles/{_.article_id}/entities'
