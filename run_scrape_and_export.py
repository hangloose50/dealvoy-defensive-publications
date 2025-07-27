import gspread
from google.oauth2.service_account import Credentials
from app.services.scrapers.amazon_scraper import scrape_amazon
from app.services.walmart_scraper import scrape_walmart_product

def export_to_google_sheets(data: list[dict], sheet_name: str, worksheet_name: str = "Sheet1"):
    """
    Exports a list of dicts to a Google Sheet.
    - data: List of product dicts.
    - sheet_name: Name of the Google Sheet.
    - worksheet_name: Name of the worksheet/tab.
    """
    creds = Credentials.from_service_account_file("credentials.json", scopes=[
        "https://www.googleapis.com/auth/spreadsheets"
    ])
    gc = gspread.authorize(creds)
    sh = gc.open(sheet_name)
    try:
        ws = sh.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=worksheet_name, rows="100", cols="20")
    ws.clear()
    if data:
        headers = list(data[0].keys())
        ws.append_row(headers)
        for row in data:
            ws.append_row([row.get(h, "") for h in headers])

def main():
    # Scrape Amazon
    amazon_results = scrape_amazon("lego", max_results=5)
    # Scrape Walmart
    walmart_result = scrape_walmart_product("lego")
    walmart_results = [walmart_result] if walmart_result else []

    # Combine results
    all_results = amazon_results + walmart_results

    # Export to Google Sheets
    export_to_google_sheets(all_results, sheet_name="ProductResults", worksheet_name="LegoSearch")

if __name__ == "__main__":
    main()