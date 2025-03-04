from unittest                                                                                          import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Diff__Values                                             import Schema__MGraph__Diff__Values
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types                          import Time_Chain__Day, Time_Chain__Source, Time_Chain__Hour, Time_Chain__Year, Time_Chain__Month
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                               import S3_Key__File_Extension
from myfeeds_ai.data_feeds.Data_Feeds__Shared_Constants                                                import S3_FOLDER_NAME__LATEST
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__3__Extract_New_Articles  import Flow__Hacker_News__3__Extract_New_Articles, FILE_NAME__NEW_ARTICLES
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Json                                                                            import json__equals__list_and_set
from osbot_utils.utils.Misc                                                                            import list_set
from osbot_utils.utils.Objects import type_full_name, __, base_types
from tests.integration.data_feeds__objs_for_tests                                                      import cbr_website__assert_local_stack

class test__int__Flow__Hacker_News__Extract_New_Articles(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
        cls.current_path = '2025/02/20/23'  # use these two in order to have a deterministic data set in the tests below
        cls.previous_path = '2025/02/19/22'

    def setUp(self):
        self.flow_extract_new_articles = Flow__Hacker_News__3__Extract_New_Articles()                      # new object on every test run

    # def test_process_flow(self):
    #     with self.flow_extract_new_articles as _:
    #         _.current__path = self.current_path
    #         result = self.flow_extract_new_articles.run()

    def test_task__1__resolve__previous__path(self):

        with Flow__Hacker_News__3__Extract_New_Articles() as _:                                           # Use-case 1: no paths provided
            assert _.current__path  is None
            assert _.previous__path is None
            _.task__1__resolve__previous__path()
            assert _.current__path == _.hacker_news_storage.path_to__now_utc()
            if _.current__config_new_articles:
                assert _.previous__path == _.current__config_new_articles.path__current

        with Flow__Hacker_News__3__Extract_New_Articles() as _:                                           # Use-case 1:  with current_path
            _.current__path = self.current_path
            _.task__1__resolve__previous__path()
            assert _.current__path  == self.current_path                                                # current path is unchanged
            assert _.previous__path == _.current__config_new_articles.path__current                                                # previous path should have not changed

        with self.flow_extract_new_articles as _:                                                       # Use-case 3: with no current_path
            _.previous__path = self.previous_path
            _.task__1__resolve__previous__path()
            assert _.current__path  == _.hacker_news_storage.path_to__now_utc()                         # current path should now be latest
            assert _.previous__path == self.previous_path                                               # previous path is unchanged

        with self.flow_extract_new_articles as _:                                                       # Use-case 4: with both current and previous
            _.current__path  = self.current_path
            _.previous__path = self.previous_path
            _.task__1__resolve__previous__path()
            assert _.current__path  == self.current_path                                                # current path is unchanged
            assert _.previous__path == self.previous_path                                               # previous path is unchanged

    def test_task__2__create__timeline_diff(self):
        with self.flow_extract_new_articles as _:
            _.current__path  = self.current_path                                                        # simulate the current and previous path config
            _.previous__path = self.previous_path

            _.task__2__create__timeline_diff()

            assert type(_.timeline_diff)       is Schema__MGraph__Diff__Values
            assert base_types(_.timeline_diff) == [Type_Safe, object]

            # since we are using cached data , these will always be the ame
            assert type(_.timeline_diff) is Schema__MGraph__Diff__Values        # confirm data has been loaded into a new object of type Schema__MGraph__Diff__Values
            assert sorted(_.timeline_diff.added_values  [Time_Chain__Day   ]) == ['20']
            assert sorted(_.timeline_diff.removed_values[Time_Chain__Day   ]) == ['10']
            assert sorted(_.timeline_diff.added_values  [Time_Chain__Source]) == sorted([ '272b4927', 'e5091ea4', '5d2f8952', 'ce7e697e', 'd54c06c4', '9153bba8', '55b2f8d2'])
            assert sorted(_.timeline_diff.removed_values[Time_Chain__Source]) == sorted([ '468bfcf6', 'f2082031', '08ec0110', 'ea2a87d4', '0a68e403','d0ca70d4', '5f6bf957' ])

    def test_task__3__update_current_articles(self):
        with self.flow_extract_new_articles as _:
            _.current__path  = self.current_path                                                        # simulate the current and previous path config
            _.previous__path = self.previous_path

            _.task__2__create__timeline_diff  ()
            _.task__3__update_current_articles()

            #pprint(_.current__articles.json())

    def test_task__5__create_output(self):
        with self.flow_extract_new_articles as _:
            _.current__path  = self.current_path                                                        # simulate the current and previous path config
            _.previous__path = self.previous_path

            _.task__2__create__timeline_diff  ()
            _.task__3__update_current_articles()
            _.task__5__create_output          ()
            pprint(_.output)

    # def test_update_current_articles(self):
    #     with self.flow_extract_new_articles as _:
    #         _.current__path =  self.current_path
    #         _.previous__path = self.previous_path
    #         _.task__2__create__timeline_diff()
    #        _.task__3__update_current_articles()

    # def test_load_and_diff_timeline_data___without_any_paths(self):
    #     with Flow__Hacker_News__3__Extract_New_Articles() as _:
    #         _.task__2__create__timeline_diff()
    #         assert _.timeline_diff.json()                      == {'added_values': {}, 'removed_values': {}}
    #         assert _.mgraph__timeline__current .data().stats() == {'edges_ids': 0, 'nodes_ids': 0}
    #         assert _.mgraph__timeline__previous.data().stats() == {'edges_ids': 0, 'nodes_ids': 0}
    #
    # def test_load_and_diff_timeline_data___without_previous(self):
    #     with Flow__Hacker_News__3__Extract_New_Articles() as _:
    #         _.current__path = self.current_path
    #         _.task__2__create__timeline_diff()
    #         assert _.mgraph__timeline__current .data().stats() == {'edges_ids': 97, 'nodes_ids': 98}
    #         assert _.mgraph__timeline__previous.data().stats() == {'edges_ids': 0 , 'nodes_ids': 0}
    #         timeline_diff = _.timeline_diff.obj()
    #         assert list_set(timeline_diff.added_values) == sorted([ type_full_name(Time_Chain__Year  ),
    #                                                                 type_full_name(Time_Chain__Month ),
    #                                                                 type_full_name(Time_Chain__Day   ),
    #                                                                 type_full_name(Time_Chain__Hour  ),
    #                                                                 type_full_name(Time_Chain__Source)])
    #         assert timeline_diff.removed_values         == __()
    #
    # def test_load_and_diff_timeline_data___without_current(self):
    #     with Flow__Hacker_News__3__Extract_New_Articles() as _:
    #         _.previous__path = self.previous_path
    #         _.task__2__create__timeline_diff()
    #         assert _.mgraph__timeline__current .data().stats() == {'edges_ids': 0  , 'nodes_ids': 0  }
    #         assert _.mgraph__timeline__previous.data().stats() == {'edges_ids': 100, 'nodes_ids': 101}
    #         timeline_diff = _.timeline_diff.obj()
    #         assert timeline_diff.added_values             == __()
    #         assert list_set(timeline_diff.removed_values) == sorted([ type_full_name(Time_Chain__Year  ),
    #                                                                 type_full_name(Time_Chain__Month ),
    #                                                                 type_full_name(Time_Chain__Day   ),
    #                                                                 type_full_name(Time_Chain__Hour  ),
    #                                                                 type_full_name(Time_Chain__Source)])
    #
    #         #assert _.config_new_articles.timeline_diff.json () == {'added_values': {}, 'removed_values': {}}
    #
    # def test_save__config_new_articles__current(self):
    #     with self.flow_extract_new_articles as _:
    #         _.current__path = self.current_path
    #         _.task__2__create__timeline_diff()
    #         _.save__config_new_articles__current()
    #         assert _.path__new_articles__current      == f'{_.new__config_new_articles.path__current}/{FILE_NAME__NEW_ARTICLES}.{S3_Key__File_Extension.JSON.value}'
    #         assert _.new__config_new_articles.json()  == _.hacker_news_storage.load_from__path(path=_.new__config_new_articles.path__current, file_id=FILE_NAME__NEW_ARTICLES, extension=S3_Key__File_Extension.JSON.value)
    #
    #
    # def test_save__config_new_articles__latest(self):
    #     with self.flow_extract_new_articles as _:
    #         _.current__path = self.current_path
    #         _.task__2__create__timeline_diff()
    #         _.save__config_new_articles__current()      # todo: improve logic so that we don't need to call this one before
    #         _.save__config_new_articles__latest ()
    #         assert _.path__new_articles__latest == f'{S3_FOLDER_NAME__LATEST}/{FILE_NAME__NEW_ARTICLES}.{S3_Key__File_Extension.JSON.value}'
    #         assert _.new__config_new_articles.json() == _.hacker_news_storage.load_from__latest(file_id=FILE_NAME__NEW_ARTICLES, extension=S3_Key__File_Extension.JSON.value)
    #         assert json__equals__list_and_set(_.new__config_new_articles.json(), _.hacker_news_data.new_articles().json())
    #
    # def test_create_screenshot(self):
    #     with self.flow_extract_new_articles as _:
    #         _.task__2__create__timeline_diff()
    #         _.create_screenshot()


            # load_dotenv()
            #
            # assert type(_.timeline_diff) is Schema__MGraph__Diff__Values
            # #pprint(_.timeline_diff.json())
            # self.view = MGraph__View__Diff__Values(diff=_.timeline_diff)
            #
            # self.view.create_graph()
            # screenshot_file = type(self).__name__ + '.png'
            # with self.view.create_mgraph_screenshot() as _:
            #     # with _.export().export_dot() as dot:
            #     #     dot.show_node__value__key()
            #     _.save_to(screenshot_file)
            #     _.dot()

    # def test__experiment__load_article(self):
    #     with Flow__Hacker_News__Process_New_Articles() as _:
    #         _.current__path  = '2025/02/23/16'
    #         _.previous__path = '2025/02/19/22'
    #         _.resolve__previous__path()
    #         print()
    #         print('current' , _.current__path )
    #         print('previous', _.previous__path)
    #
    #         _.load_and_diff_timeline_data()
    #         new_articles = _.timeline_diff.added_values.get(Time_Chain__Source,{})
    #         removed_values = _.timeline_diff.removed_values.get(Time_Chain__Source, {})
    #         pprint(removed_values)
    #         return
    #         source_id__value  = list(new_articles)[2]
    #         #new_article_id = '5d2f8952'
    #         #pprint(new_article_id)
    #         # pprint(_.mgraph__timeline__current.json())
    #         # return
    #         #pprint(_.mgraph__timeline__current.json())
    #
    #         with print_duration():
    #             with _.mgraph__timeline__current as mgraph:
    #                 #pprint(mgraph.values().get_by_value(str   , new_article_id))
    #                 #domain_node = mgraph.values().get_by_value(Time_Chain__Source, source_id__value)
    #                 #node_id = domain_node.node_id
    #                 #print('node_id', node_id)
    #                 #pprint(domain_node.node.json())
    #                 #pprint(domain_node.models__to_edges()[0].data.json())
    #                 with mgraph.data() as data:
    #                     with mgraph.index() as index:
    #                         node_hour_id  = list(index.get_nodes_connected_to_value(Time_Chain__Source(source_id__value)))[0]
    #                         node_hour     = data.node(node_hour_id)
    #                         pprint(node_hour.node.json())
    #                         print('node_hour', node_hour_id)
    #                         print('source_id__value', source_id__value)
    #
    #                 #pprint(mgraph.index().nodes_to_incoming_edges_by_type())
    #                 #pprint(mgraph.data().node(new_article_id))
    #                 #pprint(mgraph.data().edge(new_article_id))
    #                 #pprint(mgraph.values().mgraph_edit.index().index_data.json())
    #
    #         #pprint(_.timeline_diff.json())
    #         return
    #         # return
    #         # assert _.current__path  == '2025/02/23/22'
    #         # assert _.previous__path == '2025/02/20/16'
    #
    #         _.save__config_new_articles__current()
    #         _.save__config_new_articles__latest()
    #         pprint(_.path__new_articles__current)
    #         pprint(_.path__new_articles__latest)
    #
    #         pprint(_.hacker_news_storage.load_from__path('2025/02/23/22','new-articles','json'))
    #         #
    #         pprint(_.hacker_news_storage.load_from__latest('new-articles','json'))
