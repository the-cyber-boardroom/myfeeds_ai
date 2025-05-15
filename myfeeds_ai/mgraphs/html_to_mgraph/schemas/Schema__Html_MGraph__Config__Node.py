from typing import Dict, Type

from myfeeds_ai.mgraphs.html_to_mgraph.schemas.Schema__Html_MGraph__Nodes import Schema__Html_MGraph__Node__HTML__HTML, \
    Schema__Html_MGraph__Node__HTML__HEAD, Schema__Html_MGraph__Node__HTML__BODY, Schema__Html_MGraph__Node__HTML__P, \
    Schema__Html_MGraph__Node__HTML__TEXT, Schema__Html_MGraph__Node__HTML__DIV, Schema__Html_MGraph__Node__HTML__NAV, \
    Schema__Html_MGraph__Node__HTML__LINK, Schema__Html_MGraph__Node__HTML__TITLE, Schema__Html_MGraph__Node__HTML__META, \
    Schema__Html_MGraph__Node__HTML__SCRIPT, Schema__Html_MGraph__Node__HTML__H1, Schema__Html_MGraph__Node__HTML__LI, \
    Schema__Html_MGraph__Node__HTML__UL, Schema__Html_MGraph__Node__HTML__SPAN, Schema__Html_MGraph__Node__HTML__BUTTON, \
    Schema__Html_MGraph__Node__HTML__A, Schema__Html_MGraph__Node__HTML__STYLE, Schema__Html_MGraph__Node__HTML__FOOTER, \
    Schema__Html_MGraph__Node__HTML__TABLE, Schema__Html_MGraph__Node__HTML__INPUT, Schema__Html_MGraph__Node__HTML__FORM, \
    Schema__Html_MGraph__Node__HTML__BR, Schema__Html_MGraph__Node__HTML__HR, Schema__Html_MGraph__Node__HTML__IMG, \
    Schema__Html_MGraph__Node__HTML__TR, Schema__Html_MGraph__Node__HTML__TD, Schema__Html_MGraph__Node__HTML__CENTER, \
    Schema__Html_MGraph__Node__HTML__H2, Schema__Html_MGraph__Node__HTML__H3, Schema__Html_MGraph__Node__HTML__SVG, \
    Schema__Html_MGraph__Node__HTML__EM, Schema__Html_MGraph__Node__HTML__STRONG, Schema__Html_MGraph__Node__HTML__IFRAME, \
    Schema__Html_MGraph__Node__HTML__SECTION, Schema__Html_MGraph__Node__HTML__HEADER, Schema__Html_MGraph__Node__HTML__NOSCRIPT, \
    Schema__Html_MGraph__Node__HTML__B, Schema__Html_MGraph__Node__HTML__NOBR, Schema__Html_MGraph__Node__HTML__LABEL, \
    Schema__Html_MGraph__Node__HTML__MAIN, Schema__Html_MGraph__Node__HTML__PATH, Schema__Html_MGraph__Node__HTML__ARTICLE
from myfeeds_ai.mgraphs.html_to_mgraph.schemas.Schema__Html_MGraph__Theme import Schema__Html_MGraph__Theme
from myfeeds_ai.mgraphs.html_to_mgraph.schemas.Schema__Html_MGraph__Theme__Colors import \
    Schema__Html_MGraph__Theme__Colors

from osbot_utils.type_safe.Type_Safe import Type_Safe



# Define base HTML node configuration class
class Schema__Html_MGraph__Config__Node(Type_Safe):
    """Base configuration class for all HTML nodes"""
    fill_color  : str = None # Schema__Html_MGraph__Theme__Colors.GRAY_LIGHT.value  # Light gray default
    font_color  : str = None # Schema__Html_MGraph__Theme__Colors.BLACK.value      # Black font by default
    shape       : str = None # = "box"      # Default box shape
    style       : str = None # "rounded"  # Rounded by default
    font_size   : int = None #12
    font_name   : str = None #"Arial"

# Define common base classes to reduce duplication
class Html_MGraph__Config__Node__White_Text(Schema__Html_MGraph__Config__Node):
    """Base class for nodes with white text"""
    font_color  : str = Schema__Html_MGraph__Theme__Colors.WHITE.value  # White text

class Html_MGraph__Config__Node__Rounded_Filled(Html_MGraph__Config__Node__White_Text):
    """Base class for rounded, filled nodes with white text"""
    style       : str = "rounded,filled"

# Define individual node classes
class Html_MGraph__Config__Node__HTML(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.HTML.value
    shape       : str = "hexagon"
    font_size   : int = 50

class Html_MGraph__Config__Node__HEAD(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.HEAD.value
    shape       : str = "hexagon"
    font_size   : int = 30

class Html_MGraph__Config__Node__BODY(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.BODY.value
    shape       : str = "hexagon"
    font_size   : int = 30

class Html_MGraph__Config__Node__P(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.P.value
    shape       : str = "note"

class Html_MGraph__Config__Node__TEXT(Html_MGraph__Config__Node__Rounded_Filled):
    fill_color  : str = Schema__Html_MGraph__Theme.TEXT.value
    shape       : str = "box"

class Html_MGraph__Config__Node__META(Schema__Html_MGraph__Config__Node):
    fill_color  : str = Schema__Html_MGraph__Theme.META.value
    shape       : str = "ellipse"

class Html_MGraph__Config__Node__TITLE(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.TITLE.value
    shape       : str = "box"

class Html_MGraph__Config__Node__LINK(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.LINK.value
    shape       : str = "ellipse"

class Html_MGraph__Config__Node__NAV(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.NAV.value
    shape       : str = "component"

class Html_MGraph__Config__Node__DIV(Schema__Html_MGraph__Config__Node):
    fill_color  : str = Schema__Html_MGraph__Theme.DIV.value
    shape       : str = "box"

class Html_MGraph__Config__Node__A(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.A.value
    shape       : str = "ellipse"

class Html_MGraph__Config__Node__BUTTON(Html_MGraph__Config__Node__Rounded_Filled):
    fill_color  : str = Schema__Html_MGraph__Theme.BUTTON.value
    font_color  : str = Schema__Html_MGraph__Theme__Colors.BLACK.value  # Override to black

class Html_MGraph__Config__Node__SPAN(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.SPAN.value
    shape       : str = "ellipse"

class Html_MGraph__Config__Node__UL(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.UL.value
    shape       : str = "folder"

class Html_MGraph__Config__Node__LI(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.LI.value
    shape       : str = "box"

class Html_MGraph__Config__Node__H1(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.H1.value
    shape       : str = "box"
    style       : str = "filled,bold"

class Html_MGraph__Config__Node__SCRIPT(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.SCRIPT.value
    shape       : str = "cds"

# New HTML element node classes
class Html_MGraph__Config__Node__STYLE(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.STYLE.value
    shape       : str = "component"

class Html_MGraph__Config__Node__FOOTER(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.FOOTER.value
    shape       : str = "tab"

class Html_MGraph__Config__Node__TABLE(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.TABLE.value
    shape       : str = "box3d"

class Html_MGraph__Config__Node__INPUT(Html_MGraph__Config__Node__Rounded_Filled):
    fill_color  : str = Schema__Html_MGraph__Theme.INPUT.value

class Html_MGraph__Config__Node__FORM(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.FORM.value
    shape       : str = "folder"

class Html_MGraph__Config__Node__BR(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.BR.value
    shape       : str = "point"

class Html_MGraph__Config__Node__HR(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.HR.value
    shape       : str = "rectangle"
    style       : str = "bold"

class Html_MGraph__Config__Node__IMG(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.IMG.value
    shape       : str = "note"

class Html_MGraph__Config__Node__TR(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.TR.value
    shape       : str = "box"

class Html_MGraph__Config__Node__TD(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.TD.value
    shape       : str = "square"

class Html_MGraph__Config__Node__CENTER(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.CENTER.value
    shape       : str = "diamond"

class Html_MGraph__Config__Node__H2(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.H2.value
    shape       : str = "box"
    style       : str = "filled,bold"

class Html_MGraph__Config__Node__H3(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.H3.value
    shape       : str = "box"
    style       : str = "filled"

class Html_MGraph__Config__Node__SVG(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.SVG.value
    shape       : str = "octagon"
    style       : str = "filled"

class Html_MGraph__Config__Node__EM(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.EM.value
    shape       : str = "egg"
    style       : str = "filled,italic"

class Html_MGraph__Config__Node__STRONG(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.STRONG.value
    shape       : str = "box"
    style       : str = "filled,bold"

class Html_MGraph__Config__Node__IFRAME(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.IFRAME.value
    shape       : str = "rect"
    style       : str = "filled,dashed"

class Html_MGraph__Config__Node__SECTION(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.SECTION.value
    shape       : str = "folder"
    style       : str = "filled"

class Html_MGraph__Config__Node__HEADER(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.HEADER.value
    shape       : str = "tab"
    style       : str = "filled"

class Html_MGraph__Config__Node__NOSCRIPT(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.NOSCRIPT.value
    shape       : str = "component"
    style       : str = "filled,dashed"

class Html_MGraph__Config__Node__B(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.B.value
    shape       : str = "box"
    style       : str = "filled,bold"

class Html_MGraph__Config__Node__NOBR(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.NOBR.value
    shape       : str = "ellipse"
    style       : str = "filled"

class Html_MGraph__Config__Node__LABEL(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.LABEL.value
    shape       : str = "house"
    style       : str = "filled"

class Html_MGraph__Config__Node__MAIN(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.MAIN.value
    shape       : str = "tab"
    style       : str = "filled,bold"

class Html_MGraph__Config__Node__PATH(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.PATH.value
    shape       : str = "cds"
    style       : str = "filled"

class Html_MGraph__Config__Node__ARTICLE(Html_MGraph__Config__Node__White_Text):
    fill_color  : str = Schema__Html_MGraph__Theme.ARTICLE.value
    shape       : str = "folder"
    style       : str = "filled"


# Create mapping of schema types to config objects
HTML_MGRAPH__NODES__CONFIG: Dict[Type, Schema__Html_MGraph__Config__Node] = {
    # Basic HTML structure elements
    Schema__Html_MGraph__Node__HTML__HTML    : Html_MGraph__Config__Node__HTML(),
    Schema__Html_MGraph__Node__HTML__HEAD    : Html_MGraph__Config__Node__HEAD(),
    Schema__Html_MGraph__Node__HTML__BODY    : Html_MGraph__Config__Node__BODY(),

    # Text and content elements
    Schema__Html_MGraph__Node__HTML__P       : Html_MGraph__Config__Node__P(),
    Schema__Html_MGraph__Node__HTML__TEXT    : Html_MGraph__Config__Node__TEXT(),
    Schema__Html_MGraph__Node__HTML__H1      : Html_MGraph__Config__Node__H1(),
    Schema__Html_MGraph__Node__HTML__H2      : Html_MGraph__Config__Node__H2(),
    Schema__Html_MGraph__Node__HTML__H3      : Html_MGraph__Config__Node__H3(),
    Schema__Html_MGraph__Node__HTML__A       : Html_MGraph__Config__Node__A(),
    Schema__Html_MGraph__Node__HTML__EM      : Html_MGraph__Config__Node__EM(),
    Schema__Html_MGraph__Node__HTML__STRONG  : Html_MGraph__Config__Node__STRONG(),
    Schema__Html_MGraph__Node__HTML__B       : Html_MGraph__Config__Node__B(),
    Schema__Html_MGraph__Node__HTML__NOBR    : Html_MGraph__Config__Node__NOBR(),

    # Head elements
    Schema__Html_MGraph__Node__HTML__META    : Html_MGraph__Config__Node__META(),
    Schema__Html_MGraph__Node__HTML__TITLE   : Html_MGraph__Config__Node__TITLE(),
    Schema__Html_MGraph__Node__HTML__LINK    : Html_MGraph__Config__Node__LINK(),
    Schema__Html_MGraph__Node__HTML__STYLE   : Html_MGraph__Config__Node__STYLE(),
    Schema__Html_MGraph__Node__HTML__SCRIPT  : Html_MGraph__Config__Node__SCRIPT(),
    Schema__Html_MGraph__Node__HTML__NOSCRIPT: Html_MGraph__Config__Node__NOSCRIPT(),

    # Structural elements
    Schema__Html_MGraph__Node__HTML__DIV     : Html_MGraph__Config__Node__DIV(),
    Schema__Html_MGraph__Node__HTML__NAV     : Html_MGraph__Config__Node__NAV(),
    Schema__Html_MGraph__Node__HTML__SPAN    : Html_MGraph__Config__Node__SPAN(),
    Schema__Html_MGraph__Node__HTML__CENTER  : Html_MGraph__Config__Node__CENTER(),
    Schema__Html_MGraph__Node__HTML__FOOTER  : Html_MGraph__Config__Node__FOOTER(),
    Schema__Html_MGraph__Node__HTML__HEADER  : Html_MGraph__Config__Node__HEADER(),
    Schema__Html_MGraph__Node__HTML__SECTION : Html_MGraph__Config__Node__SECTION(),
    Schema__Html_MGraph__Node__HTML__ARTICLE : Html_MGraph__Config__Node__ARTICLE(),
    Schema__Html_MGraph__Node__HTML__MAIN    : Html_MGraph__Config__Node__MAIN(),

    # List elements
    Schema__Html_MGraph__Node__HTML__UL      : Html_MGraph__Config__Node__UL(),
    Schema__Html_MGraph__Node__HTML__LI      : Html_MGraph__Config__Node__LI(),

    # Interactive elements
    Schema__Html_MGraph__Node__HTML__BUTTON  : Html_MGraph__Config__Node__BUTTON(),
    Schema__Html_MGraph__Node__HTML__INPUT   : Html_MGraph__Config__Node__INPUT(),
    Schema__Html_MGraph__Node__HTML__FORM    : Html_MGraph__Config__Node__FORM(),
    Schema__Html_MGraph__Node__HTML__LABEL   : Html_MGraph__Config__Node__LABEL(),

    # Table elements
    Schema__Html_MGraph__Node__HTML__TABLE   : Html_MGraph__Config__Node__TABLE(),
    Schema__Html_MGraph__Node__HTML__TR      : Html_MGraph__Config__Node__TR(),
    Schema__Html_MGraph__Node__HTML__TD      : Html_MGraph__Config__Node__TD(),

    # Media elements
    Schema__Html_MGraph__Node__HTML__IMG     : Html_MGraph__Config__Node__IMG(),
    Schema__Html_MGraph__Node__HTML__SVG     : Html_MGraph__Config__Node__SVG(),
    Schema__Html_MGraph__Node__HTML__IFRAME  : Html_MGraph__Config__Node__IFRAME(),
    Schema__Html_MGraph__Node__HTML__PATH    : Html_MGraph__Config__Node__PATH(),

    # Misc elements
    Schema__Html_MGraph__Node__HTML__BR      : Html_MGraph__Config__Node__BR(),
    Schema__Html_MGraph__Node__HTML__HR      : Html_MGraph__Config__Node__HR()
}