from unittest                                                                                           import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Diff__Values                                              import Schema__MGraph__Diff__Values
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types                           import Time_Chain__Day, Time_Chain__Source
from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__3__Extract_New_Articles   import Flow__Hacker_News__3__Extract_New_Articles
from osbot_utils.context_managers.disable_root_loggers                                                  import disable_root_loggers
from osbot_utils.helpers.Obj_Id                                                                         import is_obj_id
from osbot_utils.helpers.flows.Flow                                                                     import Flow
from osbot_utils.type_safe.Type_Safe                                                                    import Type_Safe
from osbot_utils.utils.Misc                                                                             import list_set
from osbot_utils.utils.Objects                                                                          import  __, base_types
from tests.integration.data_feeds__objs_for_tests                                                       import myfeeds_tests__setup_local_stack

class test__int__Flow__Hacker_News__3__Extract_New_Articles(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.current_path = '2025/02/20/23'  # use these two in order to have a deterministic data set in the tests below
        cls.previous_path = '2025/02/19/22'
        cls.disable_root_loggers = disable_root_loggers().__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.disable_root_loggers.__exit__(None, None, None)

    def setUp(self):
        kwargs = dict(current__path  = self.current_path ,                                                                  # simulate the current and previous path config
                      previous__path = self.previous_path)
        self.flow_extract_new_articles = Flow__Hacker_News__3__Extract_New_Articles(**kwargs)                               # new object on every test run
        self.path_now                  = self.flow_extract_new_articles.file_current_articles.hacker_news_storage.path__folder_now()

    def test_task__1__resolve__previous__path(self):

        with Flow__Hacker_News__3__Extract_New_Articles() as _:                                           # Use-case 1: no paths provided
            assert _.current__path  is None
            assert _.previous__path is None
            _.task__1__resolve__previous__path()
            assert _.current__path == _.file_new_articles.hacker_news_storage.path__folder_now()
            if _.file_new_articles.new_articles:
                assert _.previous__path == _.file_new_articles.new_articles.path__current

        with Flow__Hacker_News__3__Extract_New_Articles() as _:                                           # Use-case 1:  with current_path
            _.current__path = self.current_path
            _.task__1__resolve__previous__path()
            assert _.current__path  == self.current_path                                                # current path is unchanged
            assert _.previous__path == _.file_new_articles.new_articles.path__current                                                # previous path should have not changed

        with self.flow_extract_new_articles as _:                                                       # Use-case 3: with no current_path
            _.current__path  = ''
            _.previous__path = self.previous_path
            _.task__1__resolve__previous__path()
            assert _.current__path  == _.file_new_articles.hacker_news_storage.path__folder_now()                         # current path should now be latest
            assert _.previous__path == self.previous_path                                               # previous path is unchanged

        with self.flow_extract_new_articles as _:                                                       # Use-case 4: with both current and previous
            _.current__path = self.current_path
            _.task__1__resolve__previous__path()
            assert _.current__path  == self.current_path                                                # current path is unchanged
            assert _.previous__path == self.previous_path                                               # previous path is unchanged

    def test_task__2__create__timeline_diff(self):
        with self.flow_extract_new_articles as _:
            if _.file_timeline_diff.exists() and _.file_timeline_diff.load().added_values[Time_Chain__Day] != {'20'}:               # make sure if exists file_timeline_diff it is the values we expect below
                _.file_timeline_diff.delete__now()
            _.task__2__create__timeline_diff()

            timeline_diff = _.file_timeline_diff.timeline_diff

            assert type(timeline_diff)       is Schema__MGraph__Diff__Values
            assert base_types(timeline_diff) == [Type_Safe, object]

            # since we are using cached data , these will always be the ame
            assert type  (timeline_diff) is Schema__MGraph__Diff__Values        # confirm data has been loaded into a new object of type Schema__MGraph__Diff__Values
            assert sorted(timeline_diff.added_values  [Time_Chain__Day   ]) == ['20']
            assert sorted(timeline_diff.removed_values[Time_Chain__Day   ]) == ['10']
            assert sorted(timeline_diff.added_values  [Time_Chain__Source]) == sorted([ '272b4927', 'e5091ea4', '5d2f8952', 'ce7e697e', 'd54c06c4', '9153bba8', '55b2f8d2'])
            assert sorted(timeline_diff.removed_values[Time_Chain__Source]) == sorted([ '468bfcf6', 'f2082031', '08ec0110', 'ea2a87d4', '0a68e403','d0ca70d4', '5f6bf957' ])
            assert _.file_timeline_diff.info() == { 'exists'     : True,
                                                    'path_latest': 'latest/feed-timeline-diff.json',
                                                    'path_now'   : f'{self.path_now}/feed-timeline-diff.json'}

    def test_task__3__save__new_articles(self):
        with self.flow_extract_new_articles as _:
            _.task__2__create__timeline_diff ()
            _.task__3__save__new_articles   ()

            assert _.file_new_articles.info () == { 'exists'     : True,
                                                    'path_latest': 'latest/articles-new.json',
                                                    'path_now'   : f'{self.path_now}/articles-new.json'}

            assert _.file_new_articles.new_articles.obj() == __(path__current  = self.current_path                       ,
                                                                path__previous = self.previous_path                      ,
                                                                timeline_diff  = _.file_timeline_diff.timeline_diff.obj())



    def test_task__4__update_current_articles(self):
        with self.flow_extract_new_articles as _:

            _.task__2__create__timeline_diff  ()
            _.task__4__update_current_articles()

            assert len(_.file_current_articles.articles.articles) > 0
            assert _.file_current_articles.info() == { 'exists'    : True,
                                                      'path_latest': 'latest/articles-current.json',
                                                      'path_now'   : f'{self.path_now}/articles-current.json'}

            for article_id, article  in _.file_current_articles.articles.articles.items():
                assert is_obj_id(article_id) is True
                assert list_set (article   ) == ['article_id'                                    ,
                                                 'next_step'                                     ,
                                                 'path__file__day__text_entities'                ,
                                                 'path__file__day__text_entities__png'           ,
                                                 'path__file__entities_mgraph__json'             ,
                                                 'path__file__entities_mgraph__png'              ,
                                                 'path__file__feed__text_entities'               ,
                                                 'path__file__feed__text_entities__descriptions' ,
                                                 'path__file__feed__text_entities__files'        ,
                                                 'path__file__feed__text_entities__titles'       ,
                                                 'path__file__feed__text_entities__titles__tree' ,
                                                 'path__file__feed_article'                      ,
                                                 'path__file__markdown'                          ,
                                                 'path__file__text_entities__description'        ,
                                                 'path__file__text_entities__description__mgraph',
                                                 'path__file__text_entities__description__png'   ,
                                                 'path__file__text_entities__mgraph'             ,
                                                 'path__file__text_entities__png'                ,
                                                 'path__file__text_entities__title'              ,
                                                 'path__file__text_entities__title__mgraph'      ,
                                                 'path__file__text_entities__title__png'         ,
                                                 'path__folder__data'                            ,
                                                 'path__folder__source'                          ,
                                                 'status'                                        ]
                assert article.article_id    == article_id

    def test_run(self):                                 # also tests task__6__create_output
        with self.flow_extract_new_articles as _:
            an_flow = _.run()
            assert type(an_flow)             == Flow
            assert an_flow.flow_return_value == _.output

            assert _.output ==  { 'file_current_articles': { 'exists'     : True,
                                                             'path_latest': 'latest/articles-current.json',
                                                             'path_now'   : f'{self.path_now}/articles-current.json'  },
                                  'file_new_articles'    : { 'exists'     : True,
                                                             'path_latest': 'latest/articles-new.json',
                                                             'path_now'   : f'{self.path_now}/articles-new.json'},
                                  'file_timeline_diff'   : { 'exists'     : True,
                                                             'path_latest': 'latest/feed-timeline-diff.json',
                                                            'path_now'    : f'{self.path_now}/feed-timeline-diff.json'},

                                  'path_current'        : _.current__path ,
                                  'path_previous'       : _.previous__path }

    # todo: wire back tests and use cases below (with the new code architecture)
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
