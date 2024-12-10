from unittest                                                                               import TestCase
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.OSS__Http_Content  import OSS__Http_Content
from cbr_custom_data_feeds.providers.cyber_security.open_security_summit.OSS__Parser        import OSS__Parser
from tests.integration.data_feeds__objs_for_tests                                           import cbr_website__assert_local_stack

class test_OSS__Parser(TestCase):

    @classmethod
    def setUpClass(cls):
        cbr_website__assert_local_stack()
        cls.oss_parser  = OSS__Parser()
        cls.oss_content = OSS__Http_Content()

    def test_parse_raw_data(self):
        with self.oss_parser as _:
            raw_content = self.oss_content.raw_content()
            content          = _.parse_raw_content(raw_content.raw_data)
            participants     = content.get('participants'    )
            working_sessions = content.get('working_sessions')
            assert len(participants    ) > 218
            assert len(working_sessions) > 340
