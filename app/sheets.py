from app import gspread
from app.oauth2client.service_account import ServiceAccountCredentials

class SheetManager:
    def __init__(self, creds_file, spreadsheet_key):
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        self.client = gspread.authorize(creds)
        self.sheet  = self.client.open_by_key(spreadsheet_key)

    def ensure_sheet(self, title, headers):
        try: ws = self.sheet.worksheet(title)
        except:
            ws = self.sheet.add_worksheet(title=title, rows=1, cols=len(headers))
            ws.append_row(headers)
        return ws

    def append_rows(self, title, rows):
        if not rows: return
        ws = self.ensure_sheet(title, rows[0])
        ws.append_rows(rows, value_input_option='USER_ENTERED')
