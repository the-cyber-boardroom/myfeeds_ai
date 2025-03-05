from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator import S3_Key__File_Extension
from myfeeds_ai.providers.cyber_security.hacker_news.config.Config__Hacker_News         import FILE_ID__FEED_ARTICLE, FILE_ID__ARTICLE__MARKDOWN
from myfeeds_ai.providers.cyber_security.hacker_news.files.Hacker_News__File__Article   import Hacker_News__File__Article
from myfeeds_ai.providers.cyber_security.hacker_news.models.Model__Hacker_News__Article import Model__Hacker_News__Article
from myfeeds_ai.utils.My_Feeds__Utils                                                   import path_to__date_time
from osbot_utils.decorators.methods.cache_on_self                                       import cache_on_self
from osbot_utils.helpers.Obj_Id                                                         import Obj_Id
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.utils.Dev                                                              import pprint
from urllib.parse                                                                       import urlparse


class Hacker_News__Article(Type_Safe):
    article_id         : Obj_Id
    path__folder__data : str

    def __init__(self, article_id: Obj_Id, **kwargs) -> None:
        self.article_id = article_id
        super().__init__(**kwargs)

    def now(self):
        if self.path__folder__data:
            return path_to__date_time(self.path__folder__data)

    @cache_on_self
    def file_article(self):
        return Hacker_News__File__Article(article_id=self.article_id, file_id=FILE_ID__FEED_ARTICLE     , now=self.now())

    @cache_on_self
    def file_markdown(self):
        article_kwargs = dict(article_id   = self.article_id                ,
                              content_type = "text/markdown"                ,
                              extension    = S3_Key__File_Extension.MARKDOWN,
                              file_id      = FILE_ID__ARTICLE__MARKDOWN     ,
                              now          = self.now()                     )
        return Hacker_News__File__Article(**article_kwargs)

    def article_markdown__create(self):
        feed_article_data = self.file_article().contents()

        if feed_article_data:                                                                    # Extract data with defaults for missing fields
            title          = feed_article_data.get('title'       , 'No Title'                 ) # Article title
            author         = feed_article_data.get('author'      , 'Unknown Author'           ) # Author information
            description    = feed_article_data.get('description' , 'No description available.') # Article content
            image_url      = feed_article_data.get('image_url'   , ''                         ) # Image URL
            source_link    = feed_article_data.get('link'        , 'No source link available' ) # Article source link
            when_utc       = feed_article_data.get('when', {}    ).get('date_time_utc'        ) # When it was published

            # Create markdown content with proper formatting

            format_kwargs = dict( title         = title          ,
                                  image_url      = image_url      ,
                                  description    = description    ,
                                  author         = author         ,
                                  source_link    = source_link    ,
                                  article_id     = self.article_id,
                                  when_utc       = when_utc       )
            markdown_content       = MARKDOWN__ARTICLE__CONTENT.format(**format_kwargs)
            path_markdown_file = self.file_markdown().save_data(markdown_content)
            return path_markdown_file

    def article_data__save(self, article_data: Model__Hacker_News__Article):
        file_article = self.file_article()
        data         = article_data.json()
        article_path = file_article.save_data(data)
        return article_path


MARKDOWN__ARTICLE__CONTENT = """## {title}
![Article Image]({image_url})

{description}

```
Author    : {author}
Source    : {source_link}
When      : {when_utc}
Article ID: {article_id}
```
"""