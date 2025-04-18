from unittest                                                       import TestCase
from PIL.Image                                                      import Image
from PIL.ImageFont                                                  import FreeTypeFont
from myfeeds_ai.personas.actions.My_Feeds__Persona                  import My_Feeds__Persona
from myfeeds_ai.personas.actions.My_Feeds__Persona__Digest__Image   import My_Feeds__Persona__Digest__Image
from myfeeds_ai.personas.schemas.Schema__Persona__Types             import Schema__Persona__Types
from tests.integration.data_feeds__objs_for_tests                   import myfeeds_tests__setup_local_stack


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
            for image_url in images_urls:
                assert image_url.startswith('https://')

    def test_articles__images(self):
        with self.persona_digest_image as _:
            images = _.articles__images()
            for image in images:
                assert type(image) is Image

    def test_font(self):
        print()
        with self.persona_digest_image as _:
            font = _.font()
            assert type(font) is FreeTypeFont

    def test__generate_digest_cover(self):
        with self.persona_digest_image as _:
            title       = f"CISO CYBERSECURITY DIGEST"
            sub_title   = "March 19 – 26, 2025"
            image_bytes = _.generate_digest_cover(title=title, sub_title=sub_title)
            assert type(image_bytes) is bytes
            assert len(image_bytes) > 10000
