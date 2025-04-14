from unittest                                               import TestCase
from osbot_fast_api.utils.Fast_API__Server_Info             import fast_api__server_info
from myfeeds_ai.fast_api.admin.Admin__Fast_API              import Admin__Fast_API, ENV_VAR__AUTH__MYFEEDS__API_KEY__NAME, ENV_VAR__AUTH__MYFEEDS__API_KEY__VALUE
from myfeeds_ai.fast_api.admin.Middleware__Check_API_Key    import ERROR_MESSAGE__API_KEY_MISSING
from osbot_utils.utils.Env                                  import load_dotenv, get_env


# todo: replace with the version in osbot-fast-api (when that is available in pypi)
class test_Admin__Fast_API(TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.admin_fastapi = Admin__Fast_API().setup()
        cls.client        = cls.admin_fastapi.client()

    # def test_client__config__info(self):
    #     with self.client as _:
    #         response = _.get('config/info')
    #         assert response.status_code == 200
    #         assert response.json()      == fast_api__server_info.json()

    def test__setup_middlewares(self):
        expected_middleware = { 'function_name' : None                                                               ,
                                'params'        : {'env_var__api_key__name' : ENV_VAR__AUTH__MYFEEDS__API_KEY__NAME   ,
                                                   'env_var__api_key__value': ENV_VAR__AUTH__MYFEEDS__API_KEY__VALUE} ,
                                'type'          : 'Middleware__Check_API_Key'                                        }
        with self.admin_fastapi as _:
            assert expected_middleware in _.user_middlewares()

            response = self.client.get('config/info')
            assert response.status_code == 401
            key_name  = get_env(ENV_VAR__AUTH__MYFEEDS__API_KEY__NAME )
            admin_key = get_env(ENV_VAR__AUTH__MYFEEDS__API_KEY__VALUE)
            if admin_key:
                assert response.json() == {'error': ERROR_MESSAGE__API_KEY_MISSING}
                response_with_key = self.client.get('config/info', headers={key_name:admin_key})
                assert response_with_key.status_code == 200
                assert response_with_key.json()      == fast_api__server_info.json()
            else:
                assert response.json() == {'error': 'Server does not have API key setup'}