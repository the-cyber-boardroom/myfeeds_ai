from datetime                                                                   import datetime
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


    def generate_personas_links(self):
        personas_data = {'CEO' : '/public-data/personas/latest/exec-ceo__persona-digest.html',
                         'CISO': '/public-data/personas/latest/exec-ciso__persona-digest.html',
                         'CTO' : '/public-data/personas/latest/exec-cto__persona-digest.html'}
        personas_cards = ""
        for persona_name, persona_link in personas_data.items():
            persona_card = f"<li><a href={persona_link} target='_blank'>{persona_name}</a></li>"
            personas_cards += persona_card
        return  personas_cards

    def generate_article_card(self, article_id, article_info, base_url):
        """Generate HTML for a single article card."""
        article_data = article_info.get('article_data', {})
        article_files = article_info.get('article_files', {})

        # Create image HTML if available
        image_html = ""
        if article_data.get('image_url'):
            image_html = f'<img src="{article_data.get("image_url")}" alt="Article illustration" class="article-image">'

        # Format timestamp
        when_data = article_data.get('when', {})
        timestamp = when_data.get('date_time_utc', 'No date available')

        # Generate file labels HTML
        file_labels_html = ""
        for file_name, file_path in article_files.items():
            if file_path and not file_path.endswith('png'):  # Skip PNG files (they will be shown as thumbnails)
                # Extract just the filename without the path
                short_name = file_name.replace('__', '_')
                full_url = f"{base_url.rstrip('/')}/{file_path}"
                file_labels_html += f'<span class="file-label" onclick="openFileInNewWindow(\'{full_url}\')">{short_name}</span>'

        # Generate image thumbnails HTML
        image_previews_html = ""
        png_files = [(name, path) for name, path in article_files.items() if path.endswith('png')]
        if png_files:
            for file_name, png_path in png_files:
                if png_path:
                    # Get a simpler display name
                    display_name = file_name.replace('__', ' ').replace('png', '')
                    full_url = f"{base_url.rstrip('/')}/{png_path}"
                    image_previews_html += f"""                    
                    <div class="image-preview">
                        <img src="{full_url}" alt="{display_name}" class="thumbnail" 
                             onclick="openFileInNewWindow('{full_url}')">
                        <span>{display_name}</span>
                    </div>"""

        # Build the complete article card HTML
        return f"""
        <div class="article-card">
            {image_html}
            <div class="article-content">
                <div class="article-meta">
                    ID: {article_id} | Author: {article_data.get('author', 'Unknown')}
                </div>
                <div class="article-title">{article_data.get('title', 'No title')}</div>
                <div class="article-description">{article_data.get('description', 'No description')}</div>
                <div class="article-timestamp">Published: {timestamp}</div>
                <a href="{article_data.get('link', '#')}" class="article-link" target="_blank">Read Original</a>
                
                <div class="article-files">
                    {f'<div class="section-title">Entities Graphs:</div>' if image_previews_html else ''}
                    <div class="image-previews">
                        {image_previews_html}
                    </div>
                    
                    <div class="section-title">Article Data:</div>
                    <div class="file-labels">
                        {file_labels_html}
                    </div>
                    
                    
                </div>
            </div>
        </div>
        """

    def _generate_section_article(self, article_id, article_info, base_url):
        """Generate HTML for an article in the section view."""
        article_data = article_info.get('article_data', {})
        article_files = article_info.get('article_files', {})

        when_data = article_data.get('when', {})
        timestamp = when_data.get('date_time_utc', 'No date available')

        # Generate file labels
        file_labels_html = ""
        for file_name, file_path in article_files.items():
            if file_path and not file_name.endswith('png'):
                short_name = file_name.replace('__', '_')
                full_url = f"{base_url.rstrip('/')}/{file_path}"
                file_labels_html += f'<span class="source-file-label" onclick="openFileInNewWindow(\'{full_url}\')">{short_name}</span>'

        # Generate image thumbnails
        image_previews_html = ""
        png_files = [(name, path) for name, path in article_files.items() if name.endswith('png')]

        if png_files:
            for file_name, png_path in png_files:
                if png_path:
                    display_name = file_name.replace('__', '_').replace('_png', '')
                    full_url = f"{base_url.rstrip('/')}/{png_path}"
                    image_previews_html += f"""
                    <div class="source-image-preview">
                        <img src="{full_url}" alt="{display_name}" class="source-thumbnail" 
                             onclick="openFileInNewWindow('{full_url}')">
                        <span>{display_name}</span>
                    </div>"""

        return f"""
        <div class="source-article">
            <h3>{article_data.get('title', 'No title')}</h3>
            <div class="source-article-meta">
                <span class="source-id">ID: {article_id}</span>
                <span class="source-author">Author: {article_data.get('author', 'Unknown')}</span>
                <span class="source-date">Published: {timestamp}</span>
            </div>
            <p class="source-description">{article_data.get('description', 'No description')}</p>
            <a href="{article_data.get('link', '#')}" class="source-link" target="_blank">Read Original</a>
            
            <div class="source-article-files">
                <div class="source-file-labels">
                    {file_labels_html}
                </div>
                <div class="source-image-previews">
                    {image_previews_html}
                </div>
            </div>
        </div>
        """

    def digest_articles__html__as_page(self, base_url='/public-data/hacker-news/'):
        """Generate a standalone HTML page to display digest articles."""
        view_data = self.digest_articles__view_data()

        # Generate article cards
        article_cards_html = ""
        for article_id, article_info in view_data.items():
            article_cards_html += self.generate_article_card(article_id, article_info, base_url)
        personas_cards_html = self.generate_personas_links()
        # Fill in the HTML template
        html = self.HTML_TEMPLATE.format(css            = self.CSS            ,
                                         js             = self.JS             ,
                                         personas_cards = personas_cards_html,
                                         article_count  = len(view_data)      ,
                                         last_updated   = datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                         article_cards  = article_cards_html )

        return html

    # Static HTML templates and styles
    HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cybersecurity News Digest - Source Articles</title>
    <style>
    {css}
    </style>
</head>
<body>
    <h1>Cybersecurity News Digest - Source Articles</h1>
    
    <div class="header-meta">
        <p>This page displays the source articles used to generate personalized cybersecurity
         digests. Each article card contains the original content before it was processed and 
         tailored for the following user personas.</p>
         {personas_cards}
        <p>Total Articles: {article_count}</p>
        <p>Created on: {last_updated}</p>        
    </div>    
    <div class="articles-container">
        {article_cards}
    </div>

    <script>
    {js}
    </script>
</body>
</html>
    """

    CSS = """
body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}
h1 {
    color: #2c3e50;
    border-bottom: 2px solid #eee;
    padding-bottom: 10px;
}
h2 {
    color: #2c3e50;
    margin-top: 30px;
}
.header-meta {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 30px;
}
.articles-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 20px;
}
.article-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
    background-color: white;
}
.article-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}
.article-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-bottom: 1px solid #eee;
}
.article-content {
    padding: 15px;
}
.article-meta {
    font-size: 12px;
    color: #666;
    margin-bottom: 10px;
}
.article-title {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
}
.article-description {
    font-size: 14px;
    color: #555;
    margin-bottom: 15px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.article-timestamp {
    font-style: italic;
    color: #777;
    margin-bottom: 15px;
}
.article-link {
    display: inline-block;
    padding: 8px 12px;
    background-color: #3498db;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-size: 14px;
    margin-right: 10px;
}
.article-link:hover {
    background-color: #2980b9;
}
.article-files {
    margin-top: 15px;
    background-color: #f9f9f9;
    padding: 15px;
    border-radius: 4px;
    border: 1px solid #eee;
}
.file-labels {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 15px;
}
.file-label {
    display: inline-block;
    padding: 6px 10px;
    background-color: #e9ecef;
    color: #495057;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-size: 12px;
    cursor: pointer;
    transition: background-color 0.2s;
}
.file-label:hover {
    background-color: #dee2e6;
}
.image-previews {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin-top: 15px;
}
.image-preview {
    text-align: center;
    width: 120px;
}
.thumbnail {
    width: 100%;
    height: 80px;
    object-fit: cover;
    border: 1px solid #ddd;
    border-radius: 4px;
    transition: transform 0.2s;
    cursor: pointer;
}
.thumbnail:hover {
    transform: scale(1.05);
}
.image-preview span {
    display: block;
    font-size: 11px;
    margin-top: 5px;
    color: #555;
}
.section-title {
    font-size: 14px;
    font-weight: bold;
    margin-bottom: 10px;
    color: #2c3e50;
}

/* Source section styles for embedded view */
.source-articles-section {
    margin-top: 40px;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 8px;
    border-left: 4px solid #3498db;
}
.source-articles-info {
    margin-bottom: 20px;
}
.source-articles-container {
    display: flex;
    flex-direction: column;
    gap: 15px;
}
.source-article {
    padding: 15px;
    background-color: white;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.source-article h3 {
    margin-top: 0;
    color: #2c3e50;
}
.source-article-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    margin-bottom: 10px;
    font-size: 12px;
    color: #666;
}
.source-description {
    font-size: 14px;
    margin-bottom: 10px;
}
.source-link {
    display: inline-block;
    padding: 6px 10px;
    background-color: #3498db;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-size: 12px;
    margin-bottom: 10px;
}
.source-link:hover {
    background-color: #2980b9;
}
.source-article-files {
    margin-top: 10px;
}
.source-file-labels {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 10px;
}
.source-file-label {
    display: inline-block;
    padding: 4px 8px;
    background-color: #e9ecef;
    color: #495057;
    border: 1px solid #ced4da;
    border-radius: 4px;
    font-size: 11px;
    cursor: pointer;
}
.source-file-label:hover {
    background-color: #dee2e6;
}
.source-image-previews {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 10px;
}
.source-image-preview {
    text-align: center;
    width: 100px;
}
.source-thumbnail {
    width: 100%;
    height: 70px;
    object-fit: cover;
    border: 1px solid #ddd;
    border-radius: 4px;
    cursor: pointer;
}
.source-thumbnail:hover {
    transform: scale(1.05);
}
.source-image-preview span {
    display: block;
    font-size: 10px;
    margin-top: 4px;
    color: #555;
}
    """

    JS = """
function openFileInNewWindow(url) {
    window.open(url, '_blank');
}
    """


    def digest_articles__html__as_section(self, base_url='/public-data/hacker-news/'):
        """Generate an HTML section for digest articles to be included in persona HTML."""
        view_data = self.digest_articles__view_data()
        article_items_html = ""

        # Generate article list HTML for each article
        for article_id, article_info in view_data.items():
            article_items_html += self._generate_section_article(article_id, article_info, base_url)

        # Generate the section HTML
        html = f"""
        <div class="source-articles-section">
            <h2>Source Articles</h2>
            <div class="source-articles-info">
                <p>The personalized digest above was generated from the following {len(view_data)} source articles. These represent the raw news content before it was analyzed and tailored to the specific persona.</p>
            </div>
            <div class="source-articles-container">
                {article_items_html}
            </div>
            <script>
            {self.JS}
            </script>
        </div>
        """

        return html