from myfeeds_ai.personas.llms.Schema__Persona__Digest_Articles  import Schema__Persona__Digest_Articles
from osbot_utils.type_safe.Type_Safe                            import Type_Safe


class Schema__Persona__Digest(Type_Safe):
    digest_articles : Schema__Persona__Digest_Articles
    digest_html     : str
    digest_markdown : str
    path_now        : str