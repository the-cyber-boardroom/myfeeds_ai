from unittest                                                                   import TestCase
from myfeeds_ai.providers.cyber_security.hacker_news.llms.LLM__Prompt_Creator   import LLM__Prompt_Creator

class test_LLM__Prompt_Creator(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.llm_prompt_creator = LLM__Prompt_Creator()

    # todo: fix this since the prompt_data has been impacted by the recent refactoring and improvements of the LLMs schemas
    # def test_prompt(self):
    #     sample_text  = "cyber-news-1"
    #     prompt_data  = self.llm_prompt_creator.prompt(sample_text)
    #     print()
    #     assert prompt_data == EXPECTED_PROMPTS.get(sample_text)


    # todo: fix to take into account recent fixes to schema_for_llms.export
    # def test_type_safe_to_schema(self):
    #     schema_for_llms = Type_Safe__Schema_For__LLMs()
    #     assert schema_for_llms.export(Schema__Graph_RAG__Entities__LLMs) == EXPECTED_SCHEMA

        #pprint(EXPECTED_SCHEMA)

EXPECTED_SCHEMA = { 'properties': { 'entities': { 'items': { 'properties': { 'confidence': { 'maximum': 1,
                                                                                               'minimum': 0,
                                                                                               'type': 'number'},
                                                                             'direct_relationships': { 'description': 'Relationships with other entities found in the text',
                                                                                                       'items': { 'properties': { 'entity': { 'type': 'string'},
                                                                                                                                  'relationship_type': { 'type': 'string'},
                                                                                                                                  'strength': { 'maximum': 1,
                                                                                                                                                'minimum': 0,
                                                                                                                                                'type': 'number'}},
                                                                                                                  'required': [ 'entity','relationship_type', 'strength'] ,
                                                                                                                  'type'    : 'object'},
                                                                                                       'type': 'array'},
                                                                             'domain_relationships': { 'description': 'Related '
                                                                                                                      'concepts '
                                                                                                                      'from '
                                                                                                                      'the '
                                                                                                                      'broader '
                                                                                                                      'domain '
                                                                                                                      'knowledge',
                                                                                                       'items': { 'properties': { 'category': { 'type': 'string'},
                                                                                                                                  'concept': { 'type': 'string'},
                                                                                                                                  'relationship_type': { 'type': 'string'},
                                                                                                                                  'strength': { 'maximum': 1,
                                                                                                                                                'minimum': 0,
                                                                                                                                                'type': 'number'}},
                                                                                                                  'required': ['concept', 'relationship_type', 'category', 'strength'],
                                                                                                                  'type'    : 'object'},
                                                                                                       'type': 'array'},
                                                                             'ecosystem': { 'description': 'related '
                                                                                                           'platforms, '
                                                                                                           'standards '
                                                                                                           'and '
                                                                                                           'technologies',
                                                                                            'properties': { 'platforms': { 'items': { 'type': 'string'},
                                                                                                                           'type': 'array'},
                                                                                                            'standards': { 'items': { 'type': 'string'},
                                                                                                                           'type': 'array'},
                                                                                                            'technologies': { 'items': { 'type': 'string'},
                                                                                                                              'type': 'array'}},
                                                                                            'required': [ 'platforms', 'standards', 'technologies'],
                                                                                            'type': 'object'},
                                                                             'functional_roles': { 'description': 'Specific '
                                                                                                                  'functions/purposes '
                                                                                                                  '(e.g., '
                                                                                                                  'Framework, '
                                                                                                                  'Protocol, '
                                                                                                                  'Standard, '
                                                                                                                  'Tool)',
                                                                                                   'items': { 'type': 'string'},
                                                                                                   'type': 'array'},
                                                                             'name': { 'description': 'Core '
                                                                                                      'entity '
                                                                                                      'name',
                                                                                       'type': 'string'},
                                                                             'primary_domains': { 'description': 'Main '
                                                                                                                 'domains '
                                                                                                                 'this '
                                                                                                                 'entity '
                                                                                                                 'belongs '
                                                                                                                 'to '
                                                                                                                 '(e.g., '
                                                                                                                 'Security, '
                                                                                                                 'Development, '
                                                                                                                 'Infrastructure)',
                                                                                                  'items': { 'type': 'string'},
                                                                                                  'type': 'array'}
                                                                },
                                                              'required': [ 'confidence'          ,
                                                                            'direct_relationships',
                                                                            'domain_relationships',
                                                                            'ecosystem'           ,
                                                                            'functional_roles'    ,
                                                                            'name'                ,
                                                                            'primary_domains'     ,
                                                                            ],
                                                              'type': 'object'},
                                                   'type': 'array'}},
                     'required': ['entities'],
                     'type': 'object'}

SYSTEM_CONTENT = ('You are a comprehensive knowledge extractor that '
                  'maps entities into a rich semantic network.\n'
                  '                           For each entity:\n'
                  '                           1. Identify its core '
                  'essence and domain classifications\n'
                  '                           2. Map its functional '
                  'roles (keep these brief and specific)\n'
                  '                           3. Identify its '
                  'technical ecosystem and standards\n'
                  '                           4. Map both direct '
                  'relationships (from the text) and broader '
                  'knowledge relationships\n'
                  '                           Be specific and '
                  'precise. Avoid descriptions - focus on '
                  'relationships and classifications.\n'
                  '                           Return only valid '
                  'JSON with no additional text.')
EXPECTED_PROMPTS = { "cyber-news-1": { 'messages': [ { 'content': SYSTEM_CONTENT,
                                                       'role'   : 'system'     },
                                                    { 'content': 'Extract key entities from this text: '
                                                                 'cyber-news-1',
                                                      'role': 'user'}],
                                      'model': '',
                                      'response_format': {'type': 'json_object'},
                                      'tool_choice': {'function': {'name': 'extract_entities'}, 'type': 'function'},
                                      'tools': [ { 'function': { 'description': 'Extract entities from text',
                                                                 'name': 'extract_entities',
                                                                 'parameters': EXPECTED_SCHEMA },
                                                   'type'    : 'function'}]}}