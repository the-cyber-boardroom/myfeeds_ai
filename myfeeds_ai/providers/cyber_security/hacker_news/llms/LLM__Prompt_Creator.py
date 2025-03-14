from osbot_utils.type_safe.Type_Safe import Type_Safe


class Schema__LLM__Prompt_Data(Type_Safe):
    llm_model: str

class LLM__Prompt_Creator(Type_Safe):
    prompt_data : Schema__LLM__Prompt_Data

    def prompt(self, text):
        target_model = self.prompt_data.llm_model

        content_prompt = """You are a comprehensive knowledge extractor that maps entities into a rich semantic network.
                           For each entity:
                           1. Identify its core essence and domain classifications
                           2. Map its functional roles (keep these brief and specific)
                           3. Identify its technical ecosystem and standards
                           4. Map both direct relationships (from the text) and broader knowledge relationships
                           Be specific and precise. Avoid descriptions - focus on relationships and classifications.
                           Return only valid JSON with no additional text."""

        items = {"type": "object",
                 "properties": {
                     "name": {
                         "type": "string",
                         "description": "Core entity name"
                     },
                     "primary_domains": {
                         "type": "array",
                         "items": {"type": "string"},
                         "description": "Main domains this entity belongs to (e.g., Security, Development, Infrastructure)"
                     },
                     "functional_roles": {
                         "type": "array",
                         "items": {"type": "string"},
                         "description": "Specific functions/purposes (e.g., Framework, Protocol, Standard, Tool)"
                     },
                     "ecosystem": {
                         "type": "object",
                         "properties": {
                             "platforms"   : { "type": "array", "items": {"type": "string"}},
                             "standards"   : { "type": "array", "items": {"type": "string"}},
                             "technologies": { "type": "array", "items": {"type": "string"}}},
                         "description": "related platforms, standards and technologies"
                     },
                     "direct_relationships": {
                         "type": "array",
                         "items": {
                             "type": "object",
                             "properties": {
                                 "entity": {"type": "string"},
                                 "relationship_type": {"type": "string"},
                                 "strength": {"type": "number", "minimum": 0, "maximum": 1}
                             }
                         },
                         "description": "Relationships with other entities found in the text"
                     },
                     "domain_relationships": {
                         "type": "array",
                         "items": {
                             "type": "object",
                             "properties": {
                                 "concept": {"type": "string"},
                                 "relationship_type": {"type": "string"},
                                 "category": {"type": "string"},
                                 "strength": {"type": "number", "minimum": 0, "maximum": 1}
                             }
                         },
                         "description": "Related concepts from the broader domain knowledge"
                     },
                     "confidence": {
                         "type": "number",
                         "minimum": 0,
                         "maximum": 1
                     }
                 },
                 "required": ["name", "primary_domains", "functional_roles", "direct_relationships",
                              "domain_relationships", "confidence"]}

        # Define extract_entities tool
        extract_entities_tool = {
            "type": "function",
            "function": {
                "name": "extract_entities",
                "description": "Extract entities from text",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "entities": {
                            "type": "array",
                            "items": items,
                        }
                    },
                    "required": ["entities"]
                }
            }
        }

        return {
            "model": target_model,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": content_prompt},
                {"role": "user", "content": f"Extract key entities from this text: {text}"}
            ],
            "tools": [extract_entities_tool],
            "tool_choice": {"type": "function", "function": {"name": "extract_entities"}}
        }
