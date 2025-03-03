from unittest                                                                              import TestCase
from mgraph_db.mgraph.MGraph                                                               import MGraph
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                   import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage          import Hacker_News__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.mgraphs.Hacker_News__MGraph           import Hacker_News__MGraph
from osbot_utils.helpers.Safe_Id                                                           import Safe_Id
from tests.integration.data_feeds__objs_for_tests                                          import cbr_website__assert_local_stack


class test_Hacker_News__MGraph(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()                                                           # Ensure LocalStack is running
        cls.hacker_news_storage = Hacker_News__Storage()

    def setUp(self):
        self.file_id            = Safe_Id()                                                         # Create unique file ID for each test
        self.mgraph             = MGraph()                                                          # Create a fresh MGraph instance
        self.hacker_news_mgraph = Hacker_News__MGraph(mgraph              = self.mgraph             ,
                                                      hacker_news_storage = self.hacker_news_storage,
                                                      file_id             = self.file_id            )

    def tearDown(self):
        self.hacker_news_mgraph.delete__now()                                                       # Clean up any files created during tests
        self.hacker_news_mgraph.delete__latest()

    def test_init(self):
        assert self.hacker_news_mgraph.file_id             == self.file_id                          # Test proper initialization
        assert self.hacker_news_mgraph.mgraph              == self.mgraph
        assert self.hacker_news_mgraph.hacker_news_storage == self.hacker_news_storage

    def test_path_now(self):                                                                        # Test path_now method returns expected path format
        path_now = self.hacker_news_mgraph.path_now()
        assert type(path_now)                                                                   is str
        assert path_now.endswith(f"{self.file_id}.{S3_Key__File_Extension.MGRAPH__JSON.value}") is True

    def test_path_latest(self):                                                                     # Test path_latest method returns expected path format
        path_latest = self.hacker_news_mgraph.path_latest()
        assert type(path_latest)                                                                   is str
        assert path_latest.endswith(f"{self.file_id}.{S3_Key__File_Extension.MGRAPH__JSON.value}") is True
        assert 'latest' in path_latest.lower()

    def test_file_name(self):                                                                      # Test file_name method
        file_name = self.hacker_news_mgraph.file_name()
        expected_file_name = f"{self.file_id}.{S3_Key__File_Extension.MGRAPH__JSON.value}"
        assert file_name == expected_file_name

    def test_exists_methods_when_files_dont_exist(self):                                           # Test exists methods when files don't exist
        assert self.hacker_news_mgraph.exists__now()    is False                                   # Should return False initially since we haven't saved anything
        assert self.hacker_news_mgraph.exists__latest() is False
        assert self.hacker_news_mgraph.exists()         is False

    def test_save_load_and_exists(self):                                                           # Test save, exists, and load methods
        assert self.hacker_news_mgraph.exists__now()    is False                                   # Initially files don't exist
        assert self.hacker_news_mgraph.exists__latest() is False

        with self.mgraph.edit() as _:                                                              # Add a node to the graph to make it non-empty
            node = _.new_value(value="test value")

        self.hacker_news_mgraph.save()                                                             # Save the graph

        assert self.hacker_news_mgraph.exists__now()    is True                                    # Now files should exist
        assert self.hacker_news_mgraph.exists__latest() is True
        assert self.hacker_news_mgraph.exists()         is True

        new_mgraph = MGraph()                                                                     # Create a new MGraph instance
        new_hacker_news_mgraph = Hacker_News__MGraph(mgraph              = new_mgraph             ,
                                                     hacker_news_storage = self.hacker_news_storage,
                                                     file_id             = self.file_id            )

        new_hacker_news_mgraph.load()                                                             # Load the graph

        assert self.mgraph.data().json() == new_hacker_news_mgraph.mgraph.data().json()
        assert new_mgraph .data().json() != new_hacker_news_mgraph.mgraph.data().json()

        with new_hacker_news_mgraph.mgraph.data() as _:                                                              # Verify the node was loaded correctly
            nodes = _.nodes()
            assert len(nodes)                == 1
            assert nodes[0].node_data.value == "test value"

    def test_delete__now(self):                                                                   # Test delete__now method
        with self.mgraph.edit() as _:                                                             # Save something first
            _.new_node(value="test value")
        self.hacker_news_mgraph.save()

        assert self.hacker_news_mgraph.exists__now  () is True                                      # Verify it exists

        result = self.hacker_news_mgraph.delete__now()                                            # Delete and verify it no longer exists
        assert result                                  is True
        assert self.hacker_news_mgraph.exists__now  () is False

        result = self.hacker_news_mgraph.delete__now()                                            # Deleting non-existent should still work
        assert self.hacker_news_mgraph.exists__now  () is False                                     # No assertion on result as it might be True or False depending on implementation

    def test_delete__latest(self):                                                                # Test delete__latest method
        with self.mgraph.edit() as _:                                                             # Save something first
            _.new_node(value="test value")
        self.hacker_news_mgraph.save()

        assert self.hacker_news_mgraph.exists__latest  () is True                                   # Verify it exists

        result = self.hacker_news_mgraph.delete__latest()                                         # Delete and verify it no longer exists
        assert result                                     is True
        assert self.hacker_news_mgraph.exists__latest  () is False

        result = self.hacker_news_mgraph.delete__latest()                                         # Deleting non-existent should still work
        assert self.hacker_news_mgraph.exists__latest  () is False                                  # No assertion on result as it might be True or False depending on implementation

    def test_save_validation(self):                                                               # Test that save validates paths correctly
        with self.mgraph.edit() as _:                                                             # Add a node to make the graph non-empty
            _.new_node(value="test value")

        self.hacker_news_mgraph.save()                                                            # Normal save should work fine

        expected_path_now    = self.hacker_news_mgraph.path_now()                                 # Verify that the expected paths are what's being checked against
        expected_path_latest = self.hacker_news_mgraph.path_latest()

        assert expected_path_now.endswith(f"{self.file_id}.{S3_Key__File_Extension.MGRAPH__JSON.value}")    is True
        assert expected_path_latest.endswith(f"{self.file_id}.{S3_Key__File_Extension.MGRAPH__JSON.value}") is True