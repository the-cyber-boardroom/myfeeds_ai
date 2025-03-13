# todo refactor using now OSBot_Utils llm capabilities
# from typing                          import Dict, Any
# from osbot_utils.type_safe.Type_Safe import Type_Safe
# from osbot_utils.utils.Env           import get_env
# from osbot_utils.utils.Http          import POST_json
#
# ENV_NAME_OPEN_AI__API_KEY = "OPEN_AI__API_KEY"
#
# class My_Feeds__LLMs(Type_Safe):
#     api_url     : str = "https://api.openai.com/v1/chat/completions"
#     api_key_name: str = ENV_NAME_OPEN_AI__API_KEY
#
#     def api_key(self):
#         api_key = get_env(self.api_key_name)
#         if not api_key:
#             raise ValueError("{self.api_key_name} key not set")
#         return api_key
#
#     def execute(self, llm_payload: Dict[str, Any]):
#         url = self.api_url
#
#         headers = {"Authorization": f"Bearer {self.api_key()}",
#                    "Content-Type": "application/json",
#                    'User-Agent': "myfeeds.ai"}
#         #response = POST_json(url, headers=headers, data=llm_payload)            # todo: add error handling
#         #return response
#         return llm_payload
#
# class Hacker_News__LLMs(My_Feeds__LLMs):
#
#     pass
#
