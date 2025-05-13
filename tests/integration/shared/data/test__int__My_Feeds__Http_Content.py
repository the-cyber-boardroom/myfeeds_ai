from unittest                                                           import TestCase
from myfeeds_ai.shared.data.My_Feeds__Http_Content                      import My_Feeds__Http_Content
from osbot_aws.aws.s3.S3__DB_Base                                       import DEFAULT__LOCAL_STACK__TARGET_SERVER
from tests.integration.data_feeds__objs_for_tests                       import myfeeds_tests__setup_local_stack

class test__int__My_Feeds__Http_Content(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.server       = DEFAULT__LOCAL_STACK__TARGET_SERVER          # use localstack server since it will be up and it is fast
        cls.http_content = My_Feeds__Http_Content(server=cls.server)

    def test_requests_get(self):
        with self.http_content as _:
            response = _.requests_get('_localstack/health')
            assert response.status_code == 200
            assert response.json().get('edition')  == 'community'
#
#     def test_requests_get__cache_entry(self):
#         server = 'https://docs.diniscruz.ai'
#         with My_Feeds__Http_Content(server=server).requests_get__cache_entry() as _:
#             assert type(_) is Schema__Http__Request__Cache__Entry
#             html_dict = _.html__dict
#             assert type(html_dict) is dict
#             assert _.json__data  is None
#             assert _.method      == 'GET'
#             assert _.status_code == 200
#             assert _.url         == 'https://docs.diniscruz.ai/'
#             assert _.url__hash   == '0dc4021083'
#
#
#     def test_requests_get__data__json(self):
#         target_path = '_localstack/health'
#         with self.http_content.requests_get__cache_entry(path=target_path) as _:
#             assert type(_) is Schema__Http__Request__Cache__Entry
#             assert _.json() == { 'content_type' : 'application_json',
#                                  'duration'     : _.duration,
#                                  'etag'         : '',
#                                  'html__dict'   : None,
#                                  'json__data'   : { 'edition' : 'community',
#                                                     'services': _.json__data.get('services') ,
#                                                     'version' : '3.8.2.dev15'},
#                                  'last_modified': '',
#                                  'method'       : 'GET',
#                                  'status_code'  : 200,
#                                  'text'         : _.text,
#                                  'text__hash': 'fdc6176fe6',
#                                  'timestamp'    : _.timestamp,
#                                  'url'          : 'http://localhost:4566/_localstack/health',
#                                  'url__hash'    : '6111337f3d'}
#
#     def test_requests_get__raw_data(self):
#         with self.http_content as _:
#             raw_data     = _.requests_get__raw_data('_localstack/health')
#             raw_data_obj = raw_data.obj()
#             assert type(raw_data)                                is Model__Data_Feeds__Raw_Data
#             assert str_to_json(raw_data.raw_data).get('edition') == 'community'
#             assert raw_data_obj.duration                          < 0.02
#
