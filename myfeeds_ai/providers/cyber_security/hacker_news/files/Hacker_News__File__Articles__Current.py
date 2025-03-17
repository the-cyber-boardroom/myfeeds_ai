from typing                                                                               import Dict, List
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News           import FILE_ID__ARTICLES__CURRENT
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Articles    import Hacker_News__File__Articles
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article        import Schema__Feed__Article
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Article__Step  import Schema__Feed__Article__Step
from osbot_utils.type_safe.decorators.type_safe                                           import type_safe


class Hacker_News__File__Articles__Current(Hacker_News__File__Articles):
    file_id = FILE_ID__ARTICLES__CURRENT

    @type_safe
    def article(self, article_id):
        return self.articles.articles.get(article_id)

    @type_safe
    def change_article_next_step(self, article_id,  next_step: Schema__Feed__Article__Step):
        article = self.article(article_id)
        if article:
            article.next_step = next_step
            self.save()
            return True
        return False

    def group_by_next_step(self) -> Dict[str, List[Schema__Feed__Article]]:                                        # Group current articles by their status, preserving the typed objects.
        results = {}
        if self.articles and self.articles.articles:
            for article_id, article in self.articles.articles.items():
                status_name = article.next_step.name
                if status_name not in results:
                    results[status_name] = []
                results[status_name].append(article)
        return results

    def next_for_step(self, next_step: Schema__Feed__Article__Step)  -> List[Schema__Feed__Article]:
        return self.group_by_next_step().get(next_step.name, [])

    def next_step__1__save_article(self) -> List[Schema__Feed__Article]:
        return self.next_for_step(Schema__Feed__Article__Step.STEP__1__SAVE__ARTICLE)

    def next_step__2__markdown_for_article(self)  -> List[Schema__Feed__Article]:
        return self.next_for_step(Schema__Feed__Article__Step.STEP__2__MARKDOWN__FOR_ARTICLE)

    def next_step__3__llm_text_to_entities(self)  -> List[Schema__Feed__Article]:
        return self.next_for_step(Schema__Feed__Article__Step.STEP__3__LLM__TEXT_TO_ENTITIES)

    def next_step__4__create_text_entities_graphs(self)-> List[Schema__Feed__Article]:
        return self.next_for_step(Schema__Feed__Article__Step.STEP__4__CREATE__TEXT_ENTITIES_GRAPHS)

    def next_step__5__merge_text_entities_graphs(self)-> List[Schema__Feed__Article]:
        return self.next_for_step(Schema__Feed__Article__Step.STEP__5__MERGE__TEXT_ENTITIES_GRAPHS)

    def next_step__6__merge_day_entities_graphs(self)-> List[Schema__Feed__Article]:
        return self.next_for_step(Schema__Feed__Article__Step.STEP__6__MERGE__DAY_ENTITIES_GRAPHS)

    def next_step__7__merge_day_entities_graphs(self)-> List[Schema__Feed__Article]:
        return self.next_for_step(Schema__Feed__Article__Step.STEP__7__MERGE__FEED_ENTITIES_GRAPHS)

    def next_step__8__create_feed_entities_tree_view(self)-> List[Schema__Feed__Article]:
        return self.next_for_step(Schema__Feed__Article__Step.STEP__8__CREATE__FEED_ENTITIES_TREE_VIEW)