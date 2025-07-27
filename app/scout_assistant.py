# === ScoutVision Integration ===
from app.services.scout_vision import identify_product_from_image as scoutvision_pipeline

def handle_image_query(image_path):
    print("🔍 Running ScoutVision on image input...")
    keywords = scoutvision_pipeline(image_path)
    return keywords
# ===============================
import sys
import httpx

from app.services.scrapers import discover_scrapers
from app.services.scrapers.amazon_scraper import scrape_amazon

CATEGORY_ALIASES = {
    "grocery":      ["CostcoCategory", "Walmart", "TargetCategory", "RoundEyeSupply"],
    "toys":         ["EverestToys", "PuzzleWarehouse", "FrontierCoop", "Dandh", "Dollardays", "Eedist", "Empirediscount", "RoundEyeSupply", "Webami"],
    "electronics":  ["AmazonQuick", "AmazonBrowser", "Dandh", "Webami", "Eedist"],
    "gaming":       ["EverestToys", "PuzzleWarehouse", "EbaySearch"],
    "collectibles": ["EbaySearch", "EmpireDiscount"],
    "home":         ["CostcoCategory", "TargetCategory", "Walmart"],
    "health":       ["CostcoCategory", "Walmart"],
    "resellers":    ["EbaySearch"],
}

class ScoutAssistant:
    def __init__(self, api_base="http://127.0.0.1:8000", threshold=5.0):
        self.api_base = api_base
        self.threshold = threshold

    def run(self, prompt: str):
        print(f"Interpreting prompt: {prompt}")

        # 1) detect category keyword
        lower = prompt.lower()
        key = next((k for k in CATEGORY_ALIASES if k in lower), None)
        if key:
            sources = CATEGORY_ALIASES[key]
            print(f"Matched '{key.title()}' → scrapers: {sources}")
        else:
            sources = []
            print("No category found; defaulting to no sources (only Amazon cross-check)")

        
        # 1.5) parse any "without X,Y,Z" to exclude specific sources
        skip = []
        if "without" in prompt.lower():
            parts = prompt.lower().split("without",1)[1]
            skip = [s.strip().title() for s in parts.replace("and",",").split(",") if s.strip()]
            if skip:
                print(f"Excluding scrapers: {skip}")
                sources = [s for s in sources if s not in skip]
    # 2) load full registry and filter case-insensitively
        all_registry = discover_scrapers(active_sources=None)
        if sources:
            aliases_lc = [s.lower() for s in sources]
            registry = {
                name: fn
                for name, fn in all_registry.items()
                if name.lower() in aliases_lc
            }
        else:
            registry = all_registry

        if not registry:
            print("No matching scrapers loaded; aborting.")
            return

        # 3) run scrapers to gather UPCs
        upcs = set()
        for name, fn in registry.items():
            print(f"Running scraper: {name}")
            try:
                for item in fn():
                    if upc := item.get("upc"):
                        upcs.add(upc)
            except Exception as e:
                print(f"  [Error] {name} failed: {e}")

        if not upcs:
            print("No UPCs found; aborting.")
            return

        print(f"Collected {len(upcs)} UPCs; cross-checking on Amazon (ROI ≥ {self.threshold}%)")

        # 4) cross-check on Amazon
        passed = []
        for upc in upcs:
            try:
                snap = scrape_amazon(upc)
                if snap and snap.roi >= self.threshold:
                    passed.append({"upc": snap.upc, "price": snap.price, "roi": snap.roi})
            except Exception as e:
                print(f"  [Error] Amazon check failed for {upc}: {e}")

        if not passed:
            print("No items passed the ROI filter.")
            return

        print(f"{len(passed)} items passed; dispatching to /webhook-debug")

        # 5) dispatch
        try:
            with httpx.Client() as client:
                resp = client.post(
                    f"{self.api_base}/webhook-debug",
                    json={"items": passed},
                    timeout=10.0
                )
                resp.raise_for_status()
                print("Dispatch successful.")
        except Exception as e:
            print(f"Dispatch failed: {e}")

if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) or "Scan Grocery and send to my Sheet"
    ScoutAssistant().run(prompt)













