from unittest                                                                 import TestCase
from mgraph_db.mgraph.schemas.Schema__MGraph__Diff__Values                    import Schema__MGraph__Diff__Values
from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types import Time_Chain__Day, Time_Chain__Source
from osbot_utils.utils.Json                                                   import json__equals__list_and_set

class test_Schema__MGraph__Diff__Values(TestCase):

    def test_json_roundtrip(self):

        json_data = { 'added_values'  : { 'mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types.Time_Chain__Day': [ '20'],
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
                                                                                                                                   '08ec0110']}}
        default_json = Schema__MGraph__Diff__Values().json()
        diff_values  = Schema__MGraph__Diff__Values.from_json(json_data)

        assert Schema__MGraph__Diff__Values.from_json(default_json).json() == default_json
        assert json__equals__list_and_set(Schema__MGraph__Diff__Values.from_json(json_data).json(), json_data)
        assert json__equals__list_and_set(diff_values.added_values ,  { Time_Chain__Day    : [ '20' ],
                                                                        Time_Chain__Source : [ '272b4927','e5091ea4','5d2f8952','9153bba8','ce7e697e','d54c06c4','55b2f8d2']})
