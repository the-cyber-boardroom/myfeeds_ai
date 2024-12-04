from unittest                                             import TestCase
from osbot_fast_api.utils.Version                         import version__osbot_fast_api
from osbot_utils.utils.Json                               import str_to_json
from osbot_utils.utils.Objects                            import dict_to_obj, __, str_to_obj
from deploy.lambdas.Deploy_Lambda__Cbr_Custom__News_Feeds import Deploy_Lambda__Cbr_Custom_News_Feeds


class test__live_lambda_function(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.deploy_lambda   = Deploy_Lambda__Cbr_Custom_News_Feeds()
        cls.lambda_function = cls.deploy_lambda.lambda_function

    def test__check_lambda_deployment(self):
        with self.lambda_function as _:
            assert _.exists             () is True
            assert _.function_url_exists() is True

    def lambda_payload(self, path='/', method='GET', headers=None):
        return { "headers"                        : headers or {},
                 "rawPath"                        : path,
                 "requestContext"                 : {"http": { "method": method}}}


    def test_invoke(self):
        with self.lambda_function as _:
            assert obj(_.invoke()) == __(detail='Not Found')

            payload__config_info    = self.lambda_payload('/config/status' )
            payload__config_version = self.lambda_payload('/config/version')
            payload__open_api_json  = self.lambda_payload('/openapi.json'  )
            result__config_info     = obj(_.invoke(payload__config_info    ))
            result__config_version  = obj(_.invoke(payload__config_version ))
            result__open_api_json   = obj(_.invoke(payload__open_api_json  ))
            config_version          = str_to_json(result__config_version.body)
            open_api_json           = str_to_obj(result__open_api_json .body)
            assert result__config_info.statusCode           == 200
            assert result__config_info.headers.server       == 'uvicorn'
            assert result__config_info.body                 == '{"status":"ok"}'
            assert result__config_info.isBase64Encoded      == False
            assert result__config_info.cookies              == []
            assert config_version                           == {"version": version__osbot_fast_api }
            assert open_api_json.openapi                    =='3.1.0'
            assert open_api_json.info.title                 == 'FastAPI'

    # def test_invoke_with_logs(self):
    #     with self.lambda_function as _:
    #         result = obj(_.invoke_return_logs())
    #         pprint(result)


obj = dict_to_obj