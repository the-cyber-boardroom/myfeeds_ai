from unittest                                                                           import TestCase
from myfeeds_ai.data_feeds.models.Model__Data_Feeds__Prompt                  import Model__Data_Feeds__Prompt
from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Prompts   import OSS__Prompts, PROMPT__OSS__CURRENT_SESSIONS
from tests.integration.data_feeds__objs_for_tests                                       import myfeeds_tests__setup_local_stack


class test_OSS__Prompt_Creator(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.prompt_creator = OSS__Prompts()

    def test_current_event(self):
        with self.prompt_creator as _:
            event_prompt = _.current_event()
            prompt_text  = event_prompt.prompt_text
            event        = _.oss_files.current_event()
            assert type(event_prompt) is Model__Data_Feeds__Prompt
            assert prompt_text.startswith(PROMPT__OSS__CURRENT_SESSIONS[0:70]) is True
            for session in event.sessions.values():
                assert session.title in prompt_text