from unittest import TestCase

import pytest

from mgraph_db.query.MGraph__Query                                                                              import MGraph__Query
from mgraph_db.mgraph.actions                                                                                   import MGraph__Index
from mgraph_db.providers.time_series.MGraph__Time_Series                                                        import MGraph__Time_Series
from myfeeds_ai.providers.cyber_security.hacker_news.Hacker_News__Files import Hacker_News__Files

from osbot_utils.context_managers.print_duration                                                                import print_duration
from osbot_utils.type_safe.shared.Type_Safe__Json_Compressor                                                    import Type_Safe__Json_Compressor

from myfeeds_ai.providers.cyber_security.hacker_news.flows.Flow__Hacker_News__Create_MGraph__Articles__Timeline import Flow__Hacker_News__Create_MGraph__Articles__Timeline, S3_FILE_NAME__MGRAPH__TIMELINE
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env                                                                                      import load_dotenv
from osbot_utils.utils.Json                                                                                     import json_file_contents
from osbot_utils.utils.Misc import size, list_set
from tests.integration.data_feeds__objs_for_tests                                                               import cbr_website__assert_local_stack

class test__int__Flow__Hacker_News__Create_MGraph__Articles__Timeline(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cbr_website__assert_local_stack()
        cls.files     =  Hacker_News__Files()
        cls.data_feed = cls.files.feed_data__current()
        cls.flow__articles_timeline = Flow__Hacker_News__Create_MGraph__Articles__Timeline()

    def test_execute(self):
        load_dotenv()
        with self.flow__articles_timeline as _:
            _.setup(data_feed=self.data_feed)
            _.execute_flow()
            _.print_log_messages()

    # def test_create_query_visualisation(self):
    #     with print_duration():
    #         mgraph_json__compressed = json_file_contents(S3_FILE_NAME__MGRAPH__TIMELINE)
    #         mgraph_json = Type_Safe__Json_Compressor().decompress(mgraph_json__compressed)                    # todo: add helper method to do this import from compressed
    #         mgraph      = MGraph__Time_Series.from_json(mgraph_json)
    #
    #         # query : MGraph__Query = mgraph.query()
    #         # with query as _:
    #
    #         #with query as _:


