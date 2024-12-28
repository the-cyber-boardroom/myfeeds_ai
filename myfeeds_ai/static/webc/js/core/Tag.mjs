export default class Tag {
    constructor({tag: tag = 'tag', id=null, 'class': class_value=null , attributes={}, value=null, ...kwargs}={}) {
        this.tag            = tag                                 // needs to be first some since it is used by others (like in this.generate_random_id)
        this.attributes     = { ...attributes, ...kwargs };
        this.class          = class_value
        this.element_dom    = null
        this.element_parent = null
        this.elements       = [];
        this.html_config    = this.default_html_config();         // set default html config
        this.id             = id
        this.parent_dom     = null
        this.styles         = this.default_styles();              // set default styles
        this.value          = value
    }

    add(target) {
        if (Array.isArray(target)) {
            for (let element of target) {       // If the argument is an array, iterate over it and add each element
                this.add_element(element);}
        } else {
            this.add_element(target); }         // If the argument is a single element, add it directly
        return this;
    }

    add_class(class_name) {
        if (this.class) {
            this.class += ` ${class_name}`
        } else {
            this.class = class_name
        }
        return this
    }

    add_element(element) {
        element.element_parent = this
        this.elements.push(element)
        return this
    }

    add_elements(...elements) {
        for(let element of elements){
            element.element_parent = this
            this.add_element(element)
        }
        return this
    }

    clear_elements() {
        this.elements = []
    }

    clone({id=null, ...kwargs}={}) {
        const prototype = Object.getPrototypeOf(this)
        const obj       = Object.create(prototype)
        Object.assign(obj, this);                                   // clone this object
        Object.assign(obj, kwargs);                                 // except
        obj.html_config = { ...this.html_config   }                 //   - html_config (create a copy of the current html_config object)
        obj.elements    = []                                        //   - elements    (i.e. the tag children)
        obj.id          = id                                        //   - id          (reset id or set to the provided value)
        obj.styles      = { ...this.styles        }                 //   - styles      (create a copy of the current styles object)
        return obj
    }

    default_html_config() { return { include_id               : true ,
                                     include_tag              : true ,
                                     include_end_tag          : true ,
                                     indent_before_last_tag   : true ,
                                     new_line_before_elements : true ,
                                     new_line_after_final_tag : true ,
                                     trim_final_html_code     : false}}

    default_styles() { return { background_color: null,
                                border          : null,
                                bottom          : null,
                                left            : null,
                                margin          : null,
                                overflow        : null,
                                padding         : null,
                                position        : null,
                                right           : null,
                                top             : null,
                                width           : null,
                                z_index         : null}}

    dom() {
        return this.element_dom
    }

    dom_add() {
        return this.dom_add_to_element(document.body)
    }

    dom_add_to_id(tag_id){
        const element = document.getElementById(tag_id)
        return this.dom_add_to_element(element)
    }

    //todo: solve bug that happens when id is not set
    dom_add_to_element(dom_element) {
        if (dom_element && this.dom() === null) {
            dom_element.insertAdjacentHTML('beforeend', this.html());
            this.element_dom = document.getElementById(this.id)
            this.parent_dom  = dom_element
            return true
        }
        return false
    }

    // todo: see if this is still needed
    dom_add_class(className, styles) {
          let styleString = '';
          for (const property in styles) {
            // Convert camelCase to kebab-case
            const kebabProperty = property.replace(/([a-z0-9])([A-Z])/g, '$1-$2').toLowerCase();
            styleString += `${kebabProperty}: ${styles[property]}; `;
          }
          const style = document.createElement('style');
          document.head.appendChild(style);
          style.sheet.insertRule(`.${className} { ${styleString} }`, 0);
    }

    dom_apply_styles() {
        this.dom_set_styles(this.styles)
        return self
    }

    dom_create() {
        var parser = new DOMParser();
        var doc = parser.parseFromString(this.html(), 'text/html');
        return doc.body.firstChild;
    }

    dom_set_style(property, value) {
        if (this.dom()) {
            this.dom().style[property] = value;
        }
        return this
    }

    dom_set_styles(styles) {
        for (let property in styles) {
            if (styles.hasOwnProperty(property)) {
                this.dom_set_style(property, styles[property])
            }
        }
        return this
    }
    dom_styles(){
        let style = window.getComputedStyle(this.dom());
        let styleObject = {};

        // Iterate over all the properties
        for (let i = 0; i < style.length; i++) {
            let prop = style[i];
            let value = style.getPropertyValue(prop);
            styleObject[prop] = value;
        }

        return styleObject;
    }

    dom_parent() {                      // todo: see if this is still needed
        return this.parent_dom
    }

    dom_remove() {
        const dom_element = this.dom()
        if (dom_element) {
            dom_element.remove()
            this.element_dom = null
            return this.dom() === null
        }
        return false

    }

    generate_random_id() {
        const random_part = Math.random().toString(36).substring(2, 7); // Generate a random string.
        return `${this.tag.toLowerCase()}_${random_part}`;
    }

    html(depth=0) {
        let attributes  = '';
        const attributes_string = this.html_render_extra_attributes()
        const style_string      = this.html_render_styles()

        if (style_string.length > 0) {
            attributes += ` style="${style_string}"`;
        }

        if (this.class) {
            attributes += ` class="${this.class}"`
        }

        if (attributes_string.length > 0) {
            attributes += ` ${attributes_string}`
        }

        // Close the opening tag, insert inner HTML, and close the tag
        const indent = ' '.repeat(depth * 4)
        let html = ''
        if (this.html_config.include_tag) {
            html = indent + `<${this.tag}`
            if (this.html_config.include_id && this.id) {
                html += ` id="${this.id}"` }

            html += attributes
            if (this.html_config.include_end_tag) {
                html += '>' }
            else {
                html += '/>' }
        }
        if (this.html_config.include_end_tag) {
            if (this.value != null) {                                   // when value is set, use it for the inner_html value
                //html += this.value
                html += this.html_escape(this.value)                   // breaking change where now all values are html escaped by default
            }
            else {
                if (this.html_config.new_line_before_elements) {
                    html += '\n' }
                html += this.inner_html(depth)
                if (this.html_config.indent_before_last_tag) {
                    html += indent
                }
            }
            if (this.html_config.include_tag) {
                    html += `</${this.tag}>`; }
        }
        if (this.html_config.new_line_after_final_tag) {
                    html += '\n' }
        if (this.html_config.trim_final_html_code){
            return html.trim()
        }
        else {
            return html }
    }

    html_escape(unsafe_string) {
        if (unsafe_string === null || unsafe_string === undefined)              // Handle null/undefined values
            return '';
        const div          = document.createElement('div');                     // Create temporary DOM element
        div.textContent    = String(unsafe_string);                             // Coerce to string & escape chars
        const escaped_html = div.innerHTML;                                     // Get escaped HTML entities string
        return escaped_html;                                                    // Return string safe for innerHTML
    }

    html_render_extra_attributes() {
        let extra_attributes = ''
        for (const key in this.attributes) {
            if (this.attributes.hasOwnProperty(key)) {
                const value = this.attributes[key]
                if (value === null) {                                    // special case where attributes that have the value of null are added with no value (which is sometimes needed in html attributes)
                    extra_attributes += `${key} `
                } else {
                    extra_attributes += `${key}="${value}" ` }}}
        return extra_attributes.trim()
    }
    html_render_styles() {
        let style_string = ''
        if (this.styles && Object.keys(this.styles).length) {
            // Construct the style attribute value
            for (const key in this.styles) {
                if (this.styles.hasOwnProperty(key) && this.styles[key]) {
                    const styleKey = key.replace(/([A-Z])/g, '-$1').toLowerCase();      // Convert camelCase to kebab-case for CSS properties
                    style_string += `${styleKey}: ${this.styles[key]}; `;
                }
            }
        }
        // Trim the last space and append the style attribute to the HTML string
        return style_string.trim();
    }
    inner_html(depth=0) {
        var html = ''
        for (const index in this.elements) {
            const element = this.elements[index]
            html += element.html(depth+1)
        }
        return html
    }

    parent() {
        return this.element_parent
    }
    set_style(key, value) {
        this.styles[key] = value
        return this
    }

    set_styles(key_values) {
        for (var key in key_values) {
            const value = key_values[key]
            this.set_style(key,value)
        }
        return this
    }

    with_id(id) {
        if (this.id === id) return this

        if (this.elements) {                            // Search through child elements
            for (const child of this.elements) {
                const found = child.with_id(id)
                if (found) return found
            }
        }
        return null
    }
}

// todo: add method to get all css styles and for some specific class
// const className = '.your-class';
// const sheets = document.styleSheets;
// let rulesList = [];
//
// for (let i = 0; i < sheets.length; i++) {
//   const rules = sheets[i].rules || sheets[i].cssRules;
//   for (let j = 0; j < rules.length; j++) {
//     const rule = rules[j];
//     if (rule.type === CSSRule.STYLE_RULE && rule.selectorText.includes(className)) {
//       rulesList.push(rule.cssText);
//     }
//   }
// }
//
// console.log(rulesList);

// for the code above to work the crossOrigin attribute needs to be set to anonymous
// <link rel="stylesheet" href="https://code.jquery.com/qunit/qunit-2.20.0.css" crossOrigin = "anonymous">