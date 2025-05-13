from unittest                                                           import TestCase
from myfeeds_ai.shared.http.Http__Request__Cache                        import Http__Request__Cache
from myfeeds_ai.shared.http.Http__Request__Execute__Requests            import Http__Request__Execute__Requests
from myfeeds_ai.shared.http.schemas.Schema__Http__Request               import Schema__Http__Request
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Cache__Entry import Schema__Http__Request__Cache__Entry
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Methods      import Schema__Http__Request__Methods
from myfeeds_ai.shared.http.schemas.Schema__Http__Response              import Schema__Http__Response
from osbot_utils.helpers.Obj_Id                                         import Obj_Id
from osbot_utils.helpers.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from osbot_utils.helpers.safe_str.Safe_Str__Url                         import Safe_Str__Url
from osbot_utils.utils.Objects                                          import __
from tests.integration.data_feeds__objs_for_tests                       import myfeeds_tests__setup_local_stack


class test__int__Http__Request__Cache(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.http_request_execute = Http__Request__Execute__Requests()
        cls.http_request_cache   = Http__Request__Cache  ()

    def test_add__cache_entry(self):
        with self.http_request_cache as _:
            # create test data
            cache_hash  = Safe_Str__Hash('0123456789')
            request     = Schema__Http__Request(cache__hash=cache_hash)
            response    = Schema__Http__Response()
            # add request and response
            cache_id    = _.add__cache_entry(request, response)
            cache_entry = _.cache_entries[cache_id]
            assert type(cache_id   )                                       is Obj_Id
            assert type(cache_entry)                                       is Schema__Http__Request__Cache__Entry
            assert cache_entry.request                                     == request
            assert cache_entry.response                                    == response
            assert cache_entry.cache_id                                    == cache_id
            assert _.cache_index.cache_id__from__hash__request[cache_hash] == cache_id

            # Check if it exists
            assert _.exists(request) is True  # Item should exist in cache

            # Retrieve it
            cached_entry = _.get__cache_entry__from__request(request)
            assert cached_entry == cache_entry
            assert _.get__response__by_id(cache_id) == response

            # Delete it
            assert _.delete__using__request(request=request) is True
            assert _.exists(request)                         is False



    def test_calculate_hash(self):
        method  = Schema__Http__Request__Methods.GET
        url     = Safe_Str__Url('https://docs.diniscruz.ai')
        params  = dict(a=42)
        with self.http_request_cache as _:
            request_hash = _.calculate_hash(method, url)
            assert type(request_hash) is Safe_Str__Hash
            assert _.calculate_hash(method, url                 ) == '9844727eea'
            assert _.calculate_hash(method, url, params         ) == '1e7ddc810b'


    def test_create_cache_entry(self):
        method  = Schema__Http__Request__Methods.GET
        url     = Safe_Str__Url('https://docs.diniscruz.ai')
        with self.http_request_execute as _:
            request  = _.create_http_request(method=method, url=url)
            response  = _.execute__http_request(request=request)

        with self.http_request_cache as _:
            cache_entry = _.create_cache_entry(request=request, response=response)
            assert type(cache_entry) is Schema__Http__Request__Cache__Entry
            assert cache_entry.obj()  == __(cache_id  = cache_entry.cache_id  ,
                                            request   = request .obj()        ,
                                            response  = response.obj()        ,
                                            timestamp = cache_entry.timestamp )