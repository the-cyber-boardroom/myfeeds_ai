# Define color theme using an Enum
from enum import Enum


class Schema__Html_MGraph__Theme__Colors(Enum):
    # Base colors
    WHITE     = "#ffffff"
    BLACK     = "#000000"

    # Neutral grays - adjusted for better contrast
    GRAY_LIGHT     = "#BDBDBD"  # Darker than before for better visibility
    GRAY_MEDIUM    = "#90A4AE"  # Slightly blue-tinted
    GRAY_DARK      = "#546E7A"  # Darker blue-gray
    GRAY_DARKER    = "#455A64"  # For numerical annotations
    GRAY_SLATE     = "#37474F"  # For text

    # Blue family - more vibrant and distinct
    BLUE           = "#1E88E5"  # More saturated root color
    BLUE_LIGHT     = "#42A5F5"  # Brighter for links
    BLUE_DARK      = "#1565C0"  # Deeper blue
    BLUE_NAVY      = "#283593"  # Script elements
    BLUE_INDIGO    = "#5C6BC0"  # Header elements
    BLUE_GRAY      = "#7986CB"  # Footer elements
    BLUE_DEEP      = "#3949AB"  # Header element

    # Green family - adjusted for better distinction
    GREEN          = "#2E7D32"  # Deeper forest green
    GREEN_LIGHT    = "#66BB6A"  # Brighter
    GREEN_DARK     = "#1B5E20"  # Very deep green
    GREEN_TEAL     = "#26A69A"  # More vibrant teal
    GREEN_MINT     = "#4DB6AC"  # Higher saturation
    GREEN_EMERALD  = "#43A047"  # Form elements

    # Red family - adjusted for better clarity
    RED            = "#D32F2F"  # Clear red, less aggressive
    RED_LIGHT      = "#EF5350"  # Brighter
    RED_DARK       = "#B71C1C"  # Deep red
    RED_BRIGHT     = "#F44336"  # Vibrant red

    # Orange family - more distinct from each other
    ORANGE         = "#EF6C00"  # Deep orange for UL
    ORANGE_LIGHT   = "#FF9800"  # Bright orange for buttons
    ORANGE_DEEP    = "#F57C00"  # Rich orange for images
    ORANGE_AMBER   = "#FFA726"  # Medium orange for list items

    # Purple family - clearer progression for headings
    PURPLE         = "#9C27B0"  # Vibrant purple for paragraphs
    PURPLE_LIGHT   = "#AB47BC"  # For H3
    PURPLE_DARK    = "#7B1FA2"  # For H1
    PURPLE_DEEP    = "#8E24AA"  # For H2

    # Brown family - more distinct
    BROWN          = "#795548"  # Table elements
    BROWN_LIGHT    = "#A1887F"  # Table cells
    BROWN_MEDIUM   = "#8D6E63"  # Table rows

    # Cyan/Turquoise family
    CYAN           = "#00ACC1"  # Brighter cyan for input/label
    TURQUOISE      = "#00897B"  # Deeper for distinction

    # Olive - for content relationship edges
    OLIVE          = "#9E9D24"