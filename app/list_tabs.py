import os
from app import gspread
from app.dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=dotenv_path)

gc = gspread.service_account('credentials.json')
sh = gc.open_by_key(os.environ['SPREADSHEET_ID'])

print('Existing tabs:', [ws.title for ws in sh.worksheets()])
