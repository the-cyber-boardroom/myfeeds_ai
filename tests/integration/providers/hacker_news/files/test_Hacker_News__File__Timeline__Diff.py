from unittest                                                                                   import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Diff__Values                                      import Schema__MGraph__Diff__Values
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types                   import Time_Chain__Day, Time_Chain__Source
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Timeline__Diff    import Hacker_News__File__Timeline__Diff
from tests.integration.data_feeds__objs_for_tests                                               import cbr_website__assert_local_stack


class test_Hacker_News__File__Timeline__Diff(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()                               # make sure we are using localstack
        cls.current_path  = '2025/02/20/23'                             # use these two in order to have a deterministic data set in the tests below
        cls.previous_path = '2025/02/19/22'
        cls.file_timeline_diff = Hacker_News__File__Timeline__Diff()

    def test__init__(self):
        with self.file_timeline_diff as _:
            assert _.file_name() == 'feed-timeline-diff.json'

    def test_create__load(self):
        with self.file_timeline_diff as _:
            if _.not_exists():
                _.create(current_path=self.current_path, previous_path=self.previous_path)
            else:
                _.load()

            assert type(_.timeline_diff)                                      is Schema__MGraph__Diff__Values        # confirm data has been loaded into a new object of type Schema__MGraph__Diff__Values
            assert sorted(_.timeline_diff.added_values  [Time_Chain__Day   ]) == ['20']                              # confirm diff worked as expected
            assert sorted(_.timeline_diff.removed_values[Time_Chain__Day   ]) == ['10']                              #         note: this data is based on the current hard-coded previous_path and current_path
            assert sorted(_.timeline_diff.added_values  [Time_Chain__Source]) == sorted([ '272b4927', 'e5091ea4', '5d2f8952', 'ce7e697e', 'd54c06c4', '9153bba8', '55b2f8d2'])
            assert sorted(_.timeline_diff.removed_values[Time_Chain__Source]) == sorted([ '468bfcf6', 'f2082031', '08ec0110', 'ea2a87d4', '0a68e403','d0ca70d4', '5f6bf957' ])

    def test_save(self):
        with self.file_timeline_diff as _:
            file_name = _.file_name()
            if _.not_exists():
                _.create(current_path=self.current_path, previous_path=self.previous_path)
            _.save()
            assert file_name  == 'feed-timeline-diff.json'
            assert file_name  in _.hacker_news_storage.files_in__now   ()
            assert file_name  in _.hacker_news_storage.files_in__latest()
            assert _.exists() is True


