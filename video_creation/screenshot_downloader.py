import os
import cv2
from playwright.sync_api import sync_playwright
from pathlib import Path

from utils.arguments_manager import args_config
from utils.console import print_step, print_substep


def zoom_in(page, times=5):
    for _ in range(times):
        page.keyboard.press("Control++")


def download_screenshots_of_reddit_posts(reddit_object, screenshot_num):
    print_step("Downloading Screenshots")

    # ! Make sure the reddit screenshots folder exists
    Path("assets/png").mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        print_substep("Launching Headless Browser")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 600, "height": 600})

        # login
        page.goto("https://www.reddit.com/login/")
        page.fill('#loginUsername', os.getenv("REDDIT_USERNAME"))
        page.fill('#loginPassword', os.getenv("REDDIT_PASSWORD"))
        page.locator("text=Accedi").click()
        page.locator("text=Accept all").click()

        # Get the thread screenshot
        page.goto(reddit_object["thread_url"], timeout=0)
        page.reload()

        if page.locator('[data-testid="content-gate"]').is_visible():
            # This means the post is NSFW and requires to click the proceed button.
            print_substep("Post is NSFW.")
            page.locator('[data-testid="content-gate"] button').click()

        page.locator('[data-test-id="post-content"]').screenshot(
            path="assets/png/title.png"
        )

        # Take screenshots

        print_substep("Downloading screenshots")
        idx = 0
        for comment in reddit_object["comments"]:

            if len(comment["comment_body"]) < args_config['minchars'] or len(comment["comment_body"]) > args_config['maxchars']:
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

        # Add transparency

        if not(args_config['no_transparency']):
            for l in os.listdir(f"assets/png"):
                img = cv2.imread(f"assets/png/{l}")
                img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
                img[:, :, 3] = 235
                cv2.imwrite(f"assets/png/{l}", img)

        print_substep("Done!", style="bold green")
