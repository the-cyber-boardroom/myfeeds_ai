import pytest
from unittest                                                                                                   import TestCase
from mgraph_db.mgraph.actions.MGraph__Screenshot                                                                import ENV_NAME__URL__MGRAPH_DB_SERVERLESS
from mgraph_db.providers.time_chain.MGraph__Time_Chain                                                          import MGraph__Time_Chain
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files                                         import Hacker_News__Files
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File                                    import Hacker_News__File
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Now                               import Hacker_News__File__Now
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Timeline__Dot_Code                import CONTENT_TYPE__MGRAPH__DOT
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__2__Create_Articles_Timeline       import Flow__Hacker_News__2__Create_Articles_Timeline, FILE_NAME__MGRAPH__TIMELINE
from myfeeds_ai.providers.cyber_security.hacker_news.mgraphs.Hacker_News__MGraph                                import Hacker_News__MGraph
from myfeeds_ai.providers.cyber_security.hacker_news.mgraphs.Hacker_News__MGraph__Timeline                      import Hacker_News__MGraph__Timeline, FILE_ID__TIMELINE__MGRAPH
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Data__Feed                      import Model__Hacker_News__Data__Feed
from osbot_utils.context_managers.disable_root_loggers                                                          import disable_root_loggers
from osbot_utils.helpers.flows.Flow                                                                             import Flow
from osbot_utils.helpers.flows.decorators.flow                                                                  import flow
from osbot_utils.type_safe.Type_Safe                                                                            import Type_Safe
from osbot_utils.utils.Env                                                                                      import get_env
from osbot_utils.utils.Misc                                                                                     import list_set
from osbot_utils.utils.Objects                                                                                  import base_types, obj, __
from tests.integration.data_feeds__objs_for_tests                                                               import myfeeds_tests__setup_local_stack


class test__int__Flow__Hacker_News__2__Create_Articles_Timeline(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        myfeeds_tests__setup_local_stack()
        cls.files                   = Hacker_News__Files()
        cls.data_feed               = cls.files.feed_data__current()
        cls.flow__articles_timeline = Flow__Hacker_News__2__Create_Articles_Timeline()
        cls.hacker_news_timeline    = cls.flow__articles_timeline.hacker_news_timeline
        cls.path_now                = cls.flow__articles_timeline.hacker_news_storage.path__folder_now()
        if len(cls.data_feed.feed_data.articles) != 50:                                     # if the feed_data__current was not created from live data, reload it
            cls.data_feed = cls.files.feed_data__current(True)
        cls.disable_root_loggers = disable_root_loggers().__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.disable_root_loggers.__exit__(None, None, None)

    def test_setUpClass(self):
        with self.flow__articles_timeline as flow_2:
            assert type(flow_2) is Flow__Hacker_News__2__Create_Articles_Timeline
            with flow_2.hacker_news_timeline as _:
                assert type      (_)   is Hacker_News__MGraph__Timeline
                assert base_types(_)   == [Hacker_News__MGraph, Hacker_News__File, Hacker_News__File__Now, Type_Safe, object]
                assert type(_.mgraph)  is MGraph__Time_Chain
                assert _.file_id == FILE_ID__TIMELINE__MGRAPH
                assert _.file_name  () == f'{FILE_ID__TIMELINE__MGRAPH}.mgraph.json'
                assert _.path_now   () == f'{self.path_now}/{_.file_name()}'
                assert _.path_latest() == f'latest/{_.file_name()}'


    def test_task__1__load_articles(self):
        with self.flow__articles_timeline as _:
            assert _.data_feed is None
            _.task__1__load_articles()
            assert type(_.data_feed) is Model__Hacker_News__Data__Feed
            assert _.data_feed.feed_data.language         == 'en-us'
            assert _.data_feed.feed_data.link             == 'https://thehackernews.com'
            assert _.data_feed.feed_data.title            == 'The Hacker News'
            assert _.data_feed.feed_data.update_frequency ==  1
            assert _.data_feed.feed_data.update_period    == 'hourly'

    def test_task__2__create_mgraph(self):
        with self.flow__articles_timeline as _:
            _.task__1__load_articles()
            assert _.hacker_news_timeline.mgraph.data().stats() == {'edges_ids': 0, 'nodes_ids': 0}
            _.task__2__create_mgraph()
            with _.hacker_news_timeline.mgraph as mgraph:
                assert mgraph.data().stats().get('edges_ids') > 70
                assert list_set(mgraph.index().index_data.edges_by_type) == [ 'Schema__MGraph__Time_Chain__Edge__Day'   ,
                                                                              'Schema__MGraph__Time_Chain__Edge__Hour'  ,
                                                                              'Schema__MGraph__Time_Chain__Edge__Month' ,
                                                                              'Schema__MGraph__Time_Chain__Edge__Source']

    def test_task__3__save_mgraph(self):
        @flow()
        def an_flow() -> Flow:
            with self.flow__articles_timeline as _:
                _.task__1__load_articles()
                _.task__2__create_mgraph()
                _.task__3__save_mgraph  ()
                return 'done'

        flow_obj = an_flow().execute_flow()

        assert type(flow_obj)             is Flow
        assert flow_obj.flow_return_value == 'done'
        with self.hacker_news_timeline as _:
            assert _.exists__now   () is True
            assert _.exists__latest() is True
            assert _.exists        () is True

    def test_task__4__create_dot_code(self):
        with self.flow__articles_timeline as _:
            _.task__2__create_mgraph()
            assert _.hacker_news_timeline.mgraph.data().stats().get('edges_ids') > 70
            _.task__4__create_dot_code()
            assert 'digraph {\n'                                      in _.dot_code
            assert 'graph [rankdir="TB", ranksep=0.2, nodesep=0.1]\n' in _.dot_code

        with self.flow__articles_timeline.hacker_news_timeline_dot_code as _:
            assert _.file_name  () == 'feed-timeline.mgraph.dot'
            assert _.path_latest() == f'latest/{_.file_name()}'
            assert _.exists     () is True
            assert _.file_name  () in _.hacker_news_storage.files_in__latest()

            assert obj(_.file_info__latest()).ContentType == CONTENT_TYPE__MGRAPH__DOT

    def test_task__5__create_png(self):
        if get_env(ENV_NAME__URL__MGRAPH_DB_SERVERLESS):
            with self.flow__articles_timeline as _:
                _.task__2__create_mgraph()
                _.task__4__create_dot_code()
                _.task__5__create_png   ()

            #if not_in_github_action():          # todo: figure out why this doesn't work in GH Actions
            with self.flow__articles_timeline.hacker_news_timeline_png as _:
                assert _.file_name() == 'feed-timeline.mgraph.png'
                assert _.file_name() in _.hacker_news_storage.files_in__latest()           # this is failing in GitHub action
                assert _.exists   () is True

                assert _.content_type                         == 'image/png'
                assert obj(_.file_info__latest()).ContentType == _.content_type
                assert obj(_.file_info__now   ()).ContentType == _.content_type

    # this is tests
    # def test_task__6__create_output(self):
    #     with self.flow__articles_timeline as _:
    #         _.task__1__load_articles  ()
    #         _.task__2__create_mgraph  ()
    #         _.task__3__save_mgraph    ()
    #         _.task__4__create_dot_code()
    #         _.task__5__create_png     ()
    #         _.task__6__create_output  ()




    def test_task__6__create_output(self):  # to test this method we can run the full flow
        with self.flow__articles_timeline as _:
            an_flow = _.run()
            assert type(an_flow)             == Flow
            assert an_flow.flow_return_value == _.output
            path_now = _.hacker_news_timeline.hacker_news_storage.path__folder_now()

            png_exists = get_env(ENV_NAME__URL__MGRAPH_DB_SERVERLESS) is not None
            assert obj(_.output) == __(articles_processed=50,
                                       hacker_news_timeline=__(exists      = True,
                                                               path_latest = 'latest/feed-timeline.mgraph.json',
                                                               path_now    = f'{path_now}/feed-timeline.mgraph.json'),
                                       hacker_news_timeline_dot_code=__(exists      = True,
                                                                        path_latest = 'latest/feed-timeline.mgraph.dot',
                                                                        path_now    = f'{path_now}/feed-timeline.mgraph.dot'),
                                       hacker_news_timeline_png=__(exists     =  png_exists,
                                                                   path_latest = 'latest/feed-timeline.mgraph.png',
                                                                   path_now    = f'{path_now}/feed-timeline.mgraph.png'))


