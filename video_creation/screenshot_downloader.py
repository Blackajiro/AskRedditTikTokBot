import os
import cv2
import numpy as np
from playwright.sync_api import sync_playwright
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
from utils.arguments_manager import args_config
from utils.console import print_step, print_substep
import re
import textwrap

def zoom_in(page, times=5):
    for _ in range(times):
        page.keyboard.press("Control++")

def download_screenshots_of_reddit_posts_type_1(reddit_object):
    print_step("Downloading Screenshots")
    Path("assets/png").mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        print_substep("Launching Headless Browser")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 600, "height": 600})

        print_substep("Logging in")

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

        print_substep("Taking title screenshot")

        # screenshot the whole page for some reason
        page.locator('[data-test-id="post-content"]').screenshot(
            path="assets/png/title.png"
        )

        # Take screenshots
        #print_substep("Taking selftext screenshots")
        #page.locator('[data-test-id="post-container"]').screenshot( # maybe post-content
        #    path="assets/png/container.png"
        #)
        print_substep("Taking screenshots")
        idx = 0
        img_width = 528
        font_size = 14
        padding = 15
        font = ImageFont.truetype(f'video_creation/BentonSans-Regular.ttf', font_size)
        for sentence in reddit_object["thread_selftext"]:
            s = " ".join(sentence.split())  # remove all double " "
            split_sentence = s.split(' ')
            words_to_plot = ['']
            j = 0
            siz = 0
            for w in split_sentence:
                siz += font.getsize(' ' + w)[0]  # for efficiency you could keep this size in memory
                # and add incrementally the size of the current word and the space
                if siz > (img_width - padding * 2 - 1):  # -1 because of possible trailing \n, padding on both sides
                    words_to_plot[j] += '\n'
                    words_to_plot.append(w)  # next line
                    siz = font.getsize(w)[0]
                    j += 1
                else:
                    words_to_plot[j] += ' ' + w
            sent = ' '.join(words_to_plot)
            s = font.getsize(sent)
            bg = Image.new('RGB', (img_width, s[1] * sent.count('\n') + 50), (26, 26, 27))
            img = bg.copy()
            image_editable = ImageDraw.Draw(img)
            image_editable.text((padding, padding), sent, (214, 214, 214), font=font)
            img.save(f"assets/png/comment_{idx}.png")
            idx += 1


def download_screenshots_of_reddit_posts(reddit_object, screenshot_num):
    print_step("Downloading Screenshots")

    Path("assets/png").mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        print_substep("Launching Headless Browser")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 600, "height": 600})

        print_substep("Logging in")

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

        print_substep("Taking title screenshot")

        page.locator('[data-test-id="post-content"]').screenshot(
            path="assets/png/title.png"
        )

        # Take screenshots
        print_substep("Taking comments screenshots")
        idx = 0
        for comment in reddit_object["comments"]:

            if len(comment["comment_body"]) < args_config['minchars'] or len(comment["comment_body"]) > args_config['maxchars']:
                continue

            if idx >= screenshot_num:
                break

            if page.locator('[data-testid="content-gate"]').is_visible():
                page.locator('[data-testid="content-gate"] button').click()
            if page.locator("text=Accept all").is_visible():
                page.locator("text=Accept all").click()

            if page.locator('text=Accept all').is_visible():
                page.locator("text=Accept all").click()

            page.goto(f'https://reddit.com{comment["comment_url"]}')

            page.locator(f"#t1_{comment['comment_id']}").screenshot(
                path=f"assets/png/comment_{idx}.png"
            )

            idx += 1

        # Add transparency
        if not(args_config['no_transparency']):
            print_substep("Applying transparency")
            for l in os.listdir(f"assets/png"):
                img = cv2.imread(f"assets/png/{l}")
                img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
                img[:, :, 3] = 240
                cv2.imwrite(f"assets/png/{l}", img)

        print_substep("Done!", style="bold green")
