from unittest                                                           import TestCase
from myfeeds_ai.shared.http.Http__Request__Cache                        import Http__Request__Cache
from myfeeds_ai.shared.http.Http__Request__Execute import Http__Request__Execute
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Cache__Entry import Schema__Http__Request__Cache__Entry
from osbot_utils.helpers.duration.decorators.print_duration import print_duration
from osbot_utils.helpers.safe_str.Safe_Str import Safe_Str
from osbot_utils.helpers.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from osbot_utils.helpers.safe_str.Safe_Str__Url                         import Safe_Str__Url
from osbot_utils.utils.Misc                                             import list_set
from osbot_utils.utils.Objects import __
from tests.integration.data_feeds__objs_for_tests                       import myfeeds_tests__setup_local_stack


class test__int__Http__Request__Cache(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.http_request_execute = Http__Request__Execute()
        cls.http_request_cache   = Http__Request__Cache()

    def test_calculate_hash(self):
        method  = Safe_Str('GET')
        url     = Safe_Str__Url('https://docs.diniscruz.ai')
        params  = dict(a=42)
        with self.http_request_cache as _:
            request_hash = _.calculate_hash(method, url)
            assert type(request_hash) is Safe_Str__Hash
            assert _.calculate_hash(method, url                 ) == '9844727eea'
            assert _.calculate_hash(method, url, params         ) == '1e7ddc810b'


    def test_create_cache_entry(self):
        method  = Safe_Str('GET')
        url     = Safe_Str__Url('https://docs.diniscruz.ai')
        with self.http_request_execute as _:
            request  = _.create_http_request(method=method, url=url)
            response  = _.requests_get(request=request)

        with self.http_request_cache as _:
            cache_entry = _.create_cache_entry(request=request, response=response)
            assert type(cache_entry) is Schema__Http__Request__Cache__Entry
            assert cache_entry.obj()  == __(cache_id  = cache_entry.cache_id  ,
                                            request   = request .obj()        ,
                                            response  = response.obj()        ,
                                            timestamp = cache_entry.timestamp )