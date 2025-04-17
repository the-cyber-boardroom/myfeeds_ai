from myfeeds_ai.personas.schemas.Schema__Persona__Types                         import Schema__Persona__Types
from myfeeds_ai.pipelines.flows.Pipeline__Hacker_News__Create_Persona_Digest    import Pipeline__Hacker_News__Create_Persona_Digest
from osbot_utils.utils.Dev                                                      import pprint

#myfeeds_tests__setup_local_stack()

if __name__ == '__main__':

    persona_type = Schema__Persona__Types.EXEC__CISO                                     # todo: this needs to be passed as a param
    with Pipeline__Hacker_News__Create_Persona_Digest(persona_type=persona_type) as _:
        flow         = _.create_persona_digest()

        flow.flow_config.log_to_console = True
        flow.config_logger()

        flow.execute_flow()

        pprint(_.output)