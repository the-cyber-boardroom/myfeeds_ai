import re
from typing                                                                                         import List
from osbot_utils.type_safe.Type_Safe                                                                 import Type_Safe
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article  import Model__Hacker_News__Article
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Feed     import Model__Hacker_News__Feed

# PROMPT_ANALYSIS = """Based on the following {feed_title} cybersecurity news feed (last updated: {last_build}), provide an analysis:
#
# Current Feed Articles:
# {articles}
#
# Please provide:
# 1. A brief overview of the current cybersecurity landscape based on these articles
# 2. Key trends or patterns you observe
# 3. Notable threats or vulnerabilities mentioned
# 4. Potential implications for organizations and security professionals"""

PROMPT_SCHEMA__HACKER_NEWS = """The following data is from {feed_title} feed collected at {when}. 
There are {article_count} articles using the Hacker News schema with fields: title, description, link, data, author, summary

Current Articles:
{articles}"""

# PROMPT_EXECUTIVE = """Based on the following cybersecurity news headlines, provide a brief executive summary:
#
# Headlines:
# {articles}
#
# Please provide:
# 1. A concise (2-3 sentences) overview of the current threat landscape
# 2. Key business implications
# 3. High-level recommendations for executive action"""

class Hacker_News__Prompt_Creator(Type_Safe):

    # def create_prompt_analysis(self, feed: Model__Hacker_News__Feed, size: int = 5) -> str:       # Create an analysis-focused prompt from feed data
    #     articles = feed.articles[:size]
    #     formatted_articles = self.format_articles_full(articles)
    #
    #     return PROMPT_ANALYSIS.format(feed_title=feed.title,
    #                                 last_build=feed.last_build_date,
    #                                 articles=formatted_articles)

    def create_prompt_schema(self, feed: Model__Hacker_News__Feed, size: int = 5) -> str:         # Create a schema-focused prompt from feed data
        articles = feed.articles[:size]
        formatted_articles = self.format_articles_full(articles)

        return PROMPT_SCHEMA__HACKER_NEWS.format(feed_title=feed.title,
                                                 when=feed.when.date_time_utc,
                                                 article_count=len(articles),
                                                 articles=formatted_articles)

    # def create_prompt_executive(self, feed: Model__Hacker_News__Feed, size: int = 3) -> str:      # Create an executive-focused prompt from feed data
    #     articles = feed.articles[:size]
    #     formatted_articles = ""
    #
    #     for i, article in enumerate(articles, 1):
    #         title = self.clean_text(article.title)
    #         formatted_articles += f"{i}. {title}\n"
    #
    #     return PROMPT_EXECUTIVE.format(articles=formatted_articles)

    def format_articles_full(self, articles: List[Model__Hacker_News__Article]) -> str:           # Format full article details for prompts
        formatted_articles = ""
        for i, article in enumerate(articles, 1):
            formatted_articles += f"""
Article {i}:
Title: {self.clean_text(article.title)}
Date: {article.when.date_time_utc}
Author: {self.clean_author(article.author)}
Summary: {self.clean_text(article.description)}
"""
        return formatted_articles

    def clean_text(self, text: str) -> str:                                                      # Clean text by removing HTML tags and normalizing whitespace
        clean = re.sub(r'<[^>]+>', ''   , text)                                                  # Remove HTML tags
        clean = clean.replace('&nbsp;'  , ' ')                                                   # Remove common RSS artifacts
        clean = clean.replace('&amp;'   , '&')
        clean = clean.replace('&quot;'  , '"')
        clean = ' '.join(clean.split())                                                          # Normalize whitespace after entity replacement
        return clean.strip()

    def clean_author(self, author: str) -> str:                                                 # Clean author string by removing email and standardizing format
        author = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+\s*\(', '(', author)                            # Remove any email before parentheses
        author = re.sub(r'\s*\((.*?)\)', r'\1', author)                                         # Extract name from parentheses
        return author.strip()                                                                   # todo: review this since using regex doesn't feel right