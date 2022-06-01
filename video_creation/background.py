import os
from random import randrange
from pytube import YouTube
from pathlib import Path
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
from utils.console import print_step, print_substep


def get_start_and_end_times(video_length, length_of_clip):
    random_time = randrange(180, int(length_of_clip) - int(video_length))
    return random_time, random_time + video_length


def download_background():
    if not Path("assets/mp4/background.mp4").is_file():
        print_step("Background video")
        print_substep("Downloading background, this may take a while...")
        YouTube(os.getenv("BACKGROUND_VIDEO_URL")).streams.filter(
            res="720p"
        ).first().download(
            "assets/mp4",
            filename="background.mp4",
        )

def chop_background_video(video_length):
    print_substep("Processing background")
    background = VideoFileClip("assets/mp4/background.mp4")

    start_time, end_time = get_start_and_end_times(video_length, background.duration)
    ffmpeg_extract_subclip(
        "assets/mp4/background.mp4",
        start_time,
        end_time,
        targetname="assets/mp4/clip.mp4",
    )
    print_substep("Done!", style="bold green")
