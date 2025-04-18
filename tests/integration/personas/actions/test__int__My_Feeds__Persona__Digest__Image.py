from unittest import TestCase

from myfeeds_ai.personas.actions.My_Feeds__Persona import My_Feeds__Persona
from myfeeds_ai.personas.actions.My_Feeds__Persona__Digest__Image import My_Feeds__Persona__Digest__Image
from myfeeds_ai.personas.schemas.Schema__Persona__Types import Schema__Persona__Types
from osbot_utils.utils.Dev import pprint
from tests.integration.data_feeds__objs_for_tests import myfeeds_tests__setup_local_stack


class test__int__My_Feeds__Persona__Digest__Image(TestCase):

    @classmethod
    def setUpClass(cls):
        myfeeds_tests__setup_local_stack()
        cls.persona_type = Schema__Persona__Types.EXEC__CISO
        cls.persona              = My_Feeds__Persona(persona_type=cls.persona_type)
        cls.persona_digest_image = My_Feeds__Persona__Digest__Image(persona=cls.persona)

    def test_images__urls(self):
        with self.persona_digest_image as _:
            images_urls = _.articles__images__urls()
            assert len(images_urls) > 0
            for image_url in images_urls:
                assert image_url.startswith('https://')