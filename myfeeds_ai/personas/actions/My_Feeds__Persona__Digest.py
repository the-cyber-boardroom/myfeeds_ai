from myfeeds_ai.personas.actions.My_Feeds__Persona__Files    import My_Feeds__Persona__Files
from myfeeds_ai.personas.schemas.Schema__Persona__Types      import Schema__Persona__Types
from osbot_utils.type_safe.Type_Safe                         import Type_Safe


class My_Feeds__Persona__Digest(Type_Safe):
    persona_files : My_Feeds__Persona__Files

    def persona_digest(self, persona_type: Schema__Persona__Types):
        persona = self.persona_files.file__persona(persona_type).data()

        persona_files = dict(persona=persona.path__persona)
        persona_digest = dict(persona_type = persona_type.value,
                              description  = persona.description,
                              persona_files = persona_files)
        return persona_digest
        #return persona.json()
