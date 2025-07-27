from utils.health import init_dashboard

def get_enabled_categories(source_name):
    """
    Fetches categories marked ‘enabled’ for a given source_name.
    """
    _, sh = init_dashboard()
    ws     = sh.worksheet("category_config")
    records = ws.get_all_records()
    return [
        row["category"]
        for row in records
        if row.get("source_name") == source_name
           and str(row.get("enabled")).lower() in ("1","true","yes")
    ]
