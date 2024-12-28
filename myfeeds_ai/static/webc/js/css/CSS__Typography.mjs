export default class CSS__Typography {
    css_mappings = { 'bootstrap'       : 'css_rules__bootstrap',
                     'foundation'      : 'css_rules__foundation',
                     'tailwind'        : 'css_rules__tailwind',
                     'material-design' : 'css_rules__material_design' }

    constructor(target_element, framework) {
        this.framework      = framework
        this.target_element = target_element
    }

    apply_framework() {
        if (this.target_element) {
            if (this.framework) {
                const css_method = this.css_mappings[this.framework]
                if (css_method && typeof this[css_method] === 'function') {
                    this.target_element.add_css_rules(this[css_method]())
                }
            } else {
                this.target_element.add_css_rules(this.css_rules__standard())
            }
        }
    }
    css_rules__standard() {
        return {
            ":host"                    : { fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif" },

            // Type Scale
            ".type-mega"               : { fontSize: "4rem",      lineHeight: "1.1",  marginBottom: "0.5rem", fontWeight: "300" },
            ".type-hero"               : { fontSize: "3.5rem",    lineHeight: "1.1",  marginBottom: "0.5rem", fontWeight: "300" },
            ".type-title"              : { fontSize: "3rem",      lineHeight: "1.1",  marginBottom: "0.5rem", fontWeight: "300" },
            ".type-xl"                 : { fontSize: "2.5rem",    lineHeight: "1.2",  marginBottom: "0.5rem", fontWeight: "300" },
            ".type-lg"                 : { fontSize: "2rem",      lineHeight: "1.2",  marginBottom: "0.5rem", fontWeight: "300" },
            ".type-md"                 : { fontSize: "1.5rem",    lineHeight: "1.2",  marginBottom: "0.5rem", fontWeight: "400" },
            ".type-sm"                 : { fontSize: "0.875rem",  lineHeight: "1.4",  marginBottom: "0.5rem", fontWeight: "400" },
            ".type-xs"                 : { fontSize: "0.75rem",   lineHeight: "1.4",  marginBottom: "0.5rem", fontWeight: "400" },

            // Weights
            ".weight-thin"             : { fontWeight: "100" },
            ".weight-light"            : { fontWeight: "300" },
            ".weight-normal"           : { fontWeight: "400" },
            ".weight-medium"           : { fontWeight: "500" },
            ".weight-bold"             : { fontWeight: "700" },
            ".weight-heavy"            : { fontWeight: "900" },

            // Alignment
            ".align-start"             : { textAlign: "left" },
            ".align-center"            : { textAlign: "center" },
            ".align-end"               : { textAlign: "right" },

            // Style variations
            ".style-italic"            : { fontStyle: "italic" },
            ".style-normal"            : { fontStyle: "normal" },

            // Text transforms
            ".transform-upper"         : { textTransform: "uppercase", letterSpacing: "0.05em" },
            ".transform-lower"         : { textTransform: "lowercase" },
            ".transform-capital"       : { textTransform: "capitalize" },

            // Colors
            ".color-primary"           : { color: "#1a73e8" },
            ".color-secondary"         : { color: "#5f6368" },
            ".color-accent"            : { color: "#6200ee" },
            ".color-success"           : { color: "#188038" },
            ".color-warning"           : { color: "#f9ab00" },
            ".color-error"             : { color: "#d93025" },
            ".color-info"              : { color: "#1967d2" },
            ".color-muted"             : { color: "#5f6368" },
            ".color-white"             : { color: "#ffffff" },

            // other colors
            ".color-blue"         : { "color"           : "#4A90E2" },
            ".bg-blue"            : { "background-color": "#4A90E2" },

            // Light colors and background
            ".color-light-blue"   : { "color"           : "rgba(13, 110, 253, 0.1)" },
            ".bg-light-blue"      : { "background-color": "rgba(13, 110, 253, 0.1)" },

            ".color-light-gray"   : { "color"           : "rgba(108, 117, 125, 0.1)" },
            ".bg-light-gray"      : { "background-color": "rgba(108, 117, 125, 0.1)" },

            ".color-light-green"  : { "color"           : "#E6FFE6" },
            ".bg-light-green"     : { "background-color": "#E6FFE6" },

            ".color-light-cyan"   : { "color"           : "rgba(13, 202, 240, 0.1)" },
            ".bg-light-cyan"      : { "background-color": "rgba(13, 202, 240, 0.1)" },

            ".color-light-yellow" : { "color"           : "rgba(255, 193, 7, 0.1)" },
            ".bg-light-yellow"    : { "background-color": "rgba(255, 193, 7, 0.1)" },

            ".color-light-red"    : { "color"           : "rgba(220, 53, 69, 0.1)" },
            ".bg-light-red"       : { "background-color": "rgba(220, 53, 69, 0.1)" },

            ".color-light-white"  : { "color"           : "#f8f9fa"                },
            ".bg-light-white"     : { "background-color": "#f8f9fa"                },

            ".color-light-black"  : { "color"           : "#2D3436"                },
            ".bg-light-black"     : { "background-color": "#2D3436"                },





            // Background colors
            ".bg-primary"              : { backgroundColor: "#1a73e8" },
            ".bg-secondary"            : { backgroundColor: "#5f6368" },
            ".bg-accent"               : { backgroundColor: "#6200ee" },
            ".bg-success"              : { backgroundColor: "#188038" },
            ".bg-warning"              : { backgroundColor: "#f9ab00" },
            ".bg-error"                : { backgroundColor: "#d93025" },
            ".bg-info"                 : { backgroundColor: "#1967d2" },
            ".bg-muted"                : { backgroundColor: "#5f6368" },
            ".bg-dark"                 : { backgroundColor: "#212529" },

            // Special text types
            ".type-lead"               : { fontSize: "1.25rem", fontWeight: "300", lineHeight: "1.6", marginBottom: "1rem" },
            ".type-body"               : { fontSize: "1rem",    fontWeight: "400", lineHeight: "1.5", marginBottom: "1rem" },
            ".type-caption"            : { fontSize: "0.875rem",fontWeight: "400", lineHeight: "1.4", color: "#5f6368" },

            // Base elements
            "p"                        : { marginBottom: "1rem", fontSize: "1rem", lineHeight: "1.5" },
            "h1, h2, h3, h4, h5, h6"   : { marginBottom: "0.5rem", fontWeight: "500", lineHeight: "1.2" }
        }
    }

    css_rules__bootstrap() {
        return {
            ":host"                    : { fontFamily: "system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif" },

            // Type Scale
            ".type-mega"               : { fontSize: "5rem",    fontWeight: "300", lineHeight: "1.2", marginBottom: "0.5rem" },
            ".type-hero"               : { fontSize: "4.5rem",  fontWeight: "300", lineHeight: "1.2", marginBottom: "0.5rem" },
            ".type-title"              : { fontSize: "4rem",    fontWeight: "300", lineHeight: "1.2", marginBottom: "0.5rem" },
            ".type-xl"                 : { fontSize: "3.5rem",  fontWeight: "300", lineHeight: "1.2", marginBottom: "0.5rem" },
            ".type-lg"                 : { fontSize: "3rem",    fontWeight: "300", lineHeight: "1.2", marginBottom: "0.5rem" },
            ".type-md"                 : { fontSize: "2.5rem",  fontWeight: "300", lineHeight: "1.2", marginBottom: "0.5rem" },
            ".type-sm"                 : { fontSize: "0.875em", fontWeight: "400", lineHeight: "1.4", marginBottom: "0.5rem" },
            ".type-xs"                 : { fontSize: "0.75em",  fontWeight: "400", lineHeight: "1.4", marginBottom: "0.5rem" },

            // Weights
            ".weight-thin"             : { fontWeight: "100" },
            ".weight-light"            : { fontWeight: "300" },
            ".weight-normal"           : { fontWeight: "400" },
            ".weight-medium"           : { fontWeight: "500" },
            ".weight-bold"             : { fontWeight: "700" },
            ".weight-heavy"            : { fontWeight: "900" },

            // Alignment
            ".align-start"             : { textAlign: "left" },
            ".align-center"            : { textAlign: "center" },
            ".align-end"               : { textAlign: "right" },

            // Style variations
            ".style-italic"            : { fontStyle: "italic" },
            ".style-normal"            : { fontStyle: "normal" },

            // Text transforms
            ".transform-upper"         : { textTransform: "uppercase" },
            ".transform-lower"         : { textTransform: "lowercase" },
            ".transform-capital"       : { textTransform: "capitalize" },

            // Colors - Bootstrap's color system
            ".color-primary"           : { color: "#0d6efd" },
            ".color-secondary"         : { color: "#6c757d" },
            ".color-accent"            : { color: "#0d6efd" },
            ".color-success"           : { color: "#198754" },
            ".color-warning"           : { color: "#ffc107" },
            ".color-error"             : { color: "#dc3545" },
            ".color-info"              : { color: "#0dcaf0" },
            ".color-muted"             : { color: "#6c757d" },
            ".color-white"             : { color: "#ffffff" },

            // Background colors
            ".bg-primary"              : { backgroundColor: "#0d6efd" },
            ".bg-secondary"            : { backgroundColor: "#6c757d" },
            ".bg-accent"               : { backgroundColor: "#0d6efd" },
            ".bg-success"              : { backgroundColor: "#198754" },
            ".bg-warning"              : { backgroundColor: "#ffc107" },
            ".bg-error"                : { backgroundColor: "#dc3545" },
            ".bg-info"                 : { backgroundColor: "#0dcaf0" },
            ".bg-muted"                : { backgroundColor: "#6c757d" },

            // Special text types
            ".type-lead"               : { fontSize: "1.25rem", fontWeight: "300", lineHeight: "1.6", marginBottom: "1rem" },
            ".type-body"               : { fontSize: "1rem",    fontWeight: "400", lineHeight: "1.5", marginBottom: "1rem" },
            ".type-caption"            : { fontSize: "0.875rem",fontWeight: "400", lineHeight: "1.4", color: "#6c757d" },

            // Base elements
            "p"                        : { marginBottom: "1rem", fontSize: "1rem", lineHeight: "1.5" },
            "h1, h2, h3, h4, h5, h6"   : { marginBottom: "0.5rem", fontWeight: "500", lineHeight: "1.2" }
        }
    }

    css_rules__foundation() {
        return {
            ":host"                    : { fontFamily: "Helvetica Neue, Helvetica, Roboto, Arial, sans-serif" },

            // Type Scale
            ".type-mega"               : { fontSize: "3.75rem",  fontWeight: "300", lineHeight: "1.4", marginBottom: "0.5rem" },
            ".type-hero"               : { fontSize: "3.375rem", fontWeight: "300", lineHeight: "1.4", marginBottom: "0.5rem" },
            ".type-title"              : { fontSize: "3rem",     fontWeight: "300", lineHeight: "1.4", marginBottom: "0.5rem" },
            ".type-xl"                 : { fontSize: "2.625rem", fontWeight: "300", lineHeight: "1.4", marginBottom: "0.5rem" },
            ".type-lg"                 : { fontSize: "2.25rem",  fontWeight: "300", lineHeight: "1.4", marginBottom: "0.5rem" },
            ".type-md"                 : { fontSize: "1.875rem", fontWeight: "300", lineHeight: "1.4", marginBottom: "0.5rem" },
            ".type-sm"                 : { fontSize: "0.875rem", fontWeight: "400", lineHeight: "1.4", marginBottom: "0.5rem" },
            ".type-xs"                 : { fontSize: "0.75rem",  fontWeight: "400", lineHeight: "1.4", marginBottom: "0.5rem" },

            // Weights
            ".weight-thin"             : { fontWeight: "100" },
            ".weight-light"            : { fontWeight: "300" },
            ".weight-normal"           : { fontWeight: "400" },
            ".weight-medium"           : { fontWeight: "500" },
            ".weight-bold"             : { fontWeight: "700" },
            ".weight-heavy"            : { fontWeight: "900" },

            // Alignment
            ".align-start"             : { textAlign: "left" },
            ".align-center"            : { textAlign: "center" },
            ".align-end"               : { textAlign: "right" },

            // Style variations
            ".style-italic"            : { fontStyle: "italic" },
            ".style-normal"            : { fontStyle: "normal" },

            // Text transforms
            ".transform-upper"         : { textTransform: "uppercase" },
            ".transform-lower"         : { textTransform: "lowercase" },
            ".transform-capital"       : { textTransform: "capitalize" },

            // Colors - Foundation's color system
            ".color-primary"           : { color: "#1779ba" },
            ".color-secondary"         : { color: "#767676" },
            ".color-accent"            : { color: "#3adb76" },
            ".color-success"           : { color: "#3adb76" },
            ".color-warning"           : { color: "#ffae00" },
            ".color-error"             : { color: "#cc4b37" },
            ".color-info"              : { color: "#17a2b8" },
            ".color-muted"             : { color: "#8a8a8a" },
            ".color-white"             : { color: "#fefefe" },

            // Background colors
            ".bg-primary"              : { backgroundColor: "#1779ba" },
            ".bg-secondary"            : { backgroundColor: "#767676" },
            ".bg-accent"               : { backgroundColor: "#3adb76" },
            ".bg-success"              : { backgroundColor: "#3adb76" },
            ".bg-warning"              : { backgroundColor: "#ffae00" },
            ".bg-error"                : { backgroundColor: "#cc4b37" },
            ".bg-info"                 : { backgroundColor: "#17a2b8" },
            ".bg-muted"                : { backgroundColor: "#8a8a8a" },

            // Special text types
            ".type-lead"               : { fontSize: "125%", lineHeight: "1.6", marginBottom: "1rem" },
            ".type-body"               : { fontSize: "1rem", fontWeight: "400", lineHeight: "1.6", marginBottom: "1rem", textRendering: "optimizeLegibility" },
            ".type-caption"            : { fontSize: "0.875rem", fontWeight: "400", lineHeight: "1.4", color: "#8a8a8a" },

            // Base elements
            "p"                        : { marginBottom: "1rem", fontSize: "1rem", lineHeight: "1.6", textRendering: "optimizeLegibility" },
            "h1, h2, h3, h4, h5, h6"   : { marginBottom: "0.5rem", fontWeight: "500", lineHeight: "1.4" }
        }
    }

    css_rules__tailwind() {
        return {
            ":host"                    : { fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, Noto Sans, sans-serif" },

            // Type Scale
            ".type-mega"               : { fontSize: "8rem",     lineHeight: "1",   fontWeight: "800", marginBottom: "0.5rem" },
            ".type-hero"               : { fontSize: "6rem",     lineHeight: "1",   fontWeight: "800", marginBottom: "0.5rem" },
            ".type-title"              : { fontSize: "4.5rem",   lineHeight: "1",   fontWeight: "800", marginBottom: "0.5rem" },
            ".type-xl"                 : { fontSize: "3.75rem",  lineHeight: "1",   fontWeight: "800", marginBottom: "0.5rem" },
            ".type-lg"                 : { fontSize: "3rem",     lineHeight: "1",   fontWeight: "700", marginBottom: "0.5rem" },
            ".type-md"                 : { fontSize: "2.25rem",  lineHeight: "2.5", fontWeight: "700", marginBottom: "0.5rem" },
            ".type-sm"                 : { fontSize: "0.875rem", lineHeight: "1.25",                   marginBottom: "0.5rem" },
            ".type-xs"                 : { fontSize: "0.75rem",  lineHeight: "1.25",                   marginBottom: "0.5rem" },

            // Weights
            ".weight-thin"             : { fontWeight: "100" },
            ".weight-light"            : { fontWeight: "300" },
            ".weight-normal"           : { fontWeight: "400" },
            ".weight-medium"           : { fontWeight: "500" },
            ".weight-bold"             : { fontWeight: "700" },
            ".weight-heavy"            : { fontWeight: "900" },

            // Alignment
            ".align-start"             : { textAlign: "left" },
            ".align-center"            : { textAlign: "center" },
            ".align-end"               : { textAlign: "right" },

            // Style variations
            ".style-italic"            : { fontStyle: "italic" },
            ".style-normal"            : { fontStyle: "normal" },

            // Text transforms
            ".transform-upper"         : { textTransform: "uppercase" },
            ".transform-lower"         : { textTransform: "lowercase" },
            ".transform-capital"       : { textTransform: "capitalize" },

            // Colors - Tailwind's color system
            ".color-primary"           : { color: "#3b82f6" },
            ".color-secondary"         : { color: "#6b7280" },
            ".color-accent"            : { color: "#8b5cf6" },
            ".color-success"           : { color: "#10b981" },
            ".color-warning"           : { color: "#f59e0b" },
            ".color-error"             : { color: "#ef4444" },
            ".color-info"              : { color: "#3b82f6" },
            ".color-muted"             : { color: "#6b7280" },
            ".color-white"             : { color: "#ffffff" },

            // Background colors
            ".bg-primary"              : { backgroundColor: "#3b82f6" },
            ".bg-secondary"            : { backgroundColor: "#6b7280" },
            ".bg-accent"               : { backgroundColor: "#8b5cf6" },
            ".bg-success"              : { backgroundColor: "#10b981" },
            ".bg-warning"              : { backgroundColor: "#f59e0b" },
            ".bg-error"                : { backgroundColor: "#ef4444" },
            ".bg-info"                 : { backgroundColor: "#3b82f6" },
            ".bg-muted"                : { backgroundColor: "#6b7280" },

            // Special text types
            ".type-lead"               : { fontSize: "1.125rem", lineHeight: "1.75", fontWeight: "500" },
            ".type-body"               : { fontSize: "1rem",     lineHeight: "1.5",  fontWeight: "400" },
            ".type-caption"            : { fontSize: "0.875rem", lineHeight: "1.25", color: "#6b7280" },

            // Base elements
            "p"                        : { marginBottom: "1rem", fontSize: "1rem", lineHeight: "1.5" },
            "h1, h2, h3, h4, h5, h6"   : { marginBottom: "0.5rem", fontWeight: "600", lineHeight: "1.25" }
        }
    }

    css_rules__material_design() {
        return {
            ":host"                    : { fontFamily: "Roboto, Helvetica, Arial, sans-serif" },

            // Type Scale
            ".type-mega"               : { fontSize: "6rem",      letterSpacing: "-0.015625em", fontWeight: "300", lineHeight: "1.167", marginBottom: "0.5rem" },
            ".type-hero"               : { fontSize: "3.75rem",   letterSpacing: "-0.00833em",  fontWeight: "300", lineHeight: "1.2",   marginBottom: "0.5rem" },
            ".type-title"              : { fontSize: "3rem",      letterSpacing: "0em",         fontWeight: "400", lineHeight: "1.167", marginBottom: "0.5rem" },
            ".type-xl"                 : { fontSize: "2.125rem",  letterSpacing: "0.00735em",   fontWeight: "400", lineHeight: "1.235", marginBottom: "0.5rem" },
            ".type-lg"                 : { fontSize: "1.5rem",    letterSpacing: "0em",         fontWeight: "400", lineHeight: "1.334", marginBottom: "0.5rem" },
            ".type-md"                 : { fontSize: "1.25rem",   letterSpacing: "0.0075em",    fontWeight: "500", lineHeight: "1.6",   marginBottom: "0.5rem" },
            ".type-sm"                 : { fontSize: "0.875rem",  letterSpacing: "0.01071em",   fontWeight: "400", lineHeight: "1.43",  marginBottom: "0.5rem" },
            ".type-xs"                 : { fontSize: "0.75rem",   letterSpacing: "0.03333em",   fontWeight: "400", lineHeight: "1.66",  marginBottom: "0.5rem" },

            // Weights
            ".weight-thin"             : { fontWeight: "100" },
            ".weight-light"            : { fontWeight: "300" },
            ".weight-normal"           : { fontWeight: "400" },
            ".weight-medium"           : { fontWeight: "500" },
            ".weight-bold"             : { fontWeight: "700" },
            ".weight-heavy"            : { fontWeight: "900" },

            // Alignment
            ".align-start"             : { textAlign: "left" },
            ".align-center"            : { textAlign: "center" },
            ".align-end"               : { textAlign: "right" },

            // Style variations
            ".style-italic"            : { fontStyle: "italic" },
            ".style-normal"            : { fontStyle: "normal" },

            // Text transforms
            ".transform-upper"         : { textTransform: "uppercase", letterSpacing: "0.08333em" },
            ".transform-lower"         : { textTransform: "lowercase" },
            ".transform-capital"       : { textTransform: "capitalize" },

            // Colors - Material Design color system
            ".color-primary"           : { color: "#1976d2" },
            ".color-secondary"         : { color: "#9c27b0" },
            ".color-accent"            : { color: "#ff4081" },
            ".color-success"           : { color: "#2e7d32" },
            ".color-warning"           : { color: "#ed6c02" },
            ".color-error"             : { color: "#d32f2f" },
            ".color-info"              : { color: "#0288d1" },
            ".color-muted"             : { color: "rgba(0, 0, 0, 0.6)" },
            ".color-white"             : { color: "#ffffff" },

            // Background colors
            ".bg-primary"              : { backgroundColor: "#1976d2" },
            ".bg-secondary"            : { backgroundColor: "#9c27b0" },
            ".bg-accent"               : { backgroundColor: "#ff4081" },
            ".bg-success"              : { backgroundColor: "#2e7d32" },
            ".bg-warning"              : { backgroundColor: "#ed6c02" },
            ".bg-error"                : { backgroundColor: "#d32f2f" },
            ".bg-info"                 : { backgroundColor: "#0288d1" },
            ".bg-muted"                : { backgroundColor: "rgba(0, 0, 0, 0.6)" },

            // Special text types
            ".type-lead"               : { fontSize: "1.25rem",  letterSpacing: "0.0075em", fontWeight: "400", lineHeight: "1.6" },
            ".type-body"               : { fontSize: "1rem",     letterSpacing: "0.00938em", fontWeight: "400", lineHeight: "1.5" },
            ".type-caption"            : { fontSize: "0.75rem",  letterSpacing: "0.03333em", fontWeight: "400", lineHeight: "1.66", color: "rgba(0, 0, 0, 0.6)" },

            // Base elements
            "p"                        : { marginBottom: "1rem", fontSize: "1rem", letterSpacing: "0.00938em", lineHeight: "1.5" },
            "h1, h2, h3, h4, h5, h6"   : { marginBottom: "0.5rem", fontWeight: "400", lineHeight: "1.167" }
        }
    }
}