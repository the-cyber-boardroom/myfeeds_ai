from myfeeds_ai.pipelines.flows.Pipeline__Hacker_News__Create_Persona_Digest    import Pipeline__Hacker_News__Create_Persona_Digest

if __name__ == '__main__':
    #myfeeds_tests__setup_local_stack()
    with Pipeline__Hacker_News__Create_Persona_Digest() as _:
        flow = _.create_persona_digest()
        flow.flow_config.log_to_console = True
        flow.config_logger()

        flow.execute_flow()
        #pprint(_.output)