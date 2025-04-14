from unittest                                               import TestCase
from osbot_fast_api.api.Fast_API                            import ENV_VAR__FAST_API__AUTH__API_KEY__NAME, ENV_VAR__FAST_API__AUTH__API_KEY__VALUE
from osbot_fast_api.api.middlewares.Middleware__Check_API_Key import ERROR_MESSAGE__API_KEY_MISSING, \
    ERROR_MESSAGE__NO_KEY_NAME_SETUP
from osbot_fast_api.utils.Fast_API__Server_Info             import fast_api__server_info
from myfeeds_ai.fast_api.admin.Admin__Fast_API              import Admin__Fast_API
from osbot_utils.utils.Env                                  import load_dotenv, get_env
from osbot_utils.utils.Status import status_error


class test_Admin__Fast_API(TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.admin_fastapi = Admin__Fast_API().setup()
        cls.client        = cls.admin_fastapi.client()

    def test__setup_middlewares(self):
        expected_middleware = { 'function_name' : None                                                               ,
                                'params'        : {'env_var__api_key__name' : ENV_VAR__FAST_API__AUTH__API_KEY__NAME   ,
                                                   'env_var__api_key__value': ENV_VAR__FAST_API__AUTH__API_KEY__VALUE} ,
                                'type'          : 'Middleware__Check_API_Key'                                        }
        with self.admin_fastapi as _:
            assert expected_middleware in _.user_middlewares()

            response = self.client.get('config/info')
            assert response.status_code == 401

            key_name  = get_env(ENV_VAR__FAST_API__AUTH__API_KEY__NAME )
            admin_key = get_env(ENV_VAR__FAST_API__AUTH__API_KEY__VALUE)
            if admin_key:
                assert response.json()      == status_error(ERROR_MESSAGE__API_KEY_MISSING)
                response_with_key = self.client.get('config/info', headers={key_name:admin_key})
                assert response_with_key.status_code == 200
                assert response_with_key.json()      == fast_api__server_info.json()