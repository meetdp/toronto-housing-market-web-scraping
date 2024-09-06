from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd

url = "https://wowa.ca/toronto-housing-market"
driver = webdriver.Chrome()
driver.get(url)
# driver.maximize_window()
# time.sleep(2)

def get_mortgage_rates():
    pass

def get_market_summary():
    li_elements = driver.find_elements(By.XPATH,
                                       "//div[@class='jsx-9962acc8e0221a81 bg-blue-100 p-4 rounded-lg text-gray-800']//li")
    for li in li_elements:
        print(li.text)

def get_price_movements():
    # todo: filter the text - remove unnecessary text
    table = driver.find_element(By.CSS_SELECTOR, 'table.table-styles')
    headers = []
    data = []

    header_elements = table.find_elements(By.CSS_SELECTOR, 'thead th')
    if header_elements:
        headers = [header.text for header in header_elements]

    rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')

    for row in rows:
        cols = row.find_elements(By.CSS_SELECTOR, 'td')
        row_data = [col.text for col in cols]
        data.append(row_data)

    df = pd.DataFrame(data, columns=headers if headers else None)
    pd.set_option('display.max_columns', None)  # Show all columns
    print(df)

def get_regional_breakdown():

    try:
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='regional-breakdown']/div[2]/div/table"))
        )
    except:
        print("Table not found!")
        driver.quit()
        return

    rankings = []
    regions = []
    average_prices = []
    one_year_changes = []
    total_transactions = []

    for row in rows[1:-1]:
        cells = row.find_elements(By.TAG_NAME, "td")

        if len(cells) > 0:
            ranking = cells[0].text
            region = cells[1].text
            avg_price = cells[2].text
            year_change = cells[3].text
            total_transaction = cells[4].text if len(cells) > 4 else None  # Handle hidden data in mobile view

            rankings.append(ranking)
            regions.append(region)
            average_prices.append(avg_price)
            one_year_changes.append(year_change)
            total_transactions.append(total_transaction)

    df = pd.DataFrame({
        'Ranking': rankings,
        'Region': regions,
        'Average Sold Price': average_prices,
        '1-Year Change': one_year_changes,
        'Total Transactions': total_transactions
    })

    print(df)

def get_avg_home_price():
    pass

def get_recent_stats():
    avg_sold_price = driver.find_element(By.XPATH, '//*[@id="stats"]/div[2]/div/div[1]/div[1]')
    print(avg_sold_price)
