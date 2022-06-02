import os

from playwright.sync_api import sync_playwright
from pathlib import Path
from rich.progress import track
from utils.console import print_step, print_substep

def reddit_login(browser):
    page = browser.new_page()
    page.goto("https://www.reddit.com/login/")
    page.fill('#loginUsername', os.getenv("REDDIT_USERNAME"))
    page.fill('#loginPassword', os.getenv("REDDIT_PASSWORD"))
    page.click('#loginPassword')


    page.keyboard.press("Enter")
    page.screenshot(path='login.png')

def download_screenshots_of_reddit_posts(reddit_object, screenshot_num):
    print_step("Downloading Screenshots")

    # ! Make sure the reddit screenshots folder exists
    Path("assets/png").mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        print_substep("Launching Headless Browser")
        browser = p.chromium.launch()
        reddit_login(browser)
        # Get the thread screenshot
        page = browser.new_page()
        page.goto(reddit_object["thread_url"])

        if page.locator('[data-testid="content-gate"]').is_visible():
            # This means the post is NSFW and requires to click the proceed button.
            print_substep("Post is NSFW.")
            page.locator('[data-testid="content-gate"] button').click()

        page.locator('[data-test-id="post-content"]').screenshot(
            path="assets/png/title.png"
        )

        print_substep("Downloading screenshots")

        idx = 0
        for comment in reddit_object["comments"]:

            if len(comment["comment_body"]) > int(os.getenv("MAX_COMMENT_CHARS")):
                continue

            if idx >= screenshot_num:
                break

            if page.locator('[data-testid="content-gate"]').is_visible():
                page.locator('[data-testid="content-gate"] button').click()

            page.goto(f'https://reddit.com{comment["comment_url"]}')
            page.locator(f"#t1_{comment['comment_id']}").screenshot(
                path=f"assets/png/comment_{idx}.png"
            )

            idx += 1

        print_substep("Done!", style="bold green")
