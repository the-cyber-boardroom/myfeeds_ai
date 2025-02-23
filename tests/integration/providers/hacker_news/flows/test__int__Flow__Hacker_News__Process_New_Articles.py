from unittest                                                                                       import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Diff__Values                                          import Schema__MGraph__Diff__Values
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types                       import Time_Chain__Day, Time_Chain__Source, Time_Chain__Hour, Time_Chain__Year, Time_Chain__Month
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                            import S3_Key__File_Extension
from myfeeds_ai.data_feeds.Data_Feeds__Shared_Constants                                             import S3_FOLDER_NAME__LATEST
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__Process_New_Articles  import Flow__Hacker_News__Process_New_Articles, FILE_NAME__NEW_ARTICLES
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Json                                                                         import json__equals__list_and_set
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Objects import type_full_name, __
from tests.integration.data_feeds__objs_for_tests                                                   import cbr_website__assert_local_stack

class test_Flow__Hacker_News__Process_New_Articles(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
        cls.current_path = '2025/02/20/23'  # use these two in order to have a deterministic data set in the tests below
        cls.previous_path = '2025/02/19/22'

    def setUp(self):
        self.flow_process_new_articles = Flow__Hacker_News__Process_New_Articles()                      # new object on every test run
        # with self.flow_process_new_articles as _:
        #     _.config_new_articles.path__current            = self.path__current
        #     _.config_new_articles.path__previous           = self.path__previous

    def test_process_flow(self):
        with self.flow_process_new_articles as _:
            _.current__path = self.current_path
            result = self.flow_process_new_articles.run()
            #pprint(result)
            #pprint(_.timeline_diff.json())

    def test_resolve__previous__path(self):
        with Flow__Hacker_News__Process_New_Articles() as _:                                           # Use-case 1: no paths provided
            assert _.current__path  is None
            assert _.previous__path is None
            _.resolve__previous__path()
            assert _.current__path == _.hacker_news_storage.path_to__now_utc()
            if _.current__config_new_articles:
                assert _.previous__path == _.current__config_new_articles.path__current

        with Flow__Hacker_News__Process_New_Articles() as _:                                           # Use-case 1:  with current_path
            _.current__path = self.current_path
            _.resolve__previous__path()
            assert _.current__path  == self.current_path                                                # current path is unchanged
            assert _.previous__path == self.current_path                                                # previous path should have not changed

        with self.flow_process_new_articles as _:                                                       # Use-case 3: with no current_path
            _.previous__path = self.previous_path
            _.resolve__previous__path()
            assert _.current__path  == _.hacker_news_storage.path_to__now_utc()                         # current path should now be latest
            assert _.previous__path == self.previous_path                                               # previous path is unchanged

        with self.flow_process_new_articles as _:                                                       # Use-case 4: with both current and previous
            _.current__path  = self.current_path
            _.previous__path = self.previous_path
            _.resolve__previous__path()
            assert _.current__path  == self.current_path                                                # current path is unchanged
            assert _.previous__path == self.previous_path                                               # previous path is unchanged

    def test_load_and_diff_timeline_data(self):
        with self.flow_process_new_articles as _:
            _.current__path  = self.current_path                                                        # simulate the current and previous path config
            _.previous__path = self.previous_path
            _.load_and_diff_timeline_data()                                     # since we are using cached data , these will always be the ame
            assert type(_.timeline_diff) is Schema__MGraph__Diff__Values        # confirm data has been loaded into a new object of type Schema__MGraph__Diff__Values
            assert json__equals__list_and_set(_.timeline_diff.json(), { 'added_values'  : {  type_full_name(Time_Chain__Day)   : [ '20'],
                                                                                            type_full_name(Time_Chain__Source): [ '272b4927', 'e5091ea4', '5d2f8952', 'ce7e697e',
                                                                                                                                  'd54c06c4', '9153bba8', '55b2f8d2'            ]},
                                                                       'removed_values': { type_full_name(Time_Chain__Day)    : [ '10'],
                                                                                           type_full_name(Time_Chain__Source) : [ '468bfcf6', 'f2082031', '08ec0110', 'ea2a87d4',
                                                                                                                                 '0a68e403','d0ca70d4', '5f6bf957'             ]}})

    def test_load_and_diff_timeline_data___without_any_paths(self):
        with Flow__Hacker_News__Process_New_Articles() as _:
            _.load_and_diff_timeline_data()
            assert _.timeline_diff.json()                      == {'added_values': {}, 'removed_values': {}}
            assert _.mgraph__timeline__current .data().stats() == {'edges_ids': 0, 'nodes_ids': 0}
            assert _.mgraph__timeline__previous.data().stats() == {'edges_ids': 0, 'nodes_ids': 0}

    def test_load_and_diff_timeline_data___without_previous(self):
        with Flow__Hacker_News__Process_New_Articles() as _:
            _.current__path = self.current_path
            _.load_and_diff_timeline_data()
            assert _.mgraph__timeline__current .data().stats() == {'edges_ids': 97, 'nodes_ids': 98}
            assert _.mgraph__timeline__previous.data().stats() == {'edges_ids': 0 , 'nodes_ids': 0}
            timeline_diff = _.timeline_diff.obj()
            assert list_set(timeline_diff.added_values) == sorted([ type_full_name(Time_Chain__Year  ),
                                                                    type_full_name(Time_Chain__Month ),
                                                                    type_full_name(Time_Chain__Day   ),
                                                                    type_full_name(Time_Chain__Hour  ),
                                                                    type_full_name(Time_Chain__Source)])
            assert timeline_diff.removed_values         == __()

    def test_load_and_diff_timeline_data___without_current(self):
        with Flow__Hacker_News__Process_New_Articles() as _:
            _.previous__path = self.previous_path
            _.load_and_diff_timeline_data()
            assert _.mgraph__timeline__current .data().stats() == {'edges_ids': 0  , 'nodes_ids': 0  }
            assert _.mgraph__timeline__previous.data().stats() == {'edges_ids': 100, 'nodes_ids': 101}
            timeline_diff = _.timeline_diff.obj()
            assert timeline_diff.added_values             == __()
            assert list_set(timeline_diff.removed_values) == sorted([ type_full_name(Time_Chain__Year  ),
                                                                    type_full_name(Time_Chain__Month ),
                                                                    type_full_name(Time_Chain__Day   ),
                                                                    type_full_name(Time_Chain__Hour  ),
                                                                    type_full_name(Time_Chain__Source)])

            #assert _.config_new_articles.timeline_diff.json () == {'added_values': {}, 'removed_values': {}}

    def test_save__config_new_articles__current(self):
        with self.flow_process_new_articles as _:
            _.current__path = self.current_path
            _.load_and_diff_timeline_data()
            _.save__config_new_articles__current()
            assert _.path__new_articles__current      == f'{_.new__config_new_articles.path__current}/{FILE_NAME__NEW_ARTICLES}.{S3_Key__File_Extension.JSON.value}'
            assert _.new__config_new_articles.json()  == _.hacker_news_storage.load_from__path(path=_.new__config_new_articles.path__current, file_id=FILE_NAME__NEW_ARTICLES, extension=S3_Key__File_Extension.JSON.value)


    def test_save__config_new_articles__latest(self):
        with self.flow_process_new_articles as _:
            _.current__path = self.current_path
            _.load_and_diff_timeline_data()
            _.save__config_new_articles__current()      # todo: improve logic so that we don't need to call this one before
            _.save__config_new_articles__latest ()
            assert _.path__new_articles__latest == f'{S3_FOLDER_NAME__LATEST}/{FILE_NAME__NEW_ARTICLES}.{S3_Key__File_Extension.JSON.value}'
            assert _.new__config_new_articles.json() == _.hacker_news_storage.load_from__latest(file_id=FILE_NAME__NEW_ARTICLES, extension=S3_Key__File_Extension.JSON.value)
            assert json__equals__list_and_set(_.new__config_new_articles.json(), _.hacker_news_data.new_articles().json())

    def test_create_screenshot(self):
        with self.flow_process_new_articles as _:
            _.load_and_diff_timeline_data()
            _.create_screenshot()
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

