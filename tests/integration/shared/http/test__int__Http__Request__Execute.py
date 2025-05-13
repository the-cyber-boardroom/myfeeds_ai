from unittest                                                       import TestCase
from myfeeds_ai.shared.http.Http__Request__Execute__Requests        import Http__Request__Execute__Requests
from myfeeds_ai.shared.http.schemas.Schema__Http__Request           import Schema__Http__Request
from myfeeds_ai.shared.http.schemas.Schema__Http__Request__Methods  import Schema__Http__Request__Methods
from myfeeds_ai.shared.http.schemas.Schema__Http__Response          import Schema__Http__Response
from osbot_utils.helpers.safe_str.Safe_Str__Url                     import Safe_Str__Url
from osbot_utils.helpers.safe_str.http.Safe_Str__Http__Text         import Safe_Str__Http__Text
from tests.integration.data_feeds__objs_for_tests                   import myfeeds_tests__setup_local_stack


class test__int__Http__Request__Cache(TestCase):
    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.http_request_execute = Http__Request__Execute__Requests()  # use this version since the Http__Request__Execute.execute__http_request is currently not implemented

    def test_create_request(self):
        method = Schema__Http__Request__Methods.GET
        url    = Safe_Str__Url('https://docs.diniscruz.ai')
        with self.http_request_execute.create_http_request(method=method, url=url) as _:
            assert type(_) is Schema__Http__Request

    def test_execute(self):
        method = Schema__Http__Request__Methods.GET
        url    = Safe_Str__Url("https://docs.diniscruz.ai/")
        with self.http_request_execute as _:
            request  = _.create_http_request(method, url)
            response = _.execute(request)
            assert type(response) is Schema__Http__Response
            assert type(response.text) == Safe_Str__Http__Text
            #html_to_tag = Html_To_Tag(response.text).convert()
            #pprint(html_to_tag.json())
            #print(response.text)
