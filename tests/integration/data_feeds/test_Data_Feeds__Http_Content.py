from unittest                                                   import TestCase
from myfeeds_ai.data_feeds.Data_Feeds__Http_Content             import Data_Feeds__Http_Content
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Raw_Data   import Model__Data_Feeds__Raw_Data
from osbot_aws.aws.s3.S3__DB_Base                               import DEFAULT__LOCAL_STACK__TARGET_SERVER
from osbot_utils.utils.Json                                     import str_to_json
from tests.integration.data_feeds__objs_for_tests               import myfeeds_tests__setup_local_stack

class test_Data_Feeds__Http_Content(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.server       = DEFAULT__LOCAL_STACK__TARGET_SERVER          # use localstack server since it will be up and it is fast
        cls.http_content = Data_Feeds__Http_Content(server=cls.server)

    def test_requests_get(self):
        with self.http_content as _:
            response = _.requests_get('_localstack/health')
            assert response.status_code == 200
            assert response.json().get('edition')  == 'community'

    def test_requests_get__raw_data(self):
        with self.http_content as _:
            raw_data     = _.requests_get__raw_data('_localstack/health')
            raw_data_obj = raw_data.obj()
            assert type(raw_data)                                is Model__Data_Feeds__Raw_Data
            assert str_to_json(raw_data.raw_data).get('edition') == 'community'
            assert raw_data_obj.duration                          < 0.02

