from playwright.sync_api import sync_playwright

# Launching Playwright
with sync_playwright() as p:
    # Step 1: Start a browser instance (you can use 'firefox' or 'webkit' instead of 'chromium' if needed)
    browser = p.chromium.launch(headless=False)  # Set headless=True to run without a visible window
    page = browser.new_page()
    
    # Step 2: Go to the login page
    page.goto("https://example.com/login")

    # Step 3: Fill out the login form
    page.fill("input[name='username']", "your_username")  # Replace with actual field name
    page.fill("input[name='password']", "your_password")  # Replace with actual field name
    
    # Step 4: Click the login button
    page.click("button[type='submit']")  # Replace with actual selector for login button
    
    # Optional: Wait for navigation or an element that indicates successful login
    page.wait_for_selector("text=Welcome")  # Adjust selector to match a login success indicator

    # Step 5: Navigate to another page after login
    page.goto("https://example.com/protected-page")
    
    # Step 6: Extract data (for example, the title of the protected page)
    title = page.title()
    print("Page Title:", title)
    
    # Close the browser
    browser.close()
