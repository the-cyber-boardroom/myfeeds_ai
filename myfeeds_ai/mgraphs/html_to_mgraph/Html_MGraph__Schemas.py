from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value import Schema__MGraph__Node__Value
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge import Schema__MGraph__Edge


# Edge classes for HTML elements
class Schema__MGraph__Edge__HTML__BODY(Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__HEAD(Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__HTML(Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__TEXT(Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__P   (Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__DIV (Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__SPAN(Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__A   (Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__UL  (Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__LI  (Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__STYLE(Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__SCRIPT(Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__INPUT(Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__FORM(Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__TABLE(Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__TR  (Schema__MGraph__Edge) : pass
class Schema__MGraph__Edge__HTML__TD  (Schema__MGraph__Edge) : pass

# Node classes for HTML elements
class Schema__MGraph__NODE__HTML__BODY  (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__HEAD  (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__HTML  (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__TEXT  (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__P     (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__META  (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__TITLE (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__LINK  (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__NAV   (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__DIV   (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__A     (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__BUTTON(Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__SPAN  (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__UL    (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__LI    (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__H1    (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__SCRIPT(Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__STYLE (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__FOOTER(Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__TABLE (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__INPUT (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__FORM  (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__BR    (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__HR    (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__IMG   (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__TR    (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__TD    (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__CENTER(Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__H2      (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__H3      (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__SVG     (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__EM      (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__STRONG  (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__IFRAME  (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__SECTION (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__HEADER  (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__NOSCRIPT(Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__B      (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__NOBR   (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__LABEL  (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__MAIN   (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__PATH   (Schema__MGraph__Node__Value) : pass
class Schema__MGraph__NODE__HTML__ARTICLE(Schema__MGraph__Node__Value) : pass



# Mapping from HTML tag names to edge types
HTML__EDGES_TYPES__FOR__TAG = {
    'body'  : Schema__MGraph__Edge__HTML__BODY,
    'head'  : Schema__MGraph__Edge__HTML__HEAD,
    'html'  : Schema__MGraph__Edge__HTML__HTML,
    'p'     : Schema__MGraph__Edge__HTML__P,
    'text'  : Schema__MGraph__Edge__HTML__TEXT,
    'div'   : Schema__MGraph__Edge__HTML__DIV,
    'span'  : Schema__MGraph__Edge__HTML__SPAN,
    'a'     : Schema__MGraph__Edge__HTML__A,
    'ul'    : Schema__MGraph__Edge__HTML__UL,
    'li'    : Schema__MGraph__Edge__HTML__LI,
    'style' : Schema__MGraph__Edge__HTML__STYLE,
    'script': Schema__MGraph__Edge__HTML__SCRIPT,
    'input' : Schema__MGraph__Edge__HTML__INPUT,
    'form'  : Schema__MGraph__Edge__HTML__FORM,
    'table' : Schema__MGraph__Edge__HTML__TABLE,
    'tr'    : Schema__MGraph__Edge__HTML__TR,
    'td'    : Schema__MGraph__Edge__HTML__TD
}

# Mapping from HTML tag names to node types
HTML__NODES_TYPES__FOR__TAG = {
    'body'    : Schema__MGraph__NODE__HTML__BODY,
    'head'    : Schema__MGraph__NODE__HTML__HEAD,
    'html'    : Schema__MGraph__NODE__HTML__HTML,
    'p'       : Schema__MGraph__NODE__HTML__P,
    'text'    : Schema__MGraph__NODE__HTML__TEXT,
    'meta'    : Schema__MGraph__NODE__HTML__META,
    'title'   : Schema__MGraph__NODE__HTML__TITLE,
    'link'    : Schema__MGraph__NODE__HTML__LINK,
    'nav'     : Schema__MGraph__NODE__HTML__NAV,
    'div'     : Schema__MGraph__NODE__HTML__DIV,
    'a'       : Schema__MGraph__NODE__HTML__A,
    'button'  : Schema__MGraph__NODE__HTML__BUTTON,
    'span'    : Schema__MGraph__NODE__HTML__SPAN,
    'ul'      : Schema__MGraph__NODE__HTML__UL,
    'li'      : Schema__MGraph__NODE__HTML__LI,
    'h1'      : Schema__MGraph__NODE__HTML__H1,
    'script'  : Schema__MGraph__NODE__HTML__SCRIPT,
    'style'   : Schema__MGraph__NODE__HTML__STYLE,
    'footer'  : Schema__MGraph__NODE__HTML__FOOTER,
    'table'   : Schema__MGraph__NODE__HTML__TABLE,
    'input'   : Schema__MGraph__NODE__HTML__INPUT,
    'form'    : Schema__MGraph__NODE__HTML__FORM,
    'br'      : Schema__MGraph__NODE__HTML__BR,
    'hr'      : Schema__MGraph__NODE__HTML__HR,
    'img'     : Schema__MGraph__NODE__HTML__IMG,
    'tr'      : Schema__MGraph__NODE__HTML__TR,
    'td'      : Schema__MGraph__NODE__HTML__TD,
    'center'  : Schema__MGraph__NODE__HTML__CENTER,
    'h2'      : Schema__MGraph__NODE__HTML__H2,
    'h3'      : Schema__MGraph__NODE__HTML__H3,
    'svg'     : Schema__MGraph__NODE__HTML__SVG,
    'em'      : Schema__MGraph__NODE__HTML__EM,
    'strong'  : Schema__MGraph__NODE__HTML__STRONG,
    'iframe'  : Schema__MGraph__NODE__HTML__IFRAME,
    'section' : Schema__MGraph__NODE__HTML__SECTION,
    'header'  : Schema__MGraph__NODE__HTML__HEADER,
    'noscript': Schema__MGraph__NODE__HTML__NOSCRIPT,
    'b'       : Schema__MGraph__NODE__HTML__B,
    'nobr'    : Schema__MGraph__NODE__HTML__NOBR,
    'label'   : Schema__MGraph__NODE__HTML__LABEL,
    'main'    : Schema__MGraph__NODE__HTML__MAIN,
    'path'    : Schema__MGraph__NODE__HTML__PATH,
    'article' : Schema__MGraph__NODE__HTML__ARTICLE
}