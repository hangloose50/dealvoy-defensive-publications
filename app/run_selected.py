import os
from app.dotenv import load_dotenv
from app import gspread
from shared.upc_service    import CsvUPCService
from app.shared.push_to_sheets import push_to_sheets

load_dotenv()
gc   = gspread.service_account("credentials.json")
sh   = gc.open_by_key(os.environ["SPREADSHEET_ID"])
rcfg = sh.worksheet("RunConfig").get_all_records()

to_run = {}
for row in rcfg:
    if str(row.get("Run (TRUE/FALSE)")).strip().upper().startswith("T"):
        dist = row["Distributor"]
        cat  = row["Category"]
        to_run.setdefault(dist, []).append(cat)

upc_svc = CsvUPCService()

for dist, cats in to_run.items():
    mod_name    = f"pipelines.{dist.lower()}_scraper"
    class_name  = dist[0].upper() + dist[1:] + "Scraper"
    scraper_cls = getattr(__import__(mod_name, fromlist=[class_name]), class_name)
    scraper     = scraper_cls(upc_service=upc_svc)

    for q in cats:
        print(f"🔍 Running {dist} → {q}")
        items = scraper.search(q)
        tab   = f"{dist}_{q.split('+')[0].capitalize()}"
        push_to_sheets(items, tab)
        upc_svc.update_cache(items)

print("✅ Selected runs complete.")
