from mgraph_db.mgraph.schemas.Schema__MGraph__Edge import Schema__MGraph__Edge

# Schema__Html_MGraph__Edges class for HTML elements

class Schema__Html_MGraph__Edge__HTML__BODY  (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__HEAD  (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__HTML  (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__TEXT  (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__P     (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__DIV   (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__SPAN  (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__A     (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__UL    (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__LI    (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__STYLE (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__SCRIPT(Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__INPUT (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__FORM  (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__TABLE (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__TR    (Schema__MGraph__Edge) : pass
class Schema__Html_MGraph__Edge__HTML__TD    (Schema__MGraph__Edge) : pass

# Mapping from HTML tag names to edge types
HTML__EDGES_TYPES__FOR__TAG = {
    'body'  : Schema__Html_MGraph__Edge__HTML__BODY  ,
    'head'  : Schema__Html_MGraph__Edge__HTML__HEAD  ,
    'html'  : Schema__Html_MGraph__Edge__HTML__HTML  ,
    'p'     : Schema__Html_MGraph__Edge__HTML__P     ,
    'text'  : Schema__Html_MGraph__Edge__HTML__TEXT  ,
    'div'   : Schema__Html_MGraph__Edge__HTML__DIV   ,
    'span'  : Schema__Html_MGraph__Edge__HTML__SPAN  ,
    'a'     : Schema__Html_MGraph__Edge__HTML__A     ,
    'ul'    : Schema__Html_MGraph__Edge__HTML__UL    ,
    'li'    : Schema__Html_MGraph__Edge__HTML__LI    ,
    'style' : Schema__Html_MGraph__Edge__HTML__STYLE ,
    'script': Schema__Html_MGraph__Edge__HTML__SCRIPT,
    'input' : Schema__Html_MGraph__Edge__HTML__INPUT ,
    'form'  : Schema__Html_MGraph__Edge__HTML__FORM  ,
    'table' : Schema__Html_MGraph__Edge__HTML__TABLE ,
    'tr'    : Schema__Html_MGraph__Edge__HTML__TR    ,
    'td'    : Schema__Html_MGraph__Edge__HTML__TD
}