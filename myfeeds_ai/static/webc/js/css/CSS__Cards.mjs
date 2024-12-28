export default class CSS__Cards {
    constructor(target_element) {
        this.target_element = target_element
    }

    apply_framework() {
        if (this.target_element) {
            this.target_element.add_css_rules(this.css_rules__standard())
        }
    }

    css_rules__standard() {
        return {
            // Base card container
            ".card": {
                display: "flex",
                flexDirection: "column",
                position: "relative",
                minWidth: "0",
                wordWrap: "break-word",
                backgroundColor: "#fff",
                border: "1px solid rgba(0,0,0,.125)",
                borderRadius: "0.375rem",
                boxShadow: "0 2px 4px rgba(0,0,0,.05)"
            },

            // Card header
            ".card-header": {
                padding: "1rem",
                marginBottom: "0",
                backgroundColor: "rgba(0,0,0,.03)",
                borderBottom: "1px solid rgba(0,0,0,.125)",
                borderTopLeftRadius: "calc(0.375rem - 1px)",
                borderTopRightRadius: "calc(0.375rem - 1px)"
            },

            // Card body - main content area
            ".card-body": {
                flex: "1 1 auto",
                padding: "1rem"
            },

            // Card footer
            ".card-footer": {
                padding: "1rem",
                backgroundColor: "rgba(0,0,0,.03)",
                borderTop: "1px solid rgba(0,0,0,.125)",
                borderBottomLeftRadius: "calc(0.375rem - 1px)",
                borderBottomRightRadius: "calc(0.375rem - 1px)"
            },

            // Card title and subtitle
            ".card-title": {
                marginBottom: "0.5rem",
                fontSize: "1.25rem",
                fontWeight: "500",
                lineHeight: "1.2"
            },

            ".card-subtitle": {
                marginTop: "-0.375rem",
                marginBottom: "0",
                color: "#6c757d"
            },

            // Card text
            ".card-text": {
                marginTop: "0",
                marginBottom: "1rem"
            },

            ".card-text:last-child": {
                marginBottom: "0"
            },

            // Card image
            ".card-img": {
                width: "100%",
                borderRadius: "calc(0.375rem - 1px)"
            },

            ".card-img-top": {
                width: "100%",
                borderTopLeftRadius: "calc(0.375rem - 1px)",
                borderTopRightRadius: "calc(0.375rem - 1px)"
            },

            ".card-img-bottom": {
                width: "100%",
                borderBottomLeftRadius: "calc(0.375rem - 1px)",
                borderBottomRightRadius: "calc(0.375rem - 1px)"
            },

            // Card image overlay
            ".card-img-overlay": {
                position: "absolute",
                top: "0",
                right: "0",
                bottom: "0",
                left: "0",
                padding: "1rem",
                borderRadius: "calc(0.375rem - 1px)"
            },

            // Horizontal layout
            ".card-horizontal": {
                flexDirection: "row"
            },

            ".card-horizontal .card-img": {
                width: "30%",
                borderTopRightRadius: "0",
                borderBottomLeftRadius: "calc(0.375rem - 1px)"
            },

            // Card groups
            ".card-group": {
                display: "flex",
                flexFlow: "row wrap"
            },

            ".card-group > .card": {
                flex: "1 0 0%",
                margin: "0.5rem"
            },

            // Card deck (grid-based layout)
            ".card-deck": {
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
                gap: "1rem",
                padding: "1rem"
            },

            // Utility classes for cards
            ".card-borderless": {
                border: "none"
            },

            ".card-shadowless": {
                boxShadow: "none"
            },

            // Hover effect
            ".card-hover": {
                transition: "transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out"
            },

            ".card-hover:hover": {
                transform: "translateY(-3px)",
                boxShadow: "0 4px 8px rgba(0,0,0,.1)"
            }
        }
    }
}