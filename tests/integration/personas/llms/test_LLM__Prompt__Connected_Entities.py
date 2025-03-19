import pytest
from unittest                                                                                   import TestCase
from myfeeds_ai.personas.llms.LLM__Prompt__Connect_Entities                                     import LLM__Prompt__Connect_Entities, SYSTEM_PROMPT__CONNECT_ENTITIES
from myfeeds_ai.personas.llms.Schema__Persona__Connected_Entities                               import Schema__Persona__Connected_Entities
from myfeeds_ai.providers.cyber_security.hacker_news.llms.Hacker_News__Execute_LLM__With_Cache  import Hacker_News__Execute_LLM__With_Cache
from osbot_utils.helpers.llms.platforms.open_ai.API__LLM__Open_AI                               import ENV_NAME_OPEN_AI__API_KEY
from osbot_utils.helpers.llms.schemas.Schema__LLM_Request__Message__Role                        import Schema__LLM_Request__Message__Role
from osbot_utils.utils.Dev                                                                      import pprint
from osbot_utils.utils.Env                                                                      import get_env
from tests.integration.data_feeds__objs_for_tests                                               import myfeeds_tests__setup_local_stack


class test_LLM__Prompt__Connected_Entities(TestCase):

    @classmethod
    def setUpClass(cls):
        if get_env(ENV_NAME_OPEN_AI__API_KEY) is None:
            pytest.skip('This test requires OpenAI API Key to run')
        myfeeds_tests__setup_local_stack()
        cls.prompt_connect_entities = LLM__Prompt__Connect_Entities()

    def test_llm_request(self):
        with self.prompt_connect_entities as _:
            persona_graph_tree  = TEST_DATA__PERSONA__GRAPH_TREE__CEO
            articles_graph_tree = TEST_DATA__ARTICLES__GRAPH_TREE
            llm_request = self.prompt_connect_entities.llm_request(persona_graph_tree=persona_graph_tree, articles_graph_tree=articles_graph_tree)
            assert llm_request.request_data.function_call.parameters == Schema__Persona__Connected_Entities
            with llm_request.request_data.messages[0] as _:
                assert _.role == Schema__LLM_Request__Message__Role.SYSTEM
                assert _.content == SYSTEM_PROMPT__CONNECT_ENTITIES
            with llm_request.request_data.messages[1] as _:
                assert _.role == Schema__LLM_Request__Message__Role.USER
                assert persona_graph_tree in _.content
                assert articles_graph_tree in _.content


    def test_process_llm_response(self):
        persona_graph_tree  = TEST_DATA__PERSONA__GRAPH_TREE__CISO
        articles_graph_tree = TEST_DATA__ARTICLES__GRAPH_TREE
        llm_request         = self.prompt_connect_entities.llm_request(persona_graph_tree  = persona_graph_tree ,
                                                               articles_graph_tree = articles_graph_tree)
        with Hacker_News__Execute_LLM__With_Cache().setup() as _:
            #_.refresh_llm_cache()
            llm_response            = _ .execute__llm_request(llm_request)
        connected_entities      = self.prompt_connect_entities.process_llm_response(llm_response)
        assert len(connected_entities.connected_entities) > 1

TEST_DATA__PERSONA__GRAPH_TREE__CEO = """\
c0f98645
    entity:
        Chief Executive Officer
            responsible_for:
                CEO
                business continuity
                reputational risk
                regulatory compliance
            works_with:
                CFO
                CISO
                CTO
                legal counsel
            complies_with:
                SOX
                GDPR
            uses:
                cloud services
                AI/ML technologies
                business intelligence platforms
            maintains_awareness_of:
                cyber threats
                data breaches 
                significant security incidents

"""

TEST_DATA__ARTICLES__GRAPH_TREE = """\
78854374
    article_entity:
        AI-Powered Deception
        Cybersecurity
        Societies
        AI
        Deception
            is_a_threat_to:
                AI-Powered Deception
            addresses:
                Cybersecurity

--------

723f68c4
    article_entity:
        Bybit
        Safe{Wallet}
        Supply Chain Attack
            involved_in:
                North Korean Hackers
        North Korean Hackers
        Cryptocurrency Exchange
            associated_with:
                Safe{Wallet}
            victim_of:
                Bybit

--------

f7e8f6e9
    article_entity:
        ACR Stealer
        Cracked Software
            is_used_by:
                Cracked Software
            targeted_by:
                ACR Stealer
                Lumma
        Lumma
        Malware Campaign
        Malware Defense

--------

94f19672
    article_entity:
        CVE-2025-23209
        CISA
        Active Attacks
            Targeted_by:
                Craft CMS
            Describes_threat:
                CVE-2025-23209
        Craft CMS
        United States
            Operates_within:
                CISA
            Involved_in:
                Craft CMS

--------
"""
TEST_DATA__PERSONA__GRAPH_TREE__CISO = """\
ba29d8c4
    entity:
        CISO
            responsible_for:
                CISO
            works_with:
                CEO
                    works_with:
                        CISO
                    responsible_for:
                        CEO
                compliance officers
                    responsible_for:
                        CISO
                    works_for:
                        FinTech company
                risk assessors
                    responsible_for:
                        CISO
                    works_for:
                        FinTech company
            uses:
                Digital Payment Platforms
                    uses:
                        FinTech company
                Mobile Banking Solutions
                    uses:
                        FinTech company
                Identity and Access Management Systems
                    uses:
                        FinTech company
                Intrusion Detection Systems
                    uses:
                        FinTech company
                Data Loss Prevention Tools
                    uses:
                        FinTech company
                Incident Management Tools
                    uses:
                        FinTech company
                SIEM
                    uses:
                        FinTech company
                Threat Intelligence
                    uses:
                        FinTech company
            implements:
                ISO/IEC 27001
                    implements:
                        FinTech company
                NIST Cybersecurity Framework
                    implements:
                        FinTech company
            protects_against:
                Privacy Policies
                    protects_against:
                        CISO
                    protects:
                        FinTech company
                Data Encryption
                    protects_against:
                        CISO
                    protects:
                        FinTech company
                Anonymisation Techniques
                    protects_against:
                        CISO
                    protects:
                        FinTech company
            complies_with:
                GDPR
                    complies_with:
                        FinTech company
                SOX
                    complies_with:
                        FinTech company
                PCI DSS
                    complies_with:
                        FinTech company
                NIST SP 800-53
                    complies_with:
                        FinTech company
        CEO
        compliance officers
        risk assessors
        Digital Payment Platforms
        Mobile Banking Solutions
        Identity and Access Management Systems
        ISO/IEC 27001
        NIST Cybersecurity Framework
        Intrusion Detection Systems
        Data Loss Prevention Tools
        Incident Management Tools
        SIEM
        Privacy Policies
        Data Encryption
        Anonymisation Techniques
        GDPR
        SOX
        PCI DSS
        NIST SP 800-53
        Threat Intelligence
        Incident Response strategies
            uses:
                FinTech company
        Security Analysts
            manages:
                CISO
        Incident Responders
            manages:
                CISO
        Threat Hunters
            manages:
                CISO

--------
"""