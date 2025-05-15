from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Value import Schema__MGraph__Node__Value

# Schema__Html_MGraph__Nodes class for HTML elements

class Schema__Html_MGraph__Node__HTML__BODY    (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__HEAD    (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__HTML    (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__TEXT    (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__P       (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__META    (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__TITLE   (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__LINK    (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__NAV     (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__DIV     (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__A       (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__BUTTON  (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__SPAN    (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__UL      (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__LI      (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__H1      (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__SCRIPT  (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__STYLE   (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__FOOTER  (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__TABLE   (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__INPUT   (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__FORM    (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__BR      (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__HR      (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__IMG     (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__TR      (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__TD      (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__CENTER  (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__H2      (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__H3      (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__SVG     (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__EM      (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__STRONG  (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__IFRAME  (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__SECTION (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__HEADER  (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__NOSCRIPT(Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__B       (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__NOBR    (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__LABEL   (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__MAIN    (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__PATH    (Schema__MGraph__Node__Value) : pass
class Schema__Html_MGraph__Node__HTML__ARTICLE (Schema__MGraph__Node__Value) : pass


# Mapping from HTML tag names to node types
HTML__NODES_TYPES__FOR__TAG = {
    'body'    : Schema__Html_MGraph__Node__HTML__BODY   ,
    'head'    : Schema__Html_MGraph__Node__HTML__HEAD   ,
    'html'    : Schema__Html_MGraph__Node__HTML__HTML   ,
    'p'       : Schema__Html_MGraph__Node__HTML__P      ,
    'text'    : Schema__Html_MGraph__Node__HTML__TEXT   ,
    'meta'    : Schema__Html_MGraph__Node__HTML__META   ,
    'title'   : Schema__Html_MGraph__Node__HTML__TITLE  ,
    'link'    : Schema__Html_MGraph__Node__HTML__LINK   ,
    'nav'     : Schema__Html_MGraph__Node__HTML__NAV    ,
    'div'     : Schema__Html_MGraph__Node__HTML__DIV    ,
    'a'       : Schema__Html_MGraph__Node__HTML__A      ,
    'button'  : Schema__Html_MGraph__Node__HTML__BUTTON ,
    'span'    : Schema__Html_MGraph__Node__HTML__SPAN   ,
    'ul'      : Schema__Html_MGraph__Node__HTML__UL     ,
    'li'      : Schema__Html_MGraph__Node__HTML__LI     ,
    'h1'      : Schema__Html_MGraph__Node__HTML__H1     ,
    'h2'      : Schema__Html_MGraph__Node__HTML__H2     ,
    'h3'      : Schema__Html_MGraph__Node__HTML__H3     ,
    'script'  : Schema__Html_MGraph__Node__HTML__SCRIPT ,
    'style'   : Schema__Html_MGraph__Node__HTML__STYLE  ,
    'footer'  : Schema__Html_MGraph__Node__HTML__FOOTER ,
    'table'   : Schema__Html_MGraph__Node__HTML__TABLE  ,
    'input'   : Schema__Html_MGraph__Node__HTML__INPUT  ,
    'form'    : Schema__Html_MGraph__Node__HTML__FORM   ,
    'br'      : Schema__Html_MGraph__Node__HTML__BR     ,
    'hr'      : Schema__Html_MGraph__Node__HTML__HR     ,
    'img'     : Schema__Html_MGraph__Node__HTML__IMG    ,
    'tr'      : Schema__Html_MGraph__Node__HTML__TR     ,
    'td'      : Schema__Html_MGraph__Node__HTML__TD     ,
    'center'  : Schema__Html_MGraph__Node__HTML__CENTER ,
    'svg'     : Schema__Html_MGraph__Node__HTML__SVG    ,
    'em'      : Schema__Html_MGraph__Node__HTML__EM     ,
    'strong'  : Schema__Html_MGraph__Node__HTML__STRONG ,
    'iframe'  : Schema__Html_MGraph__Node__HTML__IFRAME ,
    'section' : Schema__Html_MGraph__Node__HTML__SECTION,
    'header'  : Schema__Html_MGraph__Node__HTML__HEADER ,
    'noscript': Schema__Html_MGraph__Node__HTML__NOSCRIPT,
    'b'       : Schema__Html_MGraph__Node__HTML__B       ,
    'nobr'    : Schema__Html_MGraph__Node__HTML__NOBR    ,
    'label'   : Schema__Html_MGraph__Node__HTML__LABEL   ,
    'main'    : Schema__Html_MGraph__Node__HTML__MAIN    ,
    'path'    : Schema__Html_MGraph__Node__HTML__PATH    ,
    'article' : Schema__Html_MGraph__Node__HTML__ARTICLE
}