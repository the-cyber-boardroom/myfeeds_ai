from myfeeds_ai.mgraphs.html_to_mgraph.schemas.Schema__Html_MGraph__Theme__Colors import Schema__Html_MGraph__Theme__Colors

# Helper class to provide a more semantic mapping for HTML elements
class Schema__Html_MGraph__Theme(object):
    # Structural elements - more distinct and hierarchical
    HTML         = Schema__Html_MGraph__Theme__Colors.BLUE          # More saturated to clearly identify as root
    HEAD         = Schema__Html_MGraph__Theme__Colors.RED           # Clear red, less aggressive
    BODY         = Schema__Html_MGraph__Theme__Colors.GREEN         # Deeper forest green
    SECTION      = Schema__Html_MGraph__Theme__Colors.GREEN_TEAL    # More vibrant teal
    ARTICLE      = Schema__Html_MGraph__Theme__Colors.GREEN_LIGHT   # Brighter
    MAIN         = Schema__Html_MGraph__Theme__Colors.GREEN_EMERALD # Form elements green
    HEADER       = Schema__Html_MGraph__Theme__Colors.BLUE_DEEP     # Header-specific blue
    FOOTER       = Schema__Html_MGraph__Theme__Colors.BLUE_GRAY     # Footer-specific blue-gray
    DIV          = Schema__Html_MGraph__Theme__Colors.GRAY_LIGHT    # Darker than before for better visibility
    NAV          = Schema__Html_MGraph__Theme__Colors.BLUE_INDIGO   # Header elements blue

    # Text elements - clearer hierarchy and better distinction
    TEXT         = Schema__Html_MGraph__Theme__Colors.GRAY_SLATE    # Darker for better contrast
    P            = Schema__Html_MGraph__Theme__Colors.PURPLE        # Vibrant purple for paragraphs
    H1           = Schema__Html_MGraph__Theme__Colors.PURPLE_DARK   # Deepest purple for H1
    H2           = Schema__Html_MGraph__Theme__Colors.PURPLE_DEEP   # Medium purple for H2
    H3           = Schema__Html_MGraph__Theme__Colors.PURPLE_LIGHT  # Lighter purple for H3
    A            = Schema__Html_MGraph__Theme__Colors.BLUE_LIGHT    # Brighter blue for links
    SPAN         = Schema__Html_MGraph__Theme__Colors.GRAY_MEDIUM   # Slightly blue-tinted
    EM           = Schema__Html_MGraph__Theme__Colors.GREEN_MINT    # Higher saturation
    STRONG       = Schema__Html_MGraph__Theme__Colors.RED_LIGHT     # Brighter red
    B            = Schema__Html_MGraph__Theme__Colors.RED_BRIGHT    # Vibrant red
    NOBR         = Schema__Html_MGraph__Theme__Colors.BLUE_GRAY     # Footer-specific blue-gray
    CENTER       = Schema__Html_MGraph__Theme__Colors.BLUE_INDIGO   # Header elements blue

    # Form elements - more vibrant and distinct
    FORM         = Schema__Html_MGraph__Theme__Colors.GREEN_EMERALD # Form elements green
    INPUT        = Schema__Html_MGraph__Theme__Colors.CYAN          # Brighter cyan
    BUTTON       = Schema__Html_MGraph__Theme__Colors.ORANGE_LIGHT  # Bright orange
    LABEL        = Schema__Html_MGraph__Theme__Colors.CYAN          # Brighter cyan

    # Table elements - maintained brown family
    TABLE        = Schema__Html_MGraph__Theme__Colors.BROWN         # Table elements
    TR           = Schema__Html_MGraph__Theme__Colors.BROWN_MEDIUM  # Table rows
    TD           = Schema__Html_MGraph__Theme__Colors.BROWN_LIGHT   # Table cells

    # Head elements - better contrast
    META         = Schema__Html_MGraph__Theme__Colors.GRAY_MEDIUM   # Slightly blue-tinted
    TITLE        = Schema__Html_MGraph__Theme__Colors.ORANGE_AMBER  # Medium orange
    LINK         = Schema__Html_MGraph__Theme__Colors.TURQUOISE     # Deeper for distinction
    STYLE        = Schema__Html_MGraph__Theme__Colors.PURPLE_DEEP   # Medium purple
    SCRIPT       = Schema__Html_MGraph__Theme__Colors.BLUE_NAVY     # Script elements
    NOSCRIPT     = Schema__Html_MGraph__Theme__Colors.BLUE_GRAY     # Footer-specific blue-gray

    # List elements - clearer parent-child relationship
    UL           = Schema__Html_MGraph__Theme__Colors.ORANGE        # Deep orange for lists
    LI           = Schema__Html_MGraph__Theme__Colors.ORANGE_AMBER  # Medium orange for list items

    # Media elements - distinctive
    IMG          = Schema__Html_MGraph__Theme__Colors.ORANGE_DEEP   # Rich orange for images
    SVG          = Schema__Html_MGraph__Theme__Colors.ORANGE_DEEP   # Rich orange for SVG
    IFRAME       = Schema__Html_MGraph__Theme__Colors.BLUE_INDIGO   # Header elements blue

    # Misc elements - better visibility
    BR           = Schema__Html_MGraph__Theme__Colors.GRAY_DARK     # Darker blue-gray
    HR           = Schema__Html_MGraph__Theme__Colors.GRAY_DARKER   # For numerical annotations
    PATH         = Schema__Html_MGraph__Theme__Colors.ORANGE_AMBER  # Medium orange

    # Text colors - unchanged
    TEXT_LIGHT   = Schema__Html_MGraph__Theme__Colors.WHITE
    TEXT_DARK    = Schema__Html_MGraph__Theme__Colors.BLACK