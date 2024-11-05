from playwright.sync_api import sync_playwright
import time
import os
import csv

email = f'jeff_krafve@hotmail.com'
password = f'Leriken123$'

result_csv = 'result.csv'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  
    page = browser.new_page()
    
    page.goto("https://csfloat.com/db?order=4&min=0&max=1")
    page.wait_for_load_state("networkidle")
    page.click('text=Sign In')
    time.sleep(10)

    page.fill("form input[type='text']", email)  # Replace with actual field name
    page.fill("form input[type='password']", password)  # Replace with actual field name
    time.sleep(2)
    page.click("form button[type='submit']")
    time.sleep(10)
    
    page.click("#imageLogin")
    time.sleep(10)
    page.mouse.click(10, 10)
    page.click("text=Database")
    time.sleep(5)
    page.click("app-search-row[key='d-sort'] mat-form-field").click()
    page.click("text=Recently Updated").click()
    time.sleep(5)
    page.click("text=Search on Database")
    time.sleep(10)

    # Check file existance
    file_exists = os.path.isfile(result_csv) and os.stat(result_csv).st_size != 0

    # Step 5: Open the existing CSV file in append mode
    with open(result_csv, mode='a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header if the file is new
        if not file_exists:
            csv_writer.writerow(["Item", "Date", "SteamID"])  # Adjust based on your table structure

        # Step 6: Scrape each row of the table
        rows = page.query_selector_all("table tr")  # Adjust the selector if needed

        for row in rows:
            name_prefix = row.query_selector_all('app-item-name-row div.name > div.prefix').getText()
            name_suffix = row.query_selector_all('app-item-name-row div.name > div.suffix').getText()
            csv_writer.writerow([item, date, steamId])  # Append the row data to CSV
    
    # Close the browser
    browser.close()
