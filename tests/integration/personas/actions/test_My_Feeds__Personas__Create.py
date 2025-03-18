import pytest
from unittest                                                                                   import TestCase
from mgraph_db.mgraph.actions.MGraph__Index                                                     import MGraph__Index
from mgraph_db.mgraph.MGraph                                                                    import MGraph
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__Nodes                             import Schema__MGraph__RAG__Node__Text_Id
from myfeeds_ai.personas.actions.My_Feeds__Personas import My_Feeds__Personas
from myfeeds_ai.personas.actions.My_Feeds__Personas__Create                                     import My_Feeds__Personas__Create
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Day                   import Hacker_News__Day
from myfeeds_ai.providers.cyber_security.hacker_news.actions.Hacker_News__Text_Entities         import Node_Type__Article_Id
from myfeeds_ai.providers.cyber_security.hacker_news.schemas.Schema__Feed__Day__Text_Entities   import Schema__Feed__Day__Text_Entities
from osbot_utils.helpers.Obj_Id                                                                 import Obj_Id
from osbot_utils.helpers.duration.decorators.print_duration                                     import print_duration
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI                               import ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.utils.Dev                                                                      import pprint
from osbot_utils.utils.Env                                                                      import get_env
from osbot_utils.utils.Files                                                                    import file_not_exists, file_create
from osbot_utils.utils.Http                                                                     import GET_json
from tests.integration.data_feeds__objs_for_tests                                               import myfeeds_tests__setup_local_stack


class test_My_Feeds__Personas__Create(TestCase):

    @classmethod
    def setUpClass(cls):
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip('This test requires OpenAI API Key to run')
        myfeeds_tests__setup_local_stack()
        cls.persona_create = My_Feeds__Personas__Create()
        cls.personas       = My_Feeds__Personas()



    def test_create_persona__ciso(self):
        with self.persona_create as _:
            persona_ciso = _.create_persona__ciso()
            pprint(persona_ciso.json())

    def test_extract_entities_from_text(self):
        with self.persona_create as _:
            #_.execute_llm_with_cache().refresh_llm_cache()
            text = ("The Chief Information Security Officer (CISO), who reports to the CEO,  at a FinTech company collaborates closely "
                    "with compliance officers and risk assessors to manage cybersecurity risks. "
                    "The company leverages Digital Payment Platforms, Mobile Banking Solutions, "
                    "and Identity and Access Management Systems, aligning with ISO/IEC 27001 and NIST Cybersecurity Framework. "
                    "They actively employ Intrusion Detection Systems, Data Loss Prevention Tools, Incident Management Tools, "
                    "and Security Information and Event Management (SIEM) platforms. Ensuring data protection through Privacy "
                    "Policies, Data Encryption, and Anonymisation Techniques, the CISO maintains regulatory compliance adhering to "
                    "GDPR, SOX, PCI DSS, and NIST SP 800-53 standards. Additionally, they utilize Threat Intelligence and Incident "
                    "Response strategies, supported by Security Analysts, Incident Responders, and Threat Hunters, to proactively "
                    "manage operational risks and information assurance.")

            text = ("""\
The Board Member responsible for cybersecurity governance provides oversight and strategic direction on cybersecurity matters 
within the FinTech company. Though having limited technical experience, this member collaborates closely with senior management 
and compliance teams to ensure effective management of cybersecurity risks.

The Board Member focuses on understanding key cybersecurity trends, regulatory developments, and high-level threats relevant 
to Digital Payment Platforms and Mobile Banking Solutions. Emphasis is placed on the importance of protecting sensitive data, 
maintaining regulatory compliance, and ensuring that cybersecurity practices align with best industry standards.

By engaging regularly with cybersecurity experts and receiving tailored briefings, the Board Member stays informed on cybersecurity 
issues to make well-informed governance decisions, contributing effectively to the organization's overall security posture.""")

            persona__text_entities = _.extract_entities_from_text(text)
            text_entities          = persona__text_entities.text_entities
            cache_id               = persona__text_entities.cache_id
            graph_rag              = _.prompt_extract_entities.create_entities_graph_rag(text_entities)
            png_file = f'{self.__class__.__name__}-{cache_id}.png'
            if file_not_exists(png_file):
                pprint(graph_rag.screenshot__create_file(png_file))

            text_ids = list(graph_rag.mgraph_entity.index().get_nodes_by_type(Schema__MGraph__RAG__Node__Text_Id))

            print()
            print(graph_rag.mgraph_entity.export().export_tree_values().as_text(text_ids))

    def test__get_tree_for_full_feed(self):
        source_url = 'https://dev.myfeeds.ai/public-data/hacker-news/latest/feed-text-entities-titles.mgraph.json'
        with print_duration():
            json_code  = GET_json(source_url)
        with print_duration():
            mgraph                = MGraph.from_json(json_code)
            index : MGraph__Index = mgraph.index()
            articles_ids   = list(index.get_nodes_by_type(Node_Type__Article_Id))
            mgraph_as_text = mgraph.export().export_tree_values().as_text(articles_ids)
            file_create(path='./feed-as-text.txt', contents=mgraph_as_text)
            pprint(len(mgraph_as_text))


    def test__get_tree_for_news(self):
        #path__folder__data = "2025/03/14/19"
        path__folder__data = "2025/03/13/23"
        with Hacker_News__Day(path__folder__data=path__folder__data) as _:
            merged_day_entities = _.file_merged_day_entities__load()
            articles_ids         = merged_day_entities.articles_ids
            mgraph              = merged_day_entities.mgraph_entities
            articles_node_id     = []
            for article_id in articles_ids:
                article_node_id = mgraph.index().values_index.get_node_id_by_value(Obj_Id, article_id, node_type=Node_Type__Article_Id)
                articles_node_id.append(article_node_id)

            assert type(_)                   is Hacker_News__Day
            assert _.now().year              == 2025
            assert type(merged_day_entities) is Schema__Feed__Day__Text_Entities
            assert type(mgraph)              is MGraph

            mgraph.export().export_tree_values().print_as_text(articles_node_id)

            #



