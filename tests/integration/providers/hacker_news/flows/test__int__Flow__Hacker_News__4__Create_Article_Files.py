from unittest                                                                                           import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__4__Create_Article_Files   import Flow__Hacker_News__4__Create_Article_Files
from tests.integration.data_feeds__objs_for_tests                                                       import cbr_website__assert_local_stack


class test__int__Flow__Hacker_News__4__Create_Article_Files(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()

    def setUp(self):
        self.flow_create_article_files = Flow__Hacker_News__4__Create_Article_Files()

    def test_task__1__load_articles_to_process(self):
        with self.flow_create_article_files as _:
            _.task__1__load_articles_to_process()
            assert _.articles_to_process      == _.file_current_articles.to__process()
            assert len(_.articles_to_process) >  0

    def test_task__2__create_missing_article_files(self):
        with self.flow_create_article_files as _:
            _.task__1__load_articles_to_process    ()
            _.task__2__create_missing_article_files()

