import pytest
from unittest                                                                               import TestCase
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Providers                              import Model__Data_Feeds__Providers
from myfeeds_ai.providers.cyber_security.docs_diniscruz_ai.actions.Docs_DinisCruz_Ai__Files import Docs_DinisCruz_Ai__Files, URL__DOCS_DINISCRUZ_AI
from myfeeds_ai.shared.http.schemas.Schema__Http__Action                                    import Schema__Http__Action
from osbot_utils.utils.Env                                                                  import not_in_github_action
from osbot_utils.utils.Functions                                                            import method_source_code
from tests.integration.data_feeds__objs_for_tests                                           import myfeeds_tests__setup_local_stack


class test_Docs_DinisCruz_Ai__Files(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.docs_files = Docs_DinisCruz_Ai__Files()

    def test__init__(self):
        with self.docs_files as _:
            assert _.base_url      == URL__DOCS_DINISCRUZ_AI
            assert _.provider_name ==  Model__Data_Feeds__Providers.DOCS_DINISCRUZ_AI
            assert _.provider_name == _.website_files.website_storage.s3_db.provider_name

    def test_home_page__data(self):
        with self.docs_files as _:
            result = _.home_page__data()
            assert type(result) is Schema__Http__Action



    # this test confirms the behaviour of the requests.get() response object, when used in an if statement
    #      the reason was a bug that we had where the initial expectation was that calling "if response:" would result in
    #      the normal behaviour of python objects (i.e. we could use it to detect if the "response" object was null or not)
    def test__requests__403__behaviour(self):
        if not_in_github_action():
            pytest.skip("only run this test in GH Actions")
        import requests
        from requests                    import Response
        from osbot_utils.helpers.ast.Ast import Ast

        request_ok  = requests.get("https://docs.diniscruz.ai"     )      # get a response object with 200 status code
        request_403 = requests.get("https://docs.diniscruz.ai/AAAA")      # get a response object with 403 status code

        assert type(request_ok)        is not None                        # confirm value is set
        assert type(request_ok )       is Response
        assert type(request_403)       is not None                        # confirm value is set
        assert type(request_403)       is Response

        assert request_ok.status_code  == 200                             # confirm ok request status_code
        assert request_403.status_code == 403                             # confirm 404 request status

        assert request_ok.ok           is True                            # confirm Ok value in ok and 404 requests
        assert request_403.ok          is False

        if request_ok:                                                    # confirm that the requests.ok is used on the equality comparison
            assert True
        if request_403:                                                   # this will
            assert False                                                  # this line will never execute


        source_code              = method_source_code(request_ok.__bool__)                  # now let's get the source code
        ast_module               = Ast().ast_module__from_source_code(source_code)          # convert it into an AST object
        ast_module__return_value = ast_module.body()[0].body()[1]                           # and get the AST of the return value
        assert source_code                            == ('def __bool__(self):\n'
                                                          '    """Returns True if :attr:`status_code` is less than 400.\n'
                                                          '\n'
                                                          '    This attribute checks if the status code of the response is between\n'
                                                          '    400 and 600 to see if there was a client error or a server error. If\n'
                                                          '    the status code, is between 200 and 400, this will return True. This\n'
                                                          '    is **not** a check to see if the response code is ``200 OK``.\n'
                                                          '    """\n'
                                                          '    return self.ok')
        assert ast_module__return_value.source_code() == 'return self.ok'
        assert ast_module__return_value.dump()        == ( 'Return(\n'
                                                            '    value=Attribute(\n'
                                                            "        value=Name(id='self', ctx=Load()),\n"
                                                            "        attr='ok',\n"
                                                     '        ctx=Load()))')
        assert ast_module__return_value.json() == {'Ast_Return': {'value': {'Ast_Attribute': {'attr' : 'ok'                                 ,
                                                                                              'ctx'  : {'Ast_Load': {}                      },
                                                                                              'value': {'Ast_Name': {'ctx': {'Ast_Load': {}}},
                                                                                                         'id'     : 'self'                  }}}}}

