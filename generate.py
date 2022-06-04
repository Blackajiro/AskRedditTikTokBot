# Imports files
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
