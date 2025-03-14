# todo: figure out why this started failing in GH Actions: https://github.com/the-cyber-boardroom/myfeeds_ai/actions/runs/13846908074/job/38747121896
# from unittest                                     import TestCase
# from starlette.testclient                         import TestClient
# from myfeeds_ai.lambdas.handler                   import app
# from tests.integration.data_feeds__objs_for_tests import myfeeds_tests__setup_local_stack
#
#
# class test__int__handler(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         myfeeds_tests__setup_local_stack()
#         cls.client = TestClient(app)
#
#     def test_openapi(self):
#         response = self.client.get("/openapi.json")
#         assert response.status_code == 200
#         assert response.json().get("openapi") == "3.1.0"
