from osbot_fast_api.api.Fast_API_Routes                                                     import Fast_API_Routes
from myfeeds_ai.providers.cyber_security.docs_diniscruz_ai.actions.Docs_DinisCruz_Ai__Files import Docs_DinisCruz_Ai__Files

ROUTE_PATH__DOCS_DINISCRUZ_AI   = 'docs-diniscruz-ai'
ROUTES_PATHS__DOCS_DINISCRUZ_AI = [f'/{ROUTE_PATH__DOCS_DINISCRUZ_AI}/all-files',
                                   f'/{ROUTE_PATH__DOCS_DINISCRUZ_AI}/home-page']

class Routes__Docs_DinisCruz_Ai(Fast_API_Routes):
    tag                      : str = ROUTE_PATH__DOCS_DINISCRUZ_AI
    files__docs_diniscruz_ai : Docs_DinisCruz_Ai__Files

    def all_files(self):
        return self.files__docs_diniscruz_ai.all_files()

    def home_page(self):
        return self.files__docs_diniscruz_ai.home_page__data()

    def setup_routes(self):
        self.add_route_get(self.all_files)
        self.add_route_get(self.home_page)

