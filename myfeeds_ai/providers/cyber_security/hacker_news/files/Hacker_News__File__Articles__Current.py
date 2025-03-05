from typing                                                                               import Dict, List
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News           import FILE_ID__ARTICLES__CURRENT
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles    import Hacker_News__File__Articles
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article        import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step  import Schema__Feed__Article__Step

class Hacker_News__File__Articles__Current(Hacker_News__File__Articles):
    file_id               = FILE_ID__ARTICLES__CURRENT

    def group_by_next_step(self) -> Dict[str, List[Schema__Feed__Article]]:                                        # Group current articles by their status, preserving the typed objects.
        results = {}
        if self.articles and self.articles.articles:
            for article_id, article in self.articles.articles.items():
                status_name = article.next_step.name
                if status_name not in results:
                    results[status_name] = []
                results[status_name].append(article)
        return results

    def next_step__1__save_article(self) -> List[Schema__Feed__Article]:
        next_step = Schema__Feed__Article__Step.STEP__1__SAVE_ARTICLE.name
        return self.group_by_next_step().get(next_step, [])

