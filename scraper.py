from playwright.sync_api import sync_playwright
import time
import os
import csv

email = f'jeff_krafve@hotmail.com'
password = f'Leriken123$'

result_csv = 'result.csv'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  
    context = browser.new_context(
        viewport={"width": 1600, "height": 900}  # Set to your desired resolution
    )
    page = context.new_page()
    
    page.goto("https://csfloat.com/db?order=4&min=0&max=1")
    page.evaluate("window.resizeTo(screen.availWidth, screen.availHeight);")
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

    element = page.query_selector("app-search-row:first-of-type mat-form-field")
    if element:
        element.click()  # Click on the element
    page.click("text=Recently Updated")
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
            name_prefix = row.query_selector_all('app-item-name-row div.name > div.prefix').get_text()
            name_suffix = row.query_selector_all('app-item-name-row div.name > div.suffix').get_text()
            field = row.query_selector_all('td:nth-of-type(2) span').get_text()
            steamId = row.query_selector_all('app-steam-avatar a').get_attribute('href')
            print ("name_prefix: ", name_prefix)
            print ("name_suffix: ", name_suffix)
            print ("field: ", field)
            print ("steamId: ", steamId)
            # csv_writer.writerow([item, date, steamId])  # Append the row data to CSV
    
    # Close the browser
    browser.close()
