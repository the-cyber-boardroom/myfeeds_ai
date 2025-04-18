from datetime                                       import datetime
from myfeeds_ai.personas.actions.My_Feeds__Persona  import My_Feeds__Persona
from osbot_utils.type_safe.Type_Safe                import Type_Safe

PATH__PUBLIC_DATA           = '/public-data/personas/'
PATH__PERSONA_DIGEST_IMAGE  = "/personas/persona-digest-image?persona_type="

class My_Feeds__Persona__Html_Page(Type_Safe):
    persona: My_Feeds__Persona = None


    def actions_config(self):
        return [
            {
                "id"    : "current-digest-articles",
                "label" : "Current Digest Articles",
                "class" : "refresh-btn",
                "url"   : "/hacker-news-articles/digest-articles-html-page"
            },
            {
                "id"    : "all-articles-timeline",
                "label" : "All Articles Timeline",
                "class" : "refresh-btn",
                "url"   : "/public-data/hacker-news/latest/feed-timeline.mgraph.png"
            },
            {
                "id"     : "mvp-myfeeds",
                "label"  : "Blog site (mvp.MyFeeds.ai)",
                "class"  : "refresh-btn",
                "url"    : "https://mvp.myfeeds.ai/"
            },
            {
                "id"     : "dev-myfeeds",
                "label"  : "API (dev.myfeeds.ai)",
                "class"  : "refresh-btn",
                "url"    : "https://dev.myfeeds.ai/"
            },
        ]

    def create(self) -> str:

        persona_data = self.persona.data().json()

        # Extract key information
        persona_type = persona_data.get('persona_type', 'Unknown')
        description = persona_data.get('description', 'No description available.')
        description_hash = persona_data.get('description__hash', '')

        # Get the current date in a readable format
        current_date = datetime.now().strftime('%B %d, %Y')

        # Create a list of resources from the path fields
        resources = []

        # Primary resource - the HTML digest
        if persona_data.get('path__persona__digest__html'):
            resources.append({
                'title': 'Cybersecurity Digest (HTML)',
                'description': 'View your complete personalized cybersecurity digest with executive summary, prioritized articles, and strategic implications tailored for your role.',
                'path': PATH__PUBLIC_DATA + persona_data.get('path__persona__digest__html'),
                'is_primary': True
            })

        # Regular resources
        if persona_data.get('path__persona__digest'):
            resources.append({
                'title': 'Digest JSON Data',
                'description': 'Raw JSON data for your personalized digest with all structured information.',
                'path': PATH__PUBLIC_DATA + persona_data.get('path__persona__digest'),
                'is_primary': False
            })

        if persona_data.get('path__persona__entities__png'):
            resources.append({
                'title': 'Entities Visualization',
                'description': 'Visual representation of key entities relevant to your role and their relationships.',
                'path': PATH__PUBLIC_DATA + persona_data.get('path__persona__entities__png'),
                'is_primary': False
            })

        if persona_data.get('path__persona__entities'):
            resources.append({
                'title': 'Entities Data',
                'description': 'Structured data of relevant entities to your role in JSON format.',
                'path': PATH__PUBLIC_DATA + persona_data.get('path__persona__entities'),
                'is_primary': False
            })

        if persona_data.get('path__persona__entities__tree_values'):
            resources.append({
                'title': 'Entities Tree',
                'description': 'Hierarchical text representation of entities and their relationships.',
                'path': PATH__PUBLIC_DATA + persona_data.get('path__persona__entities__tree_values'),
                'is_primary': False
            })

        if persona_data.get('path__persona__articles__connected_entities'):
            resources.append({
                'title': 'Connected Articles & Entities',
                'description': 'Mapping between articles and connected entities relevant to your role.',
                'path': PATH__PUBLIC_DATA + persona_data.get('path__persona__articles__connected_entities'),
                'is_primary': False
            })

        if persona_data.get('path__now'):
            resources.append({
                'title': 'Current Persona Data',
                'description': 'Your current persona configuration and details in JSON format.',
                'path': PATH__PUBLIC_DATA + persona_data.get('path__now'),
                'is_primary': False
            })

        # if persona_data.get('path__persona__latest'):
        #     resources.append( {'title'      : 'Latest Persona Data',
        #                        'description': 'Most up-to-date version of your persona configuration.',
        #                        'path'       : PATH__PUBLIC_DATA + persona_data.get('path__persona__latest'),
        #                        'is_primary' : False })
        resources.append( {'title'      : 'Persona Digest Image',
                           'description': 'The autogenerated image used on the blog entry for the current digest',
                           'path'       : PATH__PERSONA_DIGEST_IMAGE + self.persona.persona_type.value,
                           'is_primary' : False })




        # Format title nicely
        formatted_title = persona_type.replace('-', ' ').replace('_', ' ').title()
        if formatted_title.lower().startswith('exec'):
            formatted_title = formatted_title.replace('Exec ', '')

        # Generate resource cards HTML
        resource_cards_html = ""
        for resource in resources:
            primary_class = "primary-resource" if resource.get('is_primary') else ""
            resource_cards_html += f"""
            <div class="resource-card {primary_class}">
                <h3>{resource['title']}</h3>
                <p>{resource['description']}</p>
                <a href="{resource['path']}" class="resource-link" target="_blank">View Resource</a>
            </div>
            """

        # Generate complete HTML
        html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{formatted_title} Data</title>
        <style>
            :root {{
                --primary: #2c3e50;
                --secondary: #3498db;
                --accent: #e74c3c;
                --light: #ecf0f1;
                --dark: #2c3e50;
                --success: #2ecc71;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            
            header {{
                background-color: var(--primary);
                color: white;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            
            h1 {{
                margin: 0;
                font-size: 2.2em;
            }}
            
            .date-display {{
                font-size: 1.1em;
                opacity: 0.9;
                margin-top: 5px;
            }}
            
            .description {{
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                border-left: 4px solid var(--secondary);
            }}
            
            .resources {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .resource-card {{
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                transition: transform 0.2s, box-shadow 0.2s;
                border-top: 4px solid var(--secondary);
            }}
            
            .resource-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
            }}
            
            .resource-card h3 {{
                margin-top: 0;
                color: var(--dark);
                font-size: 1.2em;
            }}
            
            .resource-card p {{
                font-size: 0.9em;
                color: #666;
                margin-bottom: 15px;
            }}
            
            .resource-link {{
                display: inline-block;
                background-color: var(--secondary);
                color: white;
                padding: 8px 16px;
                text-decoration: none;
                border-radius: 4px;
                font-weight: 500;
                transition: background-color 0.2s;
            }}
            
            .resource-link:hover {{
                background-color: #2980b9;
            }}
            
            .primary-resource {{
                grid-column: span 2;
                border-top-color: var(--success);
            }}
            
            .primary-resource .resource-link {{
                background-color: var(--success);
            }}
            
            .primary-resource .resource-link:hover {{
                background-color: #27ae60;
            }}
            
            footer {{
                text-align: center;
                margin-top: 40px;
                padding: 20px;
                color: #666;
                font-size: 0.9em;
                border-top: 1px solid #ddd;
            }}
            
            .persona-details {{
                display: flex;
                justify-content: space-between;
                margin-bottom: 30px;
            }}
            
            .persona-info {{
                flex: 2;
                padding-right: 20px;
            }}
            
            .persona-actions {{
                flex: 1;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }}
            
            .refresh-btn {{
                display: block;
                width: 100%;
                padding: 10px;
                background-color: var(--success);
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 1em;
                cursor: pointer;
                margin-bottom: 10px;
                transition: background-color 0.2s;
            }}
            
            .refresh-btn:hover {{
                background-color: #27ae60;
            }}
            
            .hash-info {{
                font-family: monospace;
                font-size: 0.8em;
                color: #666;
                background-color: #f0f0f0;
                padding: 5px;
                border-radius: 4px;
                margin-top: 15px;
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>{formatted_title} Data</h1>
            <div class="date-display">{current_date}</div>
        </header>
        
        <div class="persona-details">
            <div class="persona-info">
                <div class="description">
                    <h2>Persona Overview</h2>
                    <p>{description}</p>
                    <div class="hash-info">Persona Hash: {description_hash}</div>
                </div>
            </div>
            { self.generate_article_resources_panel()}            
        </div>
        
        <h2>Persona Resources</h2>
        
        <div class="resources">
            {resource_cards_html}
        </div>
        
        <footer>
            <p>Generated on {current_date} | Persona Type: {persona_type}</p>
        </footer>
    </body>
    </html>
        """

        return html

    def generate_article_resources_panel(self):
        html = '<div class="persona-actions">\n'
        html += '    <h3>Article Resources</h3>\n'

        for action in self.actions_config():
            button_id = action.get('id', '')
            label = action.get('label', 'Action')
            css_class = action.get('class', 'refresh-btn')
            message = action.get('message', 'Action clicked')
            js_action = action.get('action', '')
            url = action.get('url', '')

            # Generate onclick attribute based on provided parameters
            if url:
                # For URLs, use window.open to open in a new tab
                escaped_url = url.replace("'", "\\'")
                onclick = f"window.open('{escaped_url}', '_blank')"
            elif js_action:
                onclick = f"{js_action}()"
            else:
                # Fallback to alert if no URL or action is provided
                escaped_message = message.replace("'", "\\'") if message else "No URL specified"
                onclick = f"alert('{escaped_message}')"

            html += f'    <button id="{button_id}" class="{css_class}" onclick="{onclick}">{label}</button>\n'

        html += '</div>'
        return html
