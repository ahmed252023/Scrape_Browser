from playwright.sync_api import sync_playwright

def extract(query, num_page=5):
    with sync_playwright() as pr:
        browser = pr.chromium.launch(headless=False)
        page = browser.new_page()
        url_search = f'https://www.bing.com/search?q={query}'
        page.goto(url_search)

        for _ in range(num_page):
            page.wait_for_selector('li.b_algo a', timeout=5000)

            # Extract titles, links, and descriptions
            links = page.eval_on_selector_all("li.b_algo a", "nodes => nodes.map(n => n.href)")
            descriptions = page.eval_on_selector_all("li.b_algo p", "nodes => nodes.map(n => n.innerText)")

            for link, desc in zip(links, descriptions):
                print(f"Link: {link}")
                print(f"Description: {desc}\n")

            # Click the next page button
            next_page = page.query_selector('a.sb_pagN')
            if next_page:
                next_page.click()
                page.wait_for_timeout(3000)
            else:
                break

        browser.close()

# Get user input for the search query and number of pages
query = input("Enter your search query: ")
num_page = input("Enter the number of pages to scrape (default is 5): ")
num_page = int(num_page) if num_page.isdigit() else 5

extract(query, num_page)




