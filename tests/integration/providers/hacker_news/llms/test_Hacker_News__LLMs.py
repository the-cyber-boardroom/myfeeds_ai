from unittest                                                               import TestCase
from mgraph_db.providers.graph_rag.actions.Graph_RAG__Document__Processor   import Graph_RAG__Document__Processor
from mgraph_db.providers.graph_rag.schemas.Schema__Graph_RAG__LLM__Entities import Schema__Graph_RAG__LLM__Entities


class test_Hacker_News__LLMs(TestCase):

    def test__make_llm_request(self):
        sample_text  = "cyber-news-1"  # Using cached test data
        llm_model    = 'gpt-4o-mini'
        processor    = Graph_RAG__Document__Processor(llm_model=llm_model)
        llm_entities = processor.extract_entities(sample_text)  # create test entities

        assert type(llm_entities) is Schema__Graph_RAG__LLM__Entities
        #pprint(llm_entities.json())
