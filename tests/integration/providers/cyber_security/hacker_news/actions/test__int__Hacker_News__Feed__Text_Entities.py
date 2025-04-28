import pytest
from unittest                                                                                       import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Feed__Text_Entities       import Hacker_News__Feed__Text_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Text_Entities__Files     import Schema__Feed__Text_Entities__Files
from tests.integration.data_feeds__objs_for_tests                                                   import myfeeds_tests__setup_local_stack

class test_Hacker_News__Feed__Text_Entities(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.feed_text_entities        = Hacker_News__Feed__Text_Entities()
        cls.file__text_entities__file = cls.feed_text_entities.file__feed_text_entities__files()
        if cls.file__text_entities__file.not_exists():
            pytest.skip("This test needs a valid file__text_entities__file")

    def test_setup(self):
        with self.file__text_entities__file as _:
            assert _.exists()
            assert _.data().path_latest__text_entities__titles == 'latest/feed-text-entities-titles.mgraph.json'

    def test_text_entities__files(self):
        with self.feed_text_entities.text_entities__files() as _:
            assert type(_) is Schema__Feed__Text_Entities__Files

    def test__mgraph__entities__titles(self):
        entities__titles = self.feed_text_entities.mgraph__entities__titles()
        assert entities__titles.get('edit_class') == 'mgraph_db.mgraph.actions.MGraph__Edit.MGraph__Edit' # easy way to confirm it is a graph

    def test_tree_view__entities__titles(self):
        tree_view__entities__titles = self.feed_text_entities.tree_view__entities__titles()
        assert type(tree_view__entities__titles) is str
        assert 'article_entity' in tree_view__entities__titles