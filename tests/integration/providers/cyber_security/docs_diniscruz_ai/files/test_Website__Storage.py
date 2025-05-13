from unittest import TestCase

from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Providers import Model__Data_Feeds__Providers
from myfeeds_ai.providers.cyber_security.docs_diniscruz_ai.files.Website__Storage import Website__Storage
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Storage import Hacker_News__Storage
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import base_types


class test_Website__Storage(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.provider_name = Model__Data_Feeds__Providers.DOCS_DINISCRUZ_AI
        cls.website_storage = Website__Storage(provider_name=cls.provider_name)

    def test__init__(self):
        with self.website_storage as _:
            assert type(_) is Website__Storage
            assert base_types(_) == [Hacker_News__Storage, Type_Safe, object]
            assert _.s3_db.provider_name.value == 'docs-diniscruz-ai'

