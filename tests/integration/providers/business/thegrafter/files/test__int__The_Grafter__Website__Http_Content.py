from pprint import pprint
from unittest import TestCase

import pytest

from myfeeds_ai.providers.business.thegrafter.files.The_Grafter__Website__Http_Content import \
    The_Grafter__Website__Http_Content



class test__int__The_Grafter__Website__Http_Content(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.the_grafter_website = The_Grafter__Website__Http_Content()

    @pytest.mark.skip(reason="add after finished adding http cache support to My_Feeds__Http_Content")
    def test_http_data(self):
        with self.the_grafter_website as _:
            http = _.http_data('results')
            pprint(http, width=500)


