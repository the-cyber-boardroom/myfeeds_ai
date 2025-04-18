# todo: see if we need this, since the My_Feeds__Persona already has a reference to the persona-digest.json
# from unittest                                               import TestCase
# from myfeeds_ai.personas.actions.My_Feeds__Persona__Digest  import My_Feeds__Persona__Digest
# from myfeeds_ai.personas.schemas.Schema__Persona__Types     import Schema__Persona__Types
# from tests.integration.data_feeds__objs_for_tests           import myfeeds_tests__setup_local_stack
#
#
# class test__int__My_Feeds__Persona__Digest(TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         myfeeds_tests__setup_local_stack()
#         cls.persona_type   = Schema__Persona__Types.EXEC__CISO
#         cls.persona_digest = My_Feeds__Persona__Digest()
#
#     def test_persona_digest(self):
#         with self.persona_digest as _:
#             persona_digest = _.persona_digest(persona_type=self.persona_type)
#
#             from osbot_utils.utils.Dev import pprint
#             pprint(persona_digest)
#
