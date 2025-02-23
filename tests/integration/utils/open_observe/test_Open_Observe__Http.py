from unittest                                           import TestCase
from datetime                                           import datetime

from requests import Session
from requests.auth                                      import HTTPBasicAuth
from myfeeds_ai.utils.open_observe.Open_Observe__Http   import Open_Observe__Http, Schema__Open_Observe__Server_Config, ENV_NAME__OPEN_OBSERVE__API_KEY, ENV_NAME__OPEN_OBSERVE__HOST, ENV_NAME__OPEN_OBSERVE__ORG, ENV_NAME__OPEN_OBSERVE__STREAM, ENV_NAME__OPEN_OBSERVE__USER, DEFAULT__CONFIG__HOST, DEFAULT__CONFIG__STREAM
from osbot_utils.utils.Env                              import load_dotenv, get_env


class test_Open_Observe__Http(TestCase):

    @classmethod
    def setUpClass(cls) -> None:                                                           # Check if we can run testsp

        if True: #cls.config.enabled is False:                                              # todo: needs bulk suport so that we can send the Flow's task data after it has been completed (not before)
            import pytest
            pytest.skip("Open_Observe env vars are not set")
        load_dotenv()
        cls.open_observe = Open_Observe__Http()
        cls.config = cls.open_observe.config()

    def setUp(self):
        self.test_id = f'test__{datetime.now().strftime("%Y%m%d_%H%M%S")}'               # Unique ID for test data

    def test_config(self):                                                                # Test config loading
        assert type(self.config)           is Schema__Open_Observe__Server_Config
        assert self.config.api_key         == get_env(ENV_NAME__OPEN_OBSERVE__API_KEY                         )
        assert self.config.host            == get_env(ENV_NAME__OPEN_OBSERVE__HOST   , DEFAULT__CONFIG__HOST  )
        assert self.config.organisation    == get_env(ENV_NAME__OPEN_OBSERVE__ORG                             )
        assert self.config.stream          == get_env(ENV_NAME__OPEN_OBSERVE__STREAM , DEFAULT__CONFIG__STREAM)
        assert self.config.user            == get_env(ENV_NAME__OPEN_OBSERVE__USER                            )
        assert self.config.enabled         is True

    def test_session(self):                                                               # Test session creation
        session = self.open_observe.session()
        assert type(session)                           is Session
        assert session.headers['Content-Type']         == 'application/json'
        assert isinstance(session.auth, HTTPBasicAuth) is True
        assert session.auth.username                   == self.config.user
        assert session.auth.password                   == self.config.api_key

    def test_url__json(self):                                                                                           # Test URL JSON generation
        with self.config as _:
            assert self.open_observe.url__json() == f'https://{_.host}/api/{_.organisation}/{_.stream}/_json'

    def test_send_data(self):                                                            # Test sending multiple logs
        data = [
            {"level": "info" , "job": self.test_id, "log": "Message 1"},
            {"level": "warn" , "job": self.test_id, "log": "Message 2"},
            {"level": "error", "job": self.test_id, "log": "Message 3"}
        ]
        result = self.open_observe.send_data(data)
        assert result is True

    def test_send_error_data(self):                                                      # Test sending invalid data
        invalid_data = [{"invalid": "data"}]                                             # Data missing required fields
        result = self.open_observe.send_data(invalid_data)
        assert result is True                                                            # Should succeed as API accepts it

    # def test_send_batch(self):                                                           # Test sending batch data
    #     data = [
    #         {"level": "info", "job": self.test_id, "log": f"Batch message {i}"}
    #         for i in range(5)                                                            # Create 5 test messages
    #     ]
    #     result = self.open_observe.send_batch(data)
    #     assert result is True
    # def test_multiple_batches(self):                                                     # Test multiple batch sends
    #     for i in range(3):                                                               # Send 3 batches
    #         data = [
    #             {"level": "info", "job": f"{self.test_id}__{i}", "log": f"Message {j}"}
    #             for j in range(3)                                                        # 3 messages per batch
    #         ]
    #         result = self.observer.send_batch(data)
    #         assert result is True
    # def test_url__bulk(self):                                                                                           # Test URL JSON generation
    #     with self.config as _:
    #         assert self.open_observe.url__bulk() == f'https://{_.host}/api/{_.organisation}/_bulk'
