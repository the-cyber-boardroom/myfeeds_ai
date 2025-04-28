from unittest                                                                       import TestCase
from myfeeds_ai.providers.cyber_security.owasp.files.Owasp__Git_Hub__Http_Content   import Owasp__Git_Hub__Http_Content
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Category      import Owasp__Top_10__Category


class test_Owasp__Git_Hub__Http_Content(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.owasp_github_content = Owasp__Git_Hub__Http_Content()

    def test_owasp_top_10(self):
        with self.owasp_github_content as _:
            result = _.owasp_top_10__category(Owasp__Top_10__Category.A04_2021__INSECURE_DESIGN)
            assert "A04:2021 – Insecure Design" in result

    def test_owasp_top_10__a04__insecure_design(self):
        with self.owasp_github_content as _:
            result = _.owasp_top_10__a04__insecure_design()
            assert "A04:2021 – Insecure Design" in result
