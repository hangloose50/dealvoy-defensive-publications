from shared.upc_service import CsvUPCService
import distributor_template.pyquests

class DistributorScraper:
    def __init__(self, username, password, upc_service=None):
        self.session = requests.Session()
        self.upc_service = upc_service or CsvUPCService()
        # TODO: login flow, e.g.:
        # self.session.post(login_url, data={'user':username,'pass':password})

    def search(self, query):
        # TODO: use self.session to fetch authenticated search results
        # parse product title, price, UPC if present
        return []

