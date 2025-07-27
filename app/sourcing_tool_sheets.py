from app import gspread
from app.oauth2client.service_account import ServiceAccountCredentials

class SheetManager:
    def __init__(self, creds_file, spreadsheet_key):
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_key(spreadsheet_key)

    def ensure_sheet(self, title: str, headers: list[str]):
        """
        Create sheet if missing; set header row.
        """
        try:
            ws = self.sheet.worksheet(title)
        except gspread.WorksheetNotFound:
            ws = self.sheet.add_worksheet(title=title, rows=1, cols=len(headers))
            ws.append_row(headers)
        return ws

    def append_rows(self, title: str, rows: list[list]):
        """
        Ensure the worksheet exists, then append the data rows.
        """
        # If rows are empty, do nothing
        if not rows:
            return

        # Use the first row to derive headers if needed
        if all(isinstance(r, dict) for r in rows):
            headers = list(rows[0].keys())
            data = [[r.get(h, "") for h in headers] for r in rows]
        else:
            headers = rows[0]
            data = rows[1:]

        ws = self.ensure_sheet(title, headers)
        ws.append_rows(data, value_input_option="USER_ENTERED")
