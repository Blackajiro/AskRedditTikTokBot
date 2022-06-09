# Imports files
import os

from dotenv import load_dotenv
from utils.console import *
from reddit.threads import *
from video_creation.background import *
from video_creation.voices import *
from video_creation.screenshot_downloader import *
from video_creation.final_video import *
from utils.arguments_manager import *

load_dotenv()

# Generation
if int(os.getenv("VIDEO_TYPE")) == 0:
    for _ in range(args_config['times']):

        # Backgrounds
        download_background()
        download_background_audio()

        # Thread
        reddit_object = get_threads()

        # Audio and Video process
        length, number_of_comments = save_text_to_mp3(reddit_object)
        download_screenshots_of_reddit_posts(reddit_object, number_of_comments)
        chop_background_video(length)
        chop_background_audio(length)

        # Final editing
        final_video = make_final_video(number_of_comments)
elif int(os.getenv("VIDEO_TYPE")) == 1:
    for _ in range(args_config['times']):
        # still needs to download background audio and video
        download_background()
        download_background_audio()
        # and get threads
        reddit_object = get_threads()
        # then need to take a post, save it to mp3 (stitch together title and post text)
        # download a screenshot, divide it in pieces
        length, num_screens = save_text_to_mp3_type_1(reddit_object)
        download_screenshots_of_reddit_posts_type_1(reddit_object)

        chop_background_video(length)
        chop_background_audio(length)
        final_video = make_final_video(num_screens)

else:
    print("Error reading VIDEO_TYPE")
