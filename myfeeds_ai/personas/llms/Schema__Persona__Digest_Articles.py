from typing                           import List
from osbot_utils.type_safe.Type_Safe  import Type_Safe
from osbot_utils.utils.Misc           import date_time_now

class Schema__Persona__Digest_Summary_Section(Type_Safe):
    """Represents a section in the executive summary with a header and content."""
    section_header : str                                            # The title of this section (e.g., "COMPLIANCE & REGULATIONS")
    section_text   : str                                            # The paragraph content for this section

class Schema__Persona__Digest_Summary(Type_Safe):
    """Structured representation of the executive summary."""
    introduction   : str                                             # Opening paragraph providing overview
    sections       : List[Schema__Persona__Digest_Summary_Section]   # Domain-specific sections with headers and content


class Schema__Persona__Digest_Article(Type_Safe):
    """Represents a single article in the personalized digest."""
    article_id              : str          # ID of the original article
    article_source_url      : str          # Link to who published the article
    article_author          : str          # Who created the article
    article_when            : str          # When the article was published
    article_image_link_url  : str          # Link to the article image
    headline                : str          # Personalized headline
    summary                 : str          # Concise summary of key points
    relevance_analysis      : str          # Why this matters to the persona
    action_recommendations  : str          # Role-specific guidance based on the news
    priority_level          : str          # Critical, high, medium, low


class Schema__Persona__Digest_Articles(Type_Safe):
    """Complete personalized digest for a specific persona."""
    persona_type           : str                                        # Type of persona (from Schema__Persona__Types)
    executive_summary      : Schema__Persona__Digest_Summary            # Structured summary with intro and sections
    articles               : List[Schema__Persona__Digest_Article]      # Processed articles
    strategic_implications : str                                        # Broader context and implications for this role

    # todo: refactor these two methods (markdown and html generation) into a separate class
    def get_markdown(self) -> str:
        """Convert the digest to a markdown format."""
        md = f"# Personalized Cybersecurity Digest for {self.persona_type}\n\n"
        md += f"## Executive Summary\n\n{self.executive_summary}\n\n"

        for article in self.articles:
            md += f"## {article.headline}\n\n"

            # Add article metadata
            md += f"**Source**: [{article.article_source_url}]({article.article_source_url})  \n"
            md += f"**Author**: {article.article_author}  \n"
            md += f"**Published**: {article.article_when}  \n\n"

            # Add image if available
            if article.article_image_link_url:
                md += f"![Article Image]({article.article_image_link_url})\n\n"

            md += f"{article.summary}\n\n"
            md += f"**Why This Matters**: {article.relevance_analysis}\n\n"
            md += f"**Recommended Actions**: {article.action_recommendations}\n\n"
            md += f"*Priority: {article.priority_level}*\n\n"
            md += "---\n\n"

        md += f"## Strategic Implications\n\n{self.strategic_implications}\n\n"

        return md

    def get_html(self, cache_id=None) -> str:
        """Convert the digest to HTML format."""
        priority_colors = {
            "critical": "#d9534f",  # Red
            "high": "#f0ad4e",      # Orange
            "medium": "#5bc0de",    # Blue
            "low": "#5cb85c"        # Green
        }
        created_at = date_time_now()
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cybersecurity Digest for {self.persona_type}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        h2 {{ color: #2c3e50; margin-top: 30px; }}
        .executive-summary {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #2c3e50; margin-bottom: 25px; }}
        .article {{ margin-bottom: 30px; padding-bottom: 20px; border-bottom: 1px solid #eee; }}
        .article-image {{ max-width: 100%; height: auto; margin: 15px 0; }}
        .article-meta {{ font-size: 14px; color: #666; margin-bottom: 15px; background-color: #f9f9f9; padding: 10px; border-radius: 4px; }}
        .article-meta a {{ color: #337ab7; text-decoration: none; }}
        .article-meta a:hover {{ text-decoration: underline; }}
        .priority {{ display: inline-block; padding: 3px 8px; border-radius: 3px; font-size: 12px; font-weight: bold; color: white; }}
        .strategic-implications {{ background-color: #f8f9fa; padding: 15px; border-left: 4px solid #2c3e50; margin-top: 25px; }}
        .footer {{ margin-top: 30px; font-size: 12px; color: #777; text-align: center; }}
    </style>
</head>

<body>    
    <h1>Cybersecurity Digest for {self.persona_type}</h1>
    <b> cache</b>: <a href="/cache/cache-entry?cache_id={cache_id }" target="_black">entry</a> | 
                   <a href="/cache/cache-response?cache_id={cache_id }" target="_black">response</a> |
                   <a href="/cache/cache-prompt?cache_id={cache_id }" target="_black">prompt</a>
    
    <h2>Executive Summary</h2>
    <div class="executive-summary">
        
        <p>{self.executive_summary.introduction}</p>
        
        {self.render_html__executive_summary_sections()}
    </div>
        
    <h2>Strategic Implications</h2>
    <div class="strategic-implications">        
        <p>{self.strategic_implications}</p>
    </div>
"""

        for article in self.articles:
            color = priority_colors.get(article.priority_level.lower(), "#777")

            image_html = ""
            if article.article_image_link_url:
                image_html = f'<img src="{article.article_image_link_url}" alt="Article illustration" class="article-image">'

            html += f"""
    <div class="article">
        <h2>{article.headline}</h2>
        <div class="article-meta">
            <strong>Source:</strong> <a href="{article.article_source_url}" target="_blank">{article.article_source_url}</a><br>
            <strong>Author:</strong> {article.article_author}<br>
            <strong>Published:</strong> {article.article_when}
        </div>
        {image_html}
        <p>{article.summary}</p>
        <p><strong>Why This Matters:</strong> {article.relevance_analysis}</p>
        <p><strong>Recommended Actions:</strong> {article.action_recommendations}</p>
        <p><span class="priority" style="background-color: {color};">{article.priority_level.upper()}</span></p>
    </div>
"""

        html += f"""    
    <div class="footer">
        <p>Generated: {created_at}</p>
    </div>
</body>
</html>
"""
        return html

    def render_html__executive_summary_sections(self) -> str:              # Helper method to render the executive summary sections."""
        sections_html = ""
        for section in self.executive_summary.sections:
            sections_html += f"""
            <div class="section">                
                <p><strong>{section.section_header}:</strong> {section.section_text}</p>
            </div>"""
        return sections_html