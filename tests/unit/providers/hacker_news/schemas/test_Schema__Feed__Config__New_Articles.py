from unittest                                                                                   import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Config__New_Articles import Schema__Feed__Config__New_Articles
from osbot_utils.utils.Json                                                                     import json__equals__list_and_set


class test_Schema__Feed__Config__New_Articles(TestCase):

    def test_json_roundtrip(self):

        json_data = { 'path__current': '2025/02/20/23',
                      'path__previous': '2025/02/19/22',
                      'timeline_diff': { 'added_values': { 'mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types.Time_Chain__Day': [ '20'],
                                                           'mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types.Time_Chain__Source': [ '5d2f8952',
                                                                                                                                                            '9153bba8',
                                                                                                                                                            '272b4927',
                                                                                                                                                            'e5091ea4',
                                                                                                                                                            'd54c06c4',
                                                                                                                                                            '55b2f8d2',
                                                                                                                                                            'ce7e697e']},
                                         'removed_values': { 'mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types.Time_Chain__Day': [ '10'],
                                                             'mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types.Time_Chain__Source': [ 'd0ca70d4',
                                                                                                                                                              '468bfcf6',
                                                                                                                                                              'ea2a87d4',
                                                                                                                                                              '0a68e403',
                                                                                                                                                              'f2082031',
                                                                                                                                          '5f6bf957',
                                                                                                                                           '08ec0110']}}}

        default_json = Schema__Feed__Config__New_Articles().json()
        assert Schema__Feed__Config__New_Articles.from_json(default_json).json() == default_json
        assert json__equals__list_and_set(Schema__Feed__Config__New_Articles.from_json(json_data).json(),  json_data)