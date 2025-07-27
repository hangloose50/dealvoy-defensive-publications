import undetected_chromedriver as uc
from app import time

from app.selenium.webdriver.common.by import By
from app.selenium.webdriver.support.ui import WebDriverWait
from app.selenium.webdriver.support import expected_conditions as EC

# ← Replace this ASIN with one that fell through as “missing UPC”
url = "https://www.amazon.com/dp/B09JQZ2KXB"

# Chrome-in-Python options, matching your scraper
opts = uc.ChromeOptions()
opts.headless = True
opts.add_argument("--window-size=1200,800")
opts.add_argument("--disable-blink-features=AutomationControlled")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--disable-gpu")
opts.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/115.0.0.0 Safari/537.36"
)

driver = uc.Chrome(options=opts)
driver.get(url)

# wait up to 15 s for the details section to appear
try:
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "detailBullets_feature_div"))
    )
except:
    pass

html = driver.page_source
with open("debug_selenium_page.html", "w", encoding="utf-8") as f:
    f.write(html)

driver.quit()
print("✅ debug_selenium_page.html written. Open it to inspect.")
