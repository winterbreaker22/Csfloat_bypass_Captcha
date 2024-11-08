import nodriver as uc
import pyautogui
import pygetwindow as gw
import time
import os
import re
import csv
import asyncio
import aiofiles
from datetime import datetime

browser_path = f"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
url = f'https://csfloat.com/db?order=4&min=0&max=1'
email = f'jeff_krafve@hotmail.com'
password = f'Leriken123$'
result_csv = 'result.csv'

wear_levels = {
    "FT": "Field-Tested",
    "MW": "Minimal-Wear",
    "FN": "Factory-New",
    "WW": "Well-Worn",
    "BS": "Battle-Scarred"
}

async def main():
    browser = await uc.start(headless=False) 

    await asyncio.sleep(3)
    page = await browser.get(url)
    await asyncio.sleep(10)

    windows = gw.getWindowsWithTitle("FloatDB - Largest Database of CS2 Skins")
    window = windows[0]
    window.maximize()
    await asyncio.sleep(5)

    signInButton = await page.select('button.login')
    await signInButton.click()
    await asyncio.sleep(15)

    email_input = await page.select("form input[type='text']") 
    await email_input.send_keys(email)
    await asyncio.sleep(3)
    password_input = await page.select("form input[type='password']")  
    await password_input.send_keys(password)
    await asyncio.sleep(3)
    submit_btn = await page.select("form button[type='submit']")
    await submit_btn.click()
    await asyncio.sleep(10)

    image_login = await page.select("#imageLogin")
    await image_login.click()
    await asyncio.sleep(10)
    pyautogui.click(x=100, y=100)
    await asyncio.sleep(5)
    database = await page.select("a[href='/db']")
    await database.click()
    await asyncio.sleep(5)

    try:
        while True:
            await page.reload()
            await asyncio.sleep(100)
            sort_element = await page.query_selector("app-search-row:first-of-type mat-form-field div.mat-mdc-select-arrow-wrapper")
            if sort_element:
                await sort_element.click()  # Click on the element
            recently_updated = await page.select("div.cdk-overlay-container div.cdk-overlay-pane > div mat-option:last-of-type > span")
            await recently_updated.click()
            await asyncio.sleep(1)
            search = await page.select("app-float-db-search button.mat-mdc-button-base")
            await search.click()
            await asyncio.sleep(10)

            # Ensure CSV file headers are in place
            file_exists = os.path.isfile(result_csv) and os.stat(result_csv).st_size != 0
            if not file_exists:
                async with aiofiles.open(result_csv, mode='a', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    await writer.writerow(["Item", "Date", "SteamID"])

            # Step 5: Open the existing CSV file in append mode
            async with aiofiles.open(result_csv, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                for i in range(100):
                    user_element = await page.select(f'table tbody tr:nth-of-type({i+1}) td:last-of-type div.link > div')
                    user_data = str(user_element) if user_element else None
                    if "app-steam-avatar" in user_data: 
                        name_prefix_element = await page.select(f'table tbody tr:nth-of-type({i+1}) app-item-name-row div.name > div.prefix')
                        name_prefix = name_prefix_element.text.strip() if name_prefix_element else None
                        name_suffix_element = await page.select(f'table tbody tr:nth-of-type({i+1}) app-item-name-row div.name > div.suffix')
                        name_suffix = name_suffix_element.text.strip() if name_suffix_element else None
                        field_element = await page.select(f'table tbody tr:nth-of-type({i+1}) td:nth-of-type(3) span')
                        field = field_element.text.strip() if field_element else None
                        match = re.search(r'profiles/(\d+)/inventory', user_data)
                        if match:
                            steamId = match.group(1)

                        item = f'{name_prefix} {name_suffix} ({wear_levels.get(field, "Unknown")})'
                        date = f'{datetime.now().date().strftime(f"%d/%m/%y")} {datetime.now().strftime("%H:%M")}'
                        await writer.writerow([item, date, steamId])
                        print (item, date, steamId)
    
    except Exception as e:
        print (e)

    await browser.stop()

if __name__ == "__main__":
    uc.loop().run_until_complete(main())