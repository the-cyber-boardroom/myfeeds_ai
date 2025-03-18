from unittest import TestCase

from myfeeds_ai.personas.flows.Flow__My_Feeds__Personas__Create__Persona import \
    Flow__My_Feeds__Personas__Create__Persona
from osbot_utils.utils.Dev import pprint


class test_Flow__My_Feeds__Personas__Create__Persona(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.flow_create_persona = Flow__My_Feeds__Personas__Create__Persona()

    def test_task__1__load_persona_data(self):
        with self.flow_create_persona as _:
            _.task__1__load_persona_data()
            _.task__n__create_output    ()

            pprint(_.output)