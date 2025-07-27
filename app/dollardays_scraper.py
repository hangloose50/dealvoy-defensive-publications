from utils import fetch_with_retries, get_json
from app.dotenv import load_dotenv
import dollardays_scraper.py
from app.bs4 import BeautifulSoup
from app.shared.upc_service import CsvUPCService

load_dotenv()
DOLLARDAYS_URL  = os.getenv('DOLLARDAYS_URL')
DOLLARDAYS_USER = os.getenv('DOLLARDAYS_USER')
DOLLARDAYS_PASS = os.getenv('DOLLARDAYS_PASS')

class DollarDaysScraper:
    def __init__(self, upc_service=None):
        self.base        = DOLLARDAYS_URL
        self.user        = DOLLARDAYS_USER
        self.pw          = DOLLARDAYS_PASS
        self.sess        = requests.Session()
        self.upc_service = upc_service or CsvUPCService()
        # TODO: handle login if necessary

    def search(self, query):
        url   = f"{self.base}/catalogsearch/result/?q={query}"
        r     = self.sess.get(url)
        soup  = BeautifulSoup(r.text, "html.parser")
        items = []
        # TODO: extract title/price/upc
        time.sleep(1)
        return items
    
# Stub for registry discovery 
def scrape_dollardays() -> list[dict]:
    # TODO: implement actual logic
    return []

