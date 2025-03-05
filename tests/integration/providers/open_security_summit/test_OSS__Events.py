from unittest                                                             import TestCase
from myfeeds_ai.providers.cyber_security.open_security_summit.OSS__Events import OSS__Events,OSS_EVENTS__CURRENT__YEAR, OSS_EVENTS__CURRENT__MONTH
from tests.integration.data_feeds__objs_for_tests                         import cbr_website__assert_local_stack

class test_OSS__Events(TestCase):

    @classmethod
    def setUpClass(cls):
        import pytest
        pytest.skip("test needs updating")
        cbr_website__assert_local_stack()
        cls.oss_events = OSS__Events()

    def test_current_event(self):
        with self.oss_events  as _:
            summit = _.current_event()
            assert summit.year  == OSS_EVENTS__CURRENT__YEAR
            assert summit.month == OSS_EVENTS__CURRENT__MONTH
            assert 20 > len(summit.organizers) > 5
            assert 20 > len(summit.sessions  ) > 5
