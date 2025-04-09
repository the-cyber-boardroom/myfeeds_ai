from mgraph_db.providers.time_chain.schemas.Schema__MGraph__Time_Chain__Types import Time_Chain__Source
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Data import Hacker_News__Data
from osbot_utils.type_safe.Type_Safe import Type_Safe


class Hacker_News__Data__Digest(Type_Safe):
    hacker_news_data: Hacker_News__Data

    def digest_articles(self):
        digest_articles  = {}
        current_articles = self.hacker_news_data.current_articles().articles
        for digest_article_id in self.digest_articles_ids():
            digest_articles[digest_article_id] = current_articles.get(digest_article_id)
        return digest_articles

    def digest_articles_ids(self) -> set:
        new_articles = self.hacker_news_data.new_articles()
        if new_articles and new_articles.timeline_diff:
            return new_articles.timeline_diff.added_values.get(Time_Chain__Source, set())
        else:
            return set()