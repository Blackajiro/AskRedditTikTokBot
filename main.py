from utils.console import print_markdown
import time
from reddit.threads import get_threads
from video_creation.background import download_background, chop_background_video
from video_creation.voices import save_text_to_mp3
from video_creation.screenshot_downloader import download_screenshots_of_reddit_posts
from video_creation.final_video import make_final_video

print_markdown("AskRedditTikTokBot - based on elebumm's RedditVideoMakerBot")

reddit_object = get_threads()

length, number_of_comments = save_text_to_mp3(reddit_object)
download_screenshots_of_reddit_posts(reddit_object, number_of_comments)
download_background()
chop_background_video(length)
final_video = make_final_video(number_of_comments)
