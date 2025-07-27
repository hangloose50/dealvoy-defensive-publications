import logging
from logging.handlers import RotatingFileHandler

def configure_logging(logfile='scraper.log'):
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    handler = RotatingFileHandler(logfile, maxBytes=5_000_000, backupCount=3)
    handler.setFormatter(fmt)
    log.addHandler(handler)


