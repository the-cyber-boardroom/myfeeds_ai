import pytest
from unittest                                                                       import TestCase
from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                            import S3_Key__File__Extension
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__S3_DB             import Hacker_News__S3_DB
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage   import Hacker_News__Storage
from osbot_utils.utils.Misc                                                         import random_text
from osbot_utils.helpers.Safe_Id                                                    import Safe_Id
from tests.integration.data_feeds__objs_for_tests                                   import myfeeds_tests__setup_local_stack

class test_Hacker_News__Storage(TestCase):

    @classmethod                                                                       # Setup test environment
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()                                             # Ensure LocalStack is running
        cls.s3_db    = Hacker_News__S3_DB().setup()                                  # Setup and create test DB
        cls.storage  = Hacker_News__Storage(s3_db=cls.s3_db)

    def setUp(self):                                                                  # Per-test setup
        self.test_data = {"key": "value", "test": random_text()}
        self.file_id   = Safe_Id(random_text())
        self.extension = S3_Key__File__Extension.JSON
        self.file_name = f'{self.file_id}.{self.extension.value}'

    def tearDown(self):                                                              # Cleanup after each test
        with self.storage as _:
            _.delete_from__now   (self.file_id, self.extension)                      # Clean both locations
            _.delete_from__latest(self.file_id, self.extension)

    def test_save_to__now(self):                                                     # Test current timestamp save
        with self.storage as _:
            s3_path    = _.save_to__now  (self.test_data, self.file_id, self.extension)
            saved_data = _.load_from__now(self.file_id, self.extension)
            assert type(s3_path)  is str
            assert s3_path        in _.s3_db.provider__all_files()
            assert saved_data     == self.test_data
            assert self.file_name in  _.files_in__now()

    def test_save_to__latest(self):                                                  # Test latest version save
        with self.storage as _:
            s3_path    = _.save_to__latest  (self.test_data, self.file_id, self.extension)
            saved_data = _.load_from__latest(self.file_id, self.extension)
            assert type(s3_path)  is str
            assert s3_path        in _.s3_db.provider__all_files()
            assert saved_data     == self.test_data
            assert self.file_name in _.files_in__latest()

    def test_load_from__latest_and__now(self):                                      # Test both load methods
        with self.storage as _:
            # Save data to both locations with different values
            data_now    = {"type": "now"   , "value": random_text()}
            data_latest = {"type": "latest", "value": random_text()}
            alternate_id = Safe_Id(random_text())                                    # Create separate ID for additional test

            _.save_to__now   (data_now   , self.file_id, self.extension)
            _.save_to__latest(data_latest, self.file_id, self.extension)

            # Load and verify data from both locations
            loaded_now    = _.load_from__now   (self.file_id, self.extension)
            loaded_latest = _.load_from__latest(self.file_id, self.extension)

            assert loaded_now    == data_now
            assert loaded_latest == data_latest

            # Test loading non-existent data
            assert _.load_from__now   (alternate_id, self.extension) is None
            assert _.load_from__latest(alternate_id, self.extension) is None

            # Cleanup additional test data (since tearDown only cleans self.file_id)
            _.delete_from__now   (alternate_id, self.extension)
            _.delete_from__latest(alternate_id, self.extension)

    def test_delete_from__latest(self):                                             # Test delete from latest
        with self.storage as _:
            # Save test data
            s3_path = _.save_to__latest(self.test_data, self.file_id, self.extension)
            assert _.load_from__latest (self.file_id, self.extension)   == self.test_data
            assert self.file_name                                       in _.files_in__latest()     # Verify path is in latest


            deleted_path = _.delete_from__latest(self.file_id, self.extension)                      # Delete and verify
            assert deleted_path                                         == s3_path
            assert _.load_from__latest(self.file_id, self.extension)    is None
            assert self.file_name                                   not in _.files_in__latest()    # Verify path no longer in latest

    def test_delete_from__now(self):                                                # Test delete from now
        with self.storage as _:
            # Save test data
            s3_path = _.save_to__now(self.test_data, self.file_id, self.extension)
            assert _.load_from__now(self.file_id, self.extension) == self.test_data
            assert self.file_name                                 in _.files_in__now()
            # Delete and verify
            deleted_path = _.delete_from__now(self.file_id, self.extension)
            assert deleted_path == s3_path
            assert _.load_from__now(self.file_id, self.extension) is None

            # Verify path no longer in files
            assert self.file_name not in _.files_in__now()

    def test_delete_non_existent(self):                                             # Test deleting non-existent files
        with self.storage as _:
            alternate_id = Safe_Id(random_text())                                    # Use different ID to not conflict with tearDown

            # Should not raise exceptions for missing files
            path_latest = _.delete_from__latest(alternate_id, self.extension)       # return False when file doesn't exist
            path_now    = _.delete_from__now   (alternate_id, self.extension)       # returns None when file doesn't exist

            assert path_latest == False
            assert path_now    is None