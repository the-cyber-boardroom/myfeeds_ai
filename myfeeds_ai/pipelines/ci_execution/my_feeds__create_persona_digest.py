from myfeeds_ai.personas.schemas.Schema__Persona__Types                         import Schema__Persona__Types
from myfeeds_ai.pipelines.flows.Pipeline__Hacker_News__Create_Persona_Digest    import Pipeline__Hacker_News__Create_Persona_Digest
from osbot_utils.utils.Dev                                                      import pprint

if __name__ == '__main__':
    #myfeeds_tests__setup_local_stack()
    with Pipeline__Hacker_News__Create_Persona_Digest() as _:
        persona_type = Schema__Persona__Types.EXEC__CEO                         # todo: this needs to be passed as a param
        flow         = _.create_persona_digest(persona_type=persona_type)

        flow.flow_config.log_to_console = True
        flow.config_logger()

        flow.execute_flow()

        pprint(_.output)