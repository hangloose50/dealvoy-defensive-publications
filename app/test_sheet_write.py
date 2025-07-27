# test_sheet_write.py

import test_
from datetime import datetime
from app.utils.health import init_dashboard

def main():
    # Initialize & provision sheets
    gc, sh = init_dashboard()

    # ISO timestamp for this test run
    ts = datetime.utcnow().isoformat()
    print(f"\nâ–¶ï¸ Test timestamp: {ts}\n")

    # 1) Write a toggle into run_config (optional)
    try:
        ws_cfg = sh.worksheet("run_config")
        ws_cfg.append_row([
            "test_toggle",       # config_key
            "1",                 # value
            "Temporary test flag",
            "True"               # enabled
        ])
        print("â†’ Appended test toggle to 'run_config'")
    except Exception as e:
        print(f"âš ï¸ Could not write to run_config: {e}")

    # 2) Append a sample row to Amazon
    try:
        ws_amz = sh.worksheet("Amazon")
        ws_amz.append_row([
            ts,
            "TESTASIN-XYZ",
            49.95,
            True,
            "https://amazon.com/dp/TESTASIN-XYZ"
        ])
        print("â†’ Appended row to 'Amazon'")
    except Exception as e:
        print(f"âš ï¸ Could not write to Amazon: {e}")

    # 3) Append a sample row to PuzzleWarehouse
    try:
        ws_puz = sh.worksheet("PuzzleWarehouse")
        ws_puz.append_row([
            ts,
            "UPC1234567890",
            15.50,
            42,
            "https://www.puzzlewarehouse.com/products/UPC1234567890"
        ])
        print("â†’ Appended row to 'PuzzleWarehouse'")
    except Exception as e:
        print(f"âš ï¸ Could not write to PuzzleWarehouse: {e}")

    # 4) Summarize all worksheets
    print("\nâœ… Sheets now present in your spreadsheet:")
    for ws in sh.worksheets():
        print("   -", ws.title)

    print(f"\nâœ… Test run complete at {ts}")

if __name__ == "__main__":
    main()


