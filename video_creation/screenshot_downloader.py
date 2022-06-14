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


def title_to_png(header, title, img_padding=15):
    print_substep('Generating ' + str(title) + '.png')
    font = ImageFont.truetype(f'video_creation/BentonSans-Regular.ttf', 14)
    bigger_font = ImageFont.truetype(f'video_creation/BentonSans-Regular.ttf', 20)

    # Create image to obtain text size
    img = Image.new("L", (1000, 500), color=0)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(header + "\n\n" + title, font=bigger_font)

    # Create final image with padding
    img2 = Image.new("L", (w + img_padding * 2, h + img_padding * 2), color=0)
    draw2 = ImageDraw.Draw(img2)
    draw2.text((img_padding, img_padding), text=header, fill='lightgray', font=font, spacing=5)
    draw2.text((img_padding, img_padding + 30), text=title, fill='white', font=bigger_font, spacing=5)
    img2.save(f"assets/png/title.png")


def text_to_png(text, name, img_padding=15):
    print_substep('Generating ' + str(name) + '.png')
    font = ImageFont.truetype(f'video_creation/BentonSans-Regular.ttf', 16)

    # Remove urls
    paragraph = re.sub(r'http\S+', '', text)

    # Fix whitespaces
    paragraph = re.sub(' +', ' ', paragraph)
    paragraph = paragraph.replace('.', '. ')

    # Single string line to multiline
    wrapped_text = textwrap.wrap(paragraph, width=60)
    text = "\n".join(wrapped_text)

    # Create image to obtain text size
    img = Image.new("L", (1000, 500), color=0)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(text, font=font)

    # Create final image with padding
    img2 = Image.new("L", (w + img_padding * 2, h + img_padding * 2), color=0)
    draw2 = ImageDraw.Draw(img2)
    draw2.text((img_padding, img_padding), text=text, fill='white', font=font, spacing=5)
    img2.save(f"assets/png/{name}.png")

    return True


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

        # Take screenshots
        if args_config['mode'] == 'ask':

            print_substep("Generating title.png")

            page.locator('[data-test-id="post-content"]').screenshot(
                path="assets/png/title.png"
            )

            print_substep("Taking comments screenshots")

            idx = 0
            for comment in reddit_object["comments"]:

                if len(comment["comment_body"]) < args_config['minchars'] or len(comment["comment_body"]) > args_config[
                    'maxchars']:
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

        elif args_config['mode'] == 'story':

            print_substep("Generating title.png")
            title_to_png("Posted by " + reddit_object['author'], reddit_object['thread_title'])

            for idx, paragraph in enumerate(reddit_object["thread_selftext"]):
                text_to_png(paragraph, "comment_" + str(idx))

        else:
            exit(-1)

        # Add transparency
        if not (args_config['no_transparency']):
            print_substep("Applying transparency")
            for l in os.listdir(f"assets/png"):
                img = cv2.imread(f"assets/png/{l}")
                img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
                img[:, :, 3] = 240
                cv2.imwrite(f"assets/png/{l}", img)

        print_substep("Done!", style="bold green")
