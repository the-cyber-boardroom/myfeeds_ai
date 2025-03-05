from unittest import TestCase

from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__5__Create_Article_Markdown import \
    Flow__Hacker_News__5__Create_Article_Markdown
from osbot_utils.utils.Dev import pprint
from tests.integration.data_feeds__objs_for_tests import cbr_website__assert_local_stack


class test__int__Flow__Hacker_News__5__Create_Article_Markdown(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()

    def setUp(self):
        self.flow_create_article_markdown = Flow__Hacker_News__5__Create_Article_Markdown()

    def test_task__1__load_articles_to_process(self):
        with self.flow_create_article_markdown as _:
            _.task__1__load_articles_to_process()
            assert _.articles_to_process      == _.file_articles_current.next_step__2__markdown_for_article()
            assert len(_.articles_to_process) >=  0
            pprint(_.articles_to_process)

    def test_task__2__create_article_markdown(self):
        with self.flow_create_article_markdown as _:
            _.task__1__load_articles_to_process()
            _.task__2__create_article_markdown()

            pprint(_.status_changes.json())

