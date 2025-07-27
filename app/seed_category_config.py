from utils.health import init_dashboard
from datetime import datetime

def seed():
    _, sh = init_dashboard()
    ws     = sh.worksheet('category_config')
    rows   = ws.get_all_records()
    if not rows:
        now = datetime.utcnow().isoformat()
        ws.append_row(['Amazon',           'Electronics',   True,  True])
        ws.append_row(['Amazon',           'Toys',          True,  False])
        ws.append_row(['PuzzleWarehouse',  'Jigsaw Puzzles',True,  True])
        print('→ Seeded category_config sample rows')
    else:
        print('→ category_config already has data; skipping seed')

if __name__ == '__main__':
    seed()

