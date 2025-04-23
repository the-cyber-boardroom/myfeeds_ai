from myfeeds_ai.data_feeds.Data_Feeds__S3__Key_Generator                                                import S3_Key__File__Extension, S3_Key__File__Content_Type
from myfeeds_ai.providers.cyber_security.hacker_news.llms.Hacker_News__Execute_LLM__With_Cache          import Hacker_News__Execute_LLM__With_Cache
from myfeeds_ai.providers.cyber_security.owasp.config.Config__Owasp                                     import FILE_ID__RAW_DATA
from myfeeds_ai.providers.cyber_security.owasp.files.Owasp__File__Top_10                                import Owasp__File__Top_10
from myfeeds_ai.providers.cyber_security.owasp.files.Owasp__Git_Hub__Http_Content                       import Owasp__Git_Hub__Http_Content
from myfeeds_ai.providers.cyber_security.owasp.llms.prompts.LLM__Prompt__Owasp__Top_10__Parse_Markdown  import LLM__Prompt__Owasp__Top_10__Parse_Markdown
from myfeeds_ai.providers.cyber_security.owasp.schemas.Owasp__Top_10__Category                          import Owasp__Top_10__Category
from myfeeds_ai.providers.cyber_security.owasp.schemas.Schema__Owasp__Top_10__Category                  import Schema__Owasp__Top_10__Category
from osbot_utils.type_safe.Type_Safe                                                                    import Type_Safe

class Owasp__Files__Top_10(Type_Safe):
    owasp_github_content: Owasp__Git_Hub__Http_Content

    def file__category__raw_data(self, category: Owasp__Top_10__Category):
        kwargs_file= dict(category     = category                           ,
                          file_id      = FILE_ID__RAW_DATA                  ,
                          extension    = S3_Key__File__Extension   .MARKDOWN,
                          content_type = S3_Key__File__Content_Type.MARKDOWN)
        return Owasp__File__Top_10(**kwargs_file)

    def file__category__raw_data__json(self, category: Owasp__Top_10__Category):
        kwargs_file= dict(category     = category                           ,
                          file_id      = FILE_ID__RAW_DATA                  ,
                          extension    = S3_Key__File__Extension   .JSON    ,
                          data_type    = Schema__Owasp__Top_10__Category    )
        return Owasp__File__Top_10(**kwargs_file)

    def file__a01__broken_access_control__raw_Data(self):
        return self.file__category__raw_data(Owasp__Top_10__Category.A01_2021__BROKEN_ACCESS_CONTROL)

    def file__a01__broken_access_control__raw_Data__json(self):
        return self.file__category__raw_data__json(Owasp__Top_10__Category.A01_2021__BROKEN_ACCESS_CONTROL)

    def a01__broken_access_control__raw_data(self):
        category = Owasp__Top_10__Category.A01_2021__BROKEN_ACCESS_CONTROL
        raw_data = self.raw_data(category)
        return raw_data

    def a01__broken_access_control__raw_data__json(self):
        category       = Owasp__Top_10__Category.A01_2021__BROKEN_ACCESS_CONTROL
        raw_data__json = self.raw_data__json(category)
        return raw_data__json



    def raw_data(self, category: Owasp__Top_10__Category) -> str:
        file__raw_data = self.file__category__raw_data(category=category)
        with file__raw_data as _:
            if _.exists():
                return _.data().decode()
            raw_data = self.owasp_github_content.owasp_top_10__category(_.category)
            _.save_data(raw_data)
            return raw_data

    def raw_data__json(self, category: Owasp__Top_10__Category) -> Schema__Owasp__Top_10__Category:
        file__raw_data       = self.file__category__raw_data      (category=category)
        file__raw_data__json = self.file__category__raw_data__json(category=category)
        with file__raw_data__json as _:
            if _.exists():
                return _.data()

            raw_data                = file__raw_data.data().decode()
            prompt_extract_category = LLM__Prompt__Owasp__Top_10__Parse_Markdown()
            execute_llm_with_cache  = Hacker_News__Execute_LLM__With_Cache().setup()
            llm_request             = prompt_extract_category.llm_request(category_markdown=raw_data)
            llm_response            = execute_llm_with_cache.execute__llm_request(llm_request)
            owasp_top_10_category   = prompt_extract_category.process_llm_response(llm_response)
            _.save_data(owasp_top_10_category)
            return owasp_top_10_category








