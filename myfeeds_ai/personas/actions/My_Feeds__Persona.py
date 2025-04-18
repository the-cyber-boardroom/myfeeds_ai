from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                        import S3_Key__File__Content_Type
from myfeeds_ai.personas.actions.My_Feeds__Persona__Files                       import My_Feeds__Persona__Files
from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage__Persona           import My_Feeds__Personas__Storage__Persona
from myfeeds_ai.personas.files.My_Feeds__Personas__File                         import My_Feeds__Personas__File
from myfeeds_ai.personas.files.My_Feeds__Personas__File__Now                    import My_Feeds__Personas__File__Now
from myfeeds_ai.personas.llms.Schema__Persona__Digest                           import Schema__Persona__Digest
from myfeeds_ai.personas.schemas.Default_Data__My_Feeds__Personas               import Default_Data__My_Feeds__Personas
from myfeeds_ai.personas.schemas.Schema__Persona                                import Schema__Persona
from myfeeds_ai.personas.schemas.Schema__Persona__Articles__Connected_Entities  import Schema__Persona__Articles__Connected_Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Text__Entities                import Schema__Persona__Text__Entities
from myfeeds_ai.personas.schemas.Schema__Persona__Types                         import Schema__Persona__Types
from myfeeds_ai.utils.shared_schemas.Str__Description                           import Str__Description
from osbot_utils.decorators.methods.cache_on_self                               import cache_on_self
from osbot_utils.helpers.safe_str.Safe_Str__Hash                                import safe_str_hash
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe


class My_Feeds__Persona(Type_Safe):
    persona_files: My_Feeds__Persona__Files
    persona_type : Schema__Persona__Types

    def create(self):
        with self.data() as _:
            _.persona_type = self.persona_type
            self.description__reset_to_default_value()
        return self

    @cache_on_self                                                                      # todo: research possible race conditions caused by this (for example when the save() method updates the path__now (which in one test was not in sync)
    def data(self) -> Schema__Persona:
        return self.file__persona().data()

    def data__reset_paths(self):
        with self.data() as _:
            _.path__persona__latest                = self.file__persona().path_latest()
            _.path__persona__entities              = ''                                 # we need to reset these paths, since it's content is no longer value (they were created for the previous version of the description)
            _.path__persona__entities__png         = ''
            _.path__persona__entities__tree_values = ''

    def delete(self):
        self.file__persona                             ().delete__latest()              # delete the persona files that are stored in the latest folder
        self.file__persona_digest                      ().delete__latest()
        self.file__persona_digest_html                 ().delete__latest()
        self.file__persona_articles__connected_entities().delete__now()                 # and files that are only stored in the now folder
        self.file__persona_entities                    ().delete__now()
        self.file__persona_entities__png               ().delete__now()
        self.file__persona_entities__tree_values       ().delete__now()

        return self.not_exists()

    def description(self) -> str:
        return self.data().description

    def description__change_value_and_reset_paths(self, new_description: str, force_reset: bool = False):
        if new_description:
            new_description = Str__Description(new_description)
            with self.data() as _:
                new_description_hash = safe_str_hash(new_description)
                if force_reset or new_description_hash != _.description__hash:
                    _.description        = new_description
                    _.description__hash  = new_description_hash
                    self.data__reset_paths()
                    self.save()
                    return True

        return False

    def description__reset_to_default_value(self, force_reset: bool = False):
        persona_default_description = Default_Data__My_Feeds__Personas.get(self.persona_type, {}).get('description')
        return self.description__change_value_and_reset_paths(new_description=persona_default_description, force_reset=force_reset)


    def description_changed(self) -> bool:
        with self.data() as _:
            if _.description:
                return _.description__hash != safe_str_hash(_.description)

    def exists(self):
        return self.file__persona().exists__latest()

    @cache_on_self
    def file__persona(self) -> My_Feeds__Personas__File:
        return self.persona_files.file__persona(persona_type=self.persona_type)

    @cache_on_self
    def file__persona_digest(self) -> My_Feeds__Personas__File:
        return self.persona_files.file__persona_digest(persona_type=self.persona_type)

    @cache_on_self
    def file__persona_digest_html(self) -> My_Feeds__Personas__File:
        return self.persona_files.file__persona_digest_html(persona_type=self.persona_type)

    @cache_on_self
    def file__persona_articles__connected_entities(self) -> My_Feeds__Personas__File__Now:
        return self.persona_files.file__persona_articles__connected_entities(persona_type=self.persona_type)

    @cache_on_self
    def file__persona_entities(self) -> My_Feeds__Personas__File__Now:
        return self.persona_files.file__persona_entities(persona_type=self.persona_type)

    @cache_on_self
    def file__persona_entities__png(self) -> My_Feeds__Personas__File__Now:
        return self.persona_files.file__persona_entities__png(persona_type=self.persona_type)

    @cache_on_self
    def file__persona_entities__tree_values(self) -> My_Feeds__Personas__File__Now:
        return self.persona_files.file__persona_entities__tree_values(persona_type=self.persona_type)

    def file_contents(self, path, content_type:S3_Key__File__Content_Type=None):
        if path:
            return self.storage().path__load_data(s3_path = path, content_type=content_type)

    def not_exists(self):
        return self.exists() is False

    def persona(self) -> Schema__Persona:
        path      = self.data().path__now
        json_data =  self.file_contents(path)
        return Schema__Persona.from_json(json_data)

    def persona__articles__connected_entities(self) -> Schema__Persona__Articles__Connected_Entities:
        path      = self.data().path__persona__articles__connected_entities
        json_data = self.file_contents(path)
        return Schema__Persona__Articles__Connected_Entities.from_json(json_data)

    def persona_digest(self) -> Schema__Persona__Digest:
        path      = self.data().path__persona__digest
        json_data = self.file_contents(path)
        return Schema__Persona__Digest.from_json(json_data)

    def persona_digest_html(self) -> str:
        path      = self.data().path__persona__digest__html
        html_code = self.file_contents(path, content_type=S3_Key__File__Content_Type.HTML)
        return html_code

    def persona__entities(self) -> Schema__Persona__Text__Entities:
        path      = self.data().path__persona__entities
        json_data = self.file_contents(path)
        return Schema__Persona__Text__Entities.from_json(json_data)

    def persona__entities__png(self) -> bytes:
        path      = self.data().path__persona__entities__png
        png_bytes = self.file_contents(path, S3_Key__File__Content_Type.PNG)
        return png_bytes

    def persona__entities__tree_values(self) -> str:
        path        = self.data().path__persona__entities__tree_values
        tree_values = self.file_contents(path, S3_Key__File__Content_Type.TXT)
        if tree_values:
            return tree_values.decode()

    def save(self):
        self.file__persona().save()
        return self

    @cache_on_self
    def storage(self):
        return My_Feeds__Personas__Storage__Persona(persona_type=self.persona_type)

    def update(self):
        return self.file__persona().update()