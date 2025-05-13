from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.type_safe.Type_Safe              import Type_Safe
from osbot_utils.utils.Http                       import GET


class Html_Graph__Site__docs_diniscruz_ai(Type_Safe):

    @cache_on_self
    def html__homepage(self):
        return GET("https://docs.diniscruz.ai")                 # change to use version for S3 (which is cached)