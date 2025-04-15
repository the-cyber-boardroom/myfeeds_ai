from myfeeds_ai.personas.actions.My_Feeds__Personas__Storage import My_Feeds__Personas__Storage
from osbot_utils.type_safe.Type_Safe                         import Type_Safe
from osbot_utils.type_safe.decorators.type_safe              import type_safe

# todo: refactor out these methods since they were from a previous version of this class
class My_Feeds__Personas(Type_Safe):
    storage : My_Feeds__Personas__Storage

    @type_safe
    def files_in__now(self, include_sub_folders:bool = True):
        return self.storage.files_in__now(include_sub_folders=include_sub_folders)

    @type_safe
    def files_in__latest(self):
        return self.storage.files_in__latest()


