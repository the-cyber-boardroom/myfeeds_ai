from unittest                                                                                                           import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__4__Article__Step_1__Create_Article_Files  import Flow__Hacker_News__4__Article__Step_1__Create_Article_Files, FLOW__HACKER_NEWS__4__MAX__ARTICLES_TO_SAVE
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Status                              import Schema__Feed__Article__Status
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step                                import Schema__Feed__Article__Step
from osbot_utils.helpers.flows.Flow import Flow
from osbot_utils.utils.Threads import invoke_async
from tests.integration.data_feeds__objs_for_tests                                                                       import myfeeds_tests__setup_local_stack

class test__int__Flow__Hacker_News__4__Article__Step_1__Create_Article_Files(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()

    def setUp(self):
        self.flow_create_article_files = Flow__Hacker_News__4__Article__Step_1__Create_Article_Files()

    def test_task__1__load_articles_to_process(self):
        with self.flow_create_article_files as _:
            _.task__1__load_articles_to_process()
            assert _.articles_to_process      == _.file_articles_current.next_step__1__save_article()
            assert len(_.articles_to_process) >=  0

    def test_task__3__create_missing_article_files(self):
        from_status = Schema__Feed__Article__Status.TO_PROCESS
        to_status   = Schema__Feed__Article__Status.PROCESSING
        from_step   = Schema__Feed__Article__Step.STEP__1__SAVE__ARTICLE
        to_step     = Schema__Feed__Article__Step.STEP__2__MARKDOWN__FOR_ARTICLE

        with self.flow_create_article_files as _:
            #_.max_articles_to_save = 2

            _.task__1__load_articles_to_process    ()
            _.task__2__find_articles_to_safe       ()
            _.task__3__create_missing_article_files()

            if len(_.status_changes) > 0:
                assert len(_.status_changes) <= FLOW__HACKER_NEWS__4__MAX__ARTICLES_TO_SAVE
                status_change = _.status_changes[0]
                assert status_change.from_status       == from_status
                assert status_change.article.status    == to_status
                assert status_change.from_step         == from_step
                assert status_change.article.next_step == to_step

                assert len(_.file_articles_all.articles.articles) > 0

                # from osbot_utils.utils.Dev import pprint
                # pprint(status_change.json())
                # article_id = status_change.article.article_id
                # #pprint(_.file_articles_all.articles.json())

    def test_run(self):
        with self.flow_create_article_files as _:
            _.max_articles_to_save = 1
            flow = _.run()
            assert type(_)    is Flow__Hacker_News__4__Article__Step_1__Create_Article_Files
            assert type(flow) is Flow

            # from osbot_utils.utils.Dev import pprint
            # pprint(flow.flow_return_value)
            # pprint(flow.durations())

