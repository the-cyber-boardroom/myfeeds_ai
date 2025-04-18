from myfeeds_ai.personas.actions.My_Feeds__Persona import My_Feeds__Persona
from osbot_utils.type_safe.Type_Safe import Type_Safe


class My_Feeds__Persona__Digest__Image(Type_Safe):
    persona : My_Feeds__Persona = None

    def articles(self):
        return self.persona.persona_digest().digest_articles.articles

    def articles__images__urls(self):
        images__urls = []
        for article in self.articles():
            images__urls.append(article.article_image_link_url)
        return images__urls

