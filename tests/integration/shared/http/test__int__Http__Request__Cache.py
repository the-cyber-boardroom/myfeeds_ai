from unittest                                                           import TestCase
from myfeeds_ai.shared.http.Http__Request__Cache                        import Http__Request__Cache
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Cache__Entry import Schema__Http__Request__Cache__Entry
from osbot_utils.helpers.safe_str.Safe_Str__Hash                        import Safe_Str__Hash
from osbot_utils.helpers.safe_str.Safe_Str__Url                         import Safe_Str__Url
from osbot_utils.utils.Misc                                             import list_set
from tests.integration.data_feeds__objs_for_tests                       import myfeeds_tests__setup_local_stack


class test__int__Http__Request__Cache(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.http_request_cache = Http__Request__Cache()

    def test_compute_request_hash(self):
        url     = Safe_Str__Url('https://docs.diniscruz.ai')
        params  = dict(a=42)
        headers = dict(api_key=123)
        with self.http_request_cache as _:
            request_hash = _.compute_request_hash(url)
            assert type(request_hash) is Safe_Str__Hash
            assert _.compute_request_hash(url                 ) == '2eb8eb2deb'
            assert _.compute_request_hash(url, params         ) == '0e2ac8f081'
            assert _.compute_request_hash(url, params, headers) == '8240ec2a5a'


    def test_requests__get__cache_entry(self):
        url = Safe_Str__Url('https://docs.diniscruz.ai')
        with self.http_request_cache as _:
            cache_entry = _.requests__get__cache_entry(url)
            html__dict  = cache_entry.html__dict
            assert type(cache_entry           ) is Schema__Http__Request__Cache__Entry
            assert type(html__dict)             is dict
            assert list_set(html__dict)         == ['attrs', 'children', 'data', 'tag']
            assert html__dict.get('attrs')      == {'class': 'no-js', 'lang': 'en'}