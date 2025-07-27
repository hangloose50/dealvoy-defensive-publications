# test_provision.py

from app.utils.health import init_dashboard

def main():
    _, sh = init_dashboard()

    print("\n✅ Sheets now in your spreadsheet:")
    for ws in sh.worksheets():
        print("  -", ws.title)

if __name__ == "__main__":
    main()
