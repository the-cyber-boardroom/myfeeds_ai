import sys
from pprint                                                                     import pprint
from myfeeds_ai.personas.schemas.Schema__Persona__Types                         import Schema__Persona__Types
from myfeeds_ai.pipelines.flows.Pipeline__Hacker_News__Create_Persona_Digest    import Pipeline__Hacker_News__Create_Persona_Digest


#myfeeds_tests__setup_local_stack()

DEFAULT_PERSONA = 'EXEC__CISO'
#DEFAULT_PERSONA = 'TEAM__APP_SEC'           # was failing here

if __name__ == '__main__':

    raw_arg   = sys.argv[1] if len(sys.argv) > 1 else ''
    input_arg = raw_arg.strip() or DEFAULT_PERSONA

    try:
        persona_type = Schema__Persona__Types[input_arg]
    except KeyError:
        raise ValueError(f"Invalid persona type: {input_arg}. Must be one of: {list(Schema__Persona__Types.__members__.keys())}")

    #persona_type = Schema__Persona__Types.EXEC__CISO                                     # todo: this needs to be passed as a param
    with Pipeline__Hacker_News__Create_Persona_Digest(persona_type=persona_type) as _:
        flow         = _.create_persona_digest()

        flow.flow_config.log_to_console = True
        flow.config_logger()

        flow.execute_flow()

        pprint(_.output, width=200)