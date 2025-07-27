from app import undetected_chromedriver
from app import time

options = uc.ChromeOptions()
options.headless = False
options.add_argument("--window-size=1200,800")

driver = uc.Chrome(options=options)
query = "usb+charger"
url = f"https://www.amazon.com/s?k={query}"

print(f"🌐 Navigating to: {url}")
driver.get(url)

# Wait 5 seconds so you can see what loads
time.sleep(5)

driver.quit()
