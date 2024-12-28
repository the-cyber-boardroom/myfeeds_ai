import pytest
from unittest                                import TestCase
from osbot_utils.utils.Objects               import obj
from osbot_utils.utils.Env                   import load_dotenv
from myfeeds_ai.data_feeds.Data_Feeds__S3_DB import Data_Feeds__S3_DB


class test_Data_Feeds__S3_DB(TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.s3_db = Data_Feeds__S3_DB()

    @pytest.mark.skip("this needs to wired as part of the update")
    def test_invalidate_cache(self):
        with self.s3_db as _:
            result = obj(_.invalidate_cache())
            assert result.InvalidationBatch.Paths.Items == [ '/public-data/hacker-news/latest/*']