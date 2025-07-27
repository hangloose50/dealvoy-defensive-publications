# test_runs.py
from app.utils.health import init_dashboard, init_runs_sheet, log_session

def main():
    # 1) connect to or create your dashboard
    gc, sh = init_dashboard()

    # 2) connect to or create the 'runs' sheet
    runs_ws = init_runs_sheet(sh)

    # 3) log a dummy session
    items_scraped = 42
    errors        = 3
    total_roi     = 18.75

    log_session(runs_ws, items_scraped, errors, total_roi)

if __name__ == "__main__":
    main()
