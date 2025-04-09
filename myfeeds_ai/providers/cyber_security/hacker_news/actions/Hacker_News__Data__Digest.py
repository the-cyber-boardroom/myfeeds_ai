from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types   import Time_Chain__Source
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data  import Hacker_News__Data
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe


class Hacker_News__Data__Digest(Type_Safe):
    hacker_news_data: Hacker_News__Data

    def digest_articles(self):
        digest_articles  = {}
        current_articles = self.hacker_news_data.current_articles().articles
        for digest_article_id in self.digest_articles__ids():
            digest_articles[digest_article_id] = current_articles.get(digest_article_id)
        return digest_articles

    def digest_articles__ids(self) -> set:
        new_articles = self.hacker_news_data.new_articles()
        if new_articles and new_articles.timeline_diff:
            return new_articles.timeline_diff.added_values.get(Time_Chain__Source, set())
        else:
            return set()

    def digest_articles__view_data(self):
        view_data = {}
        for article_id, article in self.digest_articles().items():
            with article as _:
                article_data   = self.hacker_news_data.storage.path__load_data(_.path__file__feed_article)
                article_files = dict(data__article           = _.path__file__feed_article              ,
                                     entities__title         = _.path__file__text_entities__title     ,
                                     markdown__article       = _.path__file__markdown                 ,
                                     mgraph__entities        =_.path__file__text_entities__mgraph,
                                     mgraph__entities__title = _.path__file__text_entities__title     ,
                                     png__entities           =_.path__file__text_entities__png,
                                     png__entities__title    = _.path__file__text_entities__title__png)


            view_data[article_id] = dict(article_data  = article_data    ,
                                         article_files = article_files   )
                                         #raw_data     = article.json()  )


        return view_data

