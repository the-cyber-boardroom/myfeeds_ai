from myfeeds_ai.mgraphs.html_to_mgraph.Html_MGraph__Theme__Colors import Html_MGraph__Theme__Colors


# Helper class to provide a more semantic mapping for HTML elements
class Html_MGraph__Theme(object):
    # Structural elements - more distinct and hierarchical
    HTML         = Html_MGraph__Theme__Colors.BLUE          # More saturated to clearly identify as root
    HEAD         = Html_MGraph__Theme__Colors.RED           # Clear red, less aggressive
    BODY         = Html_MGraph__Theme__Colors.GREEN         # Deeper forest green
    SECTION      = Html_MGraph__Theme__Colors.GREEN_TEAL    # More vibrant teal
    ARTICLE      = Html_MGraph__Theme__Colors.GREEN_LIGHT   # Brighter
    MAIN         = Html_MGraph__Theme__Colors.GREEN_EMERALD # Form elements green
    HEADER       = Html_MGraph__Theme__Colors.BLUE_DEEP     # Header-specific blue
    FOOTER       = Html_MGraph__Theme__Colors.BLUE_GRAY     # Footer-specific blue-gray
    DIV          = Html_MGraph__Theme__Colors.GRAY_LIGHT    # Darker than before for better visibility
    NAV          = Html_MGraph__Theme__Colors.BLUE_INDIGO   # Header elements blue

    # Text elements - clearer hierarchy and better distinction
    TEXT         = Html_MGraph__Theme__Colors.GRAY_SLATE    # Darker for better contrast
    P            = Html_MGraph__Theme__Colors.PURPLE        # Vibrant purple for paragraphs
    H1           = Html_MGraph__Theme__Colors.PURPLE_DARK   # Deepest purple for H1
    H2           = Html_MGraph__Theme__Colors.PURPLE_DEEP   # Medium purple for H2
    H3           = Html_MGraph__Theme__Colors.PURPLE_LIGHT  # Lighter purple for H3
    A            = Html_MGraph__Theme__Colors.BLUE_LIGHT    # Brighter blue for links
    SPAN         = Html_MGraph__Theme__Colors.GRAY_MEDIUM   # Slightly blue-tinted
    EM           = Html_MGraph__Theme__Colors.GREEN_MINT    # Higher saturation
    STRONG       = Html_MGraph__Theme__Colors.RED_LIGHT     # Brighter red
    B            = Html_MGraph__Theme__Colors.RED_BRIGHT    # Vibrant red
    NOBR         = Html_MGraph__Theme__Colors.BLUE_GRAY     # Footer-specific blue-gray
    CENTER       = Html_MGraph__Theme__Colors.BLUE_INDIGO   # Header elements blue

    # Form elements - more vibrant and distinct
    FORM         = Html_MGraph__Theme__Colors.GREEN_EMERALD # Form elements green
    INPUT        = Html_MGraph__Theme__Colors.CYAN          # Brighter cyan
    BUTTON       = Html_MGraph__Theme__Colors.ORANGE_LIGHT  # Bright orange
    LABEL        = Html_MGraph__Theme__Colors.CYAN          # Brighter cyan

    # Table elements - maintained brown family
    TABLE        = Html_MGraph__Theme__Colors.BROWN         # Table elements
    TR           = Html_MGraph__Theme__Colors.BROWN_MEDIUM  # Table rows
    TD           = Html_MGraph__Theme__Colors.BROWN_LIGHT   # Table cells

    # Head elements - better contrast
    META         = Html_MGraph__Theme__Colors.GRAY_MEDIUM   # Slightly blue-tinted
    TITLE        = Html_MGraph__Theme__Colors.ORANGE_AMBER  # Medium orange
    LINK         = Html_MGraph__Theme__Colors.TURQUOISE     # Deeper for distinction
    STYLE        = Html_MGraph__Theme__Colors.PURPLE_DEEP   # Medium purple
    SCRIPT       = Html_MGraph__Theme__Colors.BLUE_NAVY     # Script elements
    NOSCRIPT     = Html_MGraph__Theme__Colors.BLUE_GRAY     # Footer-specific blue-gray

    # List elements - clearer parent-child relationship
    UL           = Html_MGraph__Theme__Colors.ORANGE        # Deep orange for lists
    LI           = Html_MGraph__Theme__Colors.ORANGE_AMBER  # Medium orange for list items

    # Media elements - distinctive
    IMG          = Html_MGraph__Theme__Colors.ORANGE_DEEP   # Rich orange for images
    SVG          = Html_MGraph__Theme__Colors.ORANGE_DEEP   # Rich orange for SVG
    IFRAME       = Html_MGraph__Theme__Colors.BLUE_INDIGO   # Header elements blue

    # Misc elements - better visibility
    BR           = Html_MGraph__Theme__Colors.GRAY_DARK     # Darker blue-gray
    HR           = Html_MGraph__Theme__Colors.GRAY_DARKER   # For numerical annotations
    PATH         = Html_MGraph__Theme__Colors.ORANGE_AMBER  # Medium orange

    # Text colors - unchanged
    TEXT_LIGHT   = Html_MGraph__Theme__Colors.WHITE
    TEXT_DARK    = Html_MGraph__Theme__Colors.BLACK