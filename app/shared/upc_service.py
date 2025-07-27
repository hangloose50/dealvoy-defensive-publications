# File: shared/upc_service.py

from app import csv

class CsvUPCService:
    def __init__(self, path='upc_cache.csv'):
        self.path = path
        self.cache = {}
        if os.path.exists(self.path):
            with open(self.path, newline='', encoding='utf8') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    self.cache[r['asin']] = r['upc']

    def lookup(self, asin):
        return self.cache.get(asin)

    def update_cache(self, items):
        existing = set(self.cache)
        with open(self.path, 'a', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            for itm in items:
                a, u = itm.get('asin'), itm.get('upc')
                if a and u and a not in existing:
                    writer.writerow([a, u])
        self.__init__(self.path)
