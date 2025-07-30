import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def run_ui_test():
    # Setup headless Chrome
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1200,900')
    driver = webdriver.Chrome(options=chrome_options)
    dashboard_path = os.path.abspath('scraper_dashboard.html')
    driver.get('file://' + dashboard_path)
    time.sleep(2)
    # Check stats
    assert driver.find_element(By.ID, 'scraper-count').text != '--'
    assert driver.find_element(By.ID, 'qa-pass-rate').text.endswith('%')
    # Check alert banner for broken scrapers
    alert = driver.find_element(By.ID, 'alert-banner')
    if alert.is_displayed():
        assert 'failed more than 3 times' in alert.text
    # Check pie chart
    chart = driver.find_element(By.ID, 'qaChart')
    assert chart.is_displayed()
    # Check toggle tabs
    tabs = driver.find_elements(By.CLASS_NAME, 'toggle-tab')
    for tab in tabs:
        tab.click()
        time.sleep(0.5)
    print('✅ Scraper Health UI test passed.')
    driver.quit()

if __name__ == '__main__':
    run_ui_test()
