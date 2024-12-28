import Events__Utils from "../events/Events__Utils.mjs";
import Tag           from "./Tag.mjs";

export default class Web_Component extends HTMLElement {

    EVENT_NAME__COMPONENT_READY = 'webc::component-ready'

    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.channel   = null
        this.channels  = ['Web_Component']
        this.webc_id   = null
        this.webc_type = 'Web_Component'                         // todo: see if this is useful
        this.events_utils           = new Events__Utils()        // todo: look at removing this since this not widely used
        this.window_event_listeners = []                         // keep track of these events so that we can remove them all on disconnectedCallback
    }

    // static properties
    static get element_name() {
        return this.name.replace    (/_/g , '-')  // Replace underscores with hyphens
                        .replace    (/--/g, '-')  // make sure we only have one hyphen
                        .toLowerCase()            // Convert to lowercase
    }

    // static methods

    static add_to_body() {
        return this.create_element_add_to_body()
    }

    static create({inner_html=null, tag=null,...attributes}={}) {
        const element = document.createElement(this.element_name);        // Create a new element using the provided tag name
        for (const [attr, value] of Object.entries(attributes)) {         // // Iterate over the attributes object and set attributes on the element
            element.setAttribute(attr, value);
        }
        if (inner_html != null) {
            element.innerHTML = inner_html;
        }
        if (tag != null) {
            element.innerHTML = tag.html();
        }
        return element;
    }

    // todo: (see how is using this, and remove when not used) refactor to use the create() method above (since this is adding an element to to document body which is only one of the scenarios
    static create_element() {
        return document.createElement(this.element_name);
    }

    static create_element_add_to_body() {
        const element = this.create_element();
        return document.body.appendChild(element);
    }

    static define() {
        if (!customElements.get(this.element_name)) {
            customElements.define(this.element_name, this);
            return true; }
        return false;
    }

    // instance - connection and usually overridden methods

    async connectedCallback() {                        // todo see if any other methods should be async (of I should make them all async)
        try {
                  this.load_attributes    ()               // start by loading any attributes provided
            await this.apply_css          ()               // then apply css to the current dom

            await this.load_data          ()               // then load any data required
                  this.render             ()               // then render the core html elements (i.e. assign the inner_html)
            await this.add_web_components ()               // then add the web components that need the live dom to exist
                  this.add_event_listeners()               // then add the event listeners
                  this.add_event_handlers ()               // then add the event handlers
            await this.final_ui_changes()                  // use when needing to make final changes to the UI
            await this.component_ready()                   // use when needing to run code when the component is ready

                  this.channels.push(this.channel)                  // todo: legacy - review usage and see if the current patterns can handle this requirement better
                  this.add_event_listeners__web_component()         // todo: legacy - to remove, but first remove dependency from  WebC__Chat_Bot

            this.raise_event(this.EVENT_NAME__COMPONENT_READY)
        } catch (error) {
            console.error('Error in connectedCallback:', error);
            throw new Error(`connectedCallback failed: ${error.message}`);
        }
    }

    disconnectedCallback() {
        this.remove_event_handlers()                                // in case the parent component has extra events listeners to remove
        this.remove_window_event_listeners()                        // remove the events added via add_window_event_listener and add_event__on
        this.remove_event_listeners()                               // in case the parent component has extra events handlers to remove
        this.remove_event_listeners__webc_component()               // todo: legacy - to remove

    }

    load_attributes() {
        this.channel  = this.getAttribute('channel') || this.random_id('webc_channel_')
        this.webc_id  = this.getAttribute('webc_id') || this.random_id('webc_id_')
    }

    render() {                                  // override this method in the child class to render the component (called from connectedCallback)
        let html = this.html() || ''            // get the html of the component
        if (html instanceof Tag) {              // if the html is an instance of Tag
            html = html.html()                  //   then get the html of the Tag
        }
        this.set_inner_html(html)               // first set the html
    }
    async refresh_ui() {
              this.remove_event_handlers   ()                    // Remove existing event handlers
              this.render                  ()                    // Re-render the component's HTML
        await this.add_web_components()                    // Re-add any child web components
              this.add_event_handlers      ()                    // Re-attach event handlers
        await this.final_ui_changes  ()                    // Apply any final UI adjustments
        await this.component_ready()
              this.raise_event__component_ready()
    }

    async apply_css             () {}                   // override to apply css to the current dom
    async load_data             () {}                   // override to trigger the load any data required
          html                  () {}                   // override to return the html of the component
          add_event_listeners   () {}                   // override to set the DOM event listeners
          add_event_handlers    () {}                   // override to set the event handlers
    async add_web_components    () {}                   // override to add web components to the current component
    async final_ui_changes      () {}                   // override to make final changes to the UI
    async component_ready       () {}                   // override to run code when the component is ready
          remove_event_handlers () {}                   // override to remove event handlers
          remove_event_listeners() {}                   // override to remove event listeners
    // EVENT helper methods

    add_window_event_listener(eventType, listener) {
        const bound_listener = listener.bind(this);                                 // Automatically bind 'this' to the listener
        window.addEventListener(eventType, bound_listener);                         // Add the event listener to the window object
        this.window_event_listeners.push({ eventType, listener: bound_listener });  // Store the bound listener for cleanup
    }

    add_event__on(event_type, selector, callback, params = {}) {
        const element        = this.query_selector(selector);                                            // Find the element using the selector
        this.add_event__to_element__on(event_type, element, callback, params);                           // Add the event listener to the element
    }

    add_event__on_click(selector, callback, params = {}) {
        this.add_event__on('click', selector, callback, params);
    }

    add_event__to_element__on(event_type, element, callback, params = {}) {
        const bound_listener = (event) => callback.call(this, { ...params, event });                       // Create a bound listener that wraps the callback with params
        element.addEventListener(event_type, bound_listener);                                              // Attach the click event listener
        this.window_event_listeners.push({ eventType: event_type,  element,  listener: bound_listener, }); // Store the listener for cleanup
    }

    remove_window_event_listeners() {
        this.window_event_listeners.forEach(({ eventType, element, listener }) => {
            if (element) {
                element.removeEventListener(eventType, listener);                   // Remove DOM element event listeners
            } else {
                window.removeEventListener(eventType, listener);                    // Remove global window event listeners
            }
        });
        this.window_event_listeners = [];                                           // Clear the stored listeners array
    }

    // events methods
    raise_event(event_name, event_detail) {
        const options      =  { bubbles: false, detail: event_detail}
        const custom_event = new CustomEvent(event_name, options)
        this.dispatchEvent(custom_event);
        return custom_event
    }

    raise_event_global(event_name, event_detail={}) {
        const options      =  { bubbles: true, composed: true, detail: event_detail}
        const custom_event = new CustomEvent(event_name, options)
        this.dispatchEvent(custom_event);
        return custom_event
    }

    raise_event__component_ready() {
        this.raise_event(this.EVENT_NAME__COMPONENT_READY)
    }

    async wait_for_event(event_name, timeout) {
        const timeout_value = timeout || 100
        const current_class = this.constructor.name; // Get the name of the current class
        const timeout_message = `[${current_class}] ${event_name} event did not fire within the expected timeout value: ${timeout_value}ms.`;

        return await new Promise((resolve, reject) => {
            const on_timeout       = () => { reject(new Error(timeout_message)); }
            const timeout_function = setTimeout(on_timeout, timeout_value);
            const on_event         = (event) => { clearTimeout(timeout_function); resolve(event.detail); }
            this.addEventListener(event_name, on_event, { once: true });
        });
    }
    async wait_for__component_ready(timeout) {
        await this.wait_for_event(this.EVENT_NAME__COMPONENT_READY, timeout)
    }

    // other methods // todo organise these methods in a logical way
    add_adopted_stylesheet(stylesheet) {
        const currentStylesheets = this.shadowRoot.adoptedStyleSheets;
        this.shadowRoot.adoptedStyleSheets = [...currentStylesheets, stylesheet];
    }

    add_event_listener(selector, event_name, callback) {
        this.query_selector(selector).addEventListener(event_name, callback)
    }

    add_web_component(WebC_Class, ...attributes) {
        const child_component = WebC_Class.create(...attributes)        // calls static method create from the Web Component class
        this.shadow_root_append(child_component)                        // adds it as a child to the current WebC
        return child_component                                          // returns the instance created of WebC_Class
    }

    add_web_component_to(selector, WebC_Class, ...attributes) {
        const child_component = WebC_Class.create(...attributes)        // calls static method create from the Web Component class
        this.query_selector(selector).appendChild(child_component)      // adds it as a child to the current WebC
        return child_component                                          // returns the instance created of WebC_Class
    }

    append_child(WebC_Class, ...attributes) {
        const child_component = WebC_Class.create(...attributes)        // calls static method create from the Web Component class
        this.appendChild(child_component)                               // adds it as a child to the current WebC
        return child_component                                          // returns the instance created of WebC_Class
    }


    // root_element() {
    //     return null
    // }

    // todo: refactor stylesheets to separate class
    add_css_rules(css_rules) {
        const styleSheet  = this.create_stylesheet_from_css_rules(css_rules) // add new style sheet to adopted stylesheets for the shadow root
        this.add_adopted_stylesheet(styleSheet)
        return styleSheet
    }

    all_css_rules() {
        const cssObject = {}
        for (let stylesheet of this.stylesheets()) {
            const cssRules = stylesheet.cssRules;
            for (let rule of cssRules) {
                cssObject[rule.selectorText] = rule.cssText; }}
        return cssObject
    }

    append_inner_html(value) {        
        this.shadowRoot.innerHTML  += value
    }

    inner_html() {
        return this.shadowRoot.innerHTML 
    }
    
    query_selector(selector) {
        return this.shadow_root().querySelector(selector)
    }

    query_selector_all(selector) {
        return this.shadow_root().querySelectorAll(selector)
    }

    parent_element() {
        return this.parentElement
    }

    random_id(prefix='random') {
        const random_part = Math.random().toString(36).substring(2, 7); // Generate a random string.
        return `${prefix}_${random_part}`;
    }

    random_uuid() {
        return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
            (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
        );
    }


    set_inner_html(inner_html) {
        this.shadowRoot.innerHTML = inner_html
    }

    shadow_root() {
        return this.shadowRoot
    }

    shadow_root_append(child) {
        return this.shadowRoot.appendChild(child)
    }

    stylesheets(include_root=true, include_shadow=true) {
        const all_stylesheets =[]
        if (include_root) {
            all_stylesheets.push(...Array.from(this.shadowRoot.styleSheets)) }
        if (include_shadow) {
            all_stylesheets.push(...this.shadowRoot.adoptedStyleSheets) }
        // this is required for Safari which was duplicating the entries
        return all_stylesheets.filter((stylesheet, index, self) => index === self.findIndex(s => s === stylesheet))
    }

    async wait_for(duration=1000) {
        return new Promise(resolve => setTimeout(resolve, duration));
    }
    // this is the previous version of create_stylesheet_from_css_rules, after testing on all devices and no side effects noticed, this can be removed
    // create_stylesheet_from_css_rules(css_rules) {
    //     const styleSheet = new CSSStyleSheet();
    //     Object.entries(css_rules).forEach(([css_selector, css_properties]) => {        // Iterate over each key (selector) in cssProperties
    //         const css_init          = `${css_selector} {}`;                                     // note: it looks like at the moment there isn't another way to create an empty CSSStyleRule and populate it
    //         const rules_length      = styleSheet.cssRules.length                                // get size of css rules
    //         const insert_position   = styleSheet.insertRule(css_init, rules_length);            // so that we can create a new one at the end
    //         const cssRule           = styleSheet.cssRules[insert_position];                     // get a reference to the one we added
    //         this.populate_rule(cssRule, css_properties);                                        // populate new css rule with provided css properties
    //     });
    //     return styleSheet
    // }
    //
    // populate_rule(css_rule, css_properties) {
    //     for (let prop_name in css_properties) {
    //         const css_prop_name = prop_name.replace(/([A-Z])/g, '-$1').toLowerCase();           // Convert camelCase to kebab-case
    //         const css_prop_value = css_properties[prop_name]                                    // get css prop value
    //         css_rule.style.setProperty(css_prop_name, css_prop_value);                          // set property in css_rule
    //     }
    // }

    create_stylesheet_from_css_rules(css_rules) {
        const styleSheet = new CSSStyleSheet();
        this.process_rules(styleSheet, css_rules);
        return styleSheet;
    }

    process_rules(styleSheet, rules, parentRule = null) {
        if (!rules) { return}
        Object.entries(rules).forEach(([selector, properties]) => {
            if (typeof properties !== 'object') {
                // Skip if properties is not an object
                return;
            }
            if (selector.startsWith('@')) {
                // Handle at-rules like @keyframes
                const ruleText = `${selector} { }`;
                const insertIndex = parentRule ? parentRule.cssRules.length : styleSheet.cssRules.length;
                if (parentRule && 'insertRule' in parentRule) {
                    parentRule.insertRule(ruleText, insertIndex);
                    const atRule = parentRule.cssRules[insertIndex];
                    this.process_rules(styleSheet, properties, atRule);
                } else {
                    styleSheet.insertRule(ruleText, insertIndex);
                    const atRule = styleSheet.cssRules[insertIndex];
                    this.process_rules(styleSheet, properties, atRule);
                }
            } else {
                if (parentRule && parentRule.type === CSSRule.KEYFRAMES_RULE) {
                    // Handle keyframe selectors like "0%", "100%"
                    let ruleText = `${selector} { }`;
                    parentRule.appendRule(ruleText);
                    const keyframeRule = parentRule.findRule(selector);
                    this.populate_rule(keyframeRule, properties);
                } else {
                    // Handle regular selectors
                    const ruleText = `${selector} { }`;
                    const insertIndex = parentRule ? parentRule.cssRules.length : styleSheet.cssRules.length;
                    if (parentRule && 'insertRule' in parentRule) {
                        parentRule.insertRule(ruleText, insertIndex);
                        const cssRule = parentRule.cssRules[insertIndex];
                        this.populate_rule(cssRule, properties);
                    } else {
                        styleSheet.insertRule(ruleText, insertIndex);
                        const cssRule = styleSheet.cssRules[insertIndex];
                        this.populate_rule(cssRule, properties);
                    }
                }
            }
        });
    }

    populate_rule(cssRule, properties) {
        if (cssRule.type === CSSRule.STYLE_RULE || cssRule.type === CSSRule.KEYFRAME_RULE) {
            for (let propName in properties) {                                                             // Handle style and keyframe rules
                const cssPropName = propName.replace(/([A-Z])/g, '-$1').toLowerCase();
                const cssPropValue = properties[propName];
                cssRule.style.setProperty(cssPropName, cssPropValue);
            }
        }
    }

    // // todo: legacy: look at who is using this and remove it usage (new code should use add_window_event_listener)
    add_event_listeners__web_component() {                              // todo: see if there is a better way to do this (ie. invoke the add_event_listeners() method from this
        this.events_utils.events_receive.add_event_listener('invoke' , this.channel, this.on_invoke      );
    }
    // // todo: legacy: look at who is using this and remove it usage (new code should use add_window_event_listener)
    remove_event_listeners__webc_component() {
        this.events_utils.events_receive.remove_all_event_listeners()
    }
    on_invoke = (event) => {
        if (this.webc_id ===event.webc_id) {                                                    // only react to events that are sent to this specific webc_id
            let event_data = event.event_data                                                   // get the event_data
            let callback   = event.callback                                                     // get the callback
            if (typeof this[event_data.method] === 'function') {                                // check if the method defined in the method exists in this
                const result = this[event_data.method](...Object.values(event_data.params));    // if so execute it and capture the return value
                if (typeof callback === 'function') {                                           // check if the callback is a function
                    callback(result)                                                            // if it is defined, invoke it with the return value of the function execution
                }
            }
        }
    }

    console_log__caller(index=3){
        const err = new Error();
        const stack = err.stack.split('\n');
        console.log(stack[index]);
    }
    // instance methods
}

