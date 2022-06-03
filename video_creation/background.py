import os
from random import randrange

from moviepy.audio.io.AudioFileClip import AudioFileClip
from pytube import YouTube
from pathlib import Path
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip
from utils.console import print_step, print_substep


def get_start_and_end_times(video_length, length_of_clip):
    #random_time = randrange(180, int(length_of_clip) - int(video_length))
    random_time = randrange(180, int(length_of_clip) - int(video_length))
    return random_time, random_time + video_length


def download_background():
    print_step("Background video")
    if not Path("assets/mp4/background.mp4").is_file():
        print_substep("Downloading background, this may take a while...")
        YouTube(os.getenv("BACKGROUND_VIDEO_URL")).streams.filter(
            res="720p"
        ).first().download(
            "assets/mp4",
            filename="background.mp4",
        )
    else:
        print_substep("Background found, download not needed")

    print_substep("Done!", style="bold green")


def download_background_audio():
    print_step("Background audio")

    if os.getenv('BACKGROUND_AUDIO_URL') == '':
        print_substep("Background audio disabled")
    else:
        if not Path("assets/mp3/background_audio.mp3").is_file():
            print_substep("Downloading background audio, this may take a while...")
            YouTube(os.getenv('BACKGROUND_AUDIO_URL')).streams.filter(
                only_audio=True
            ).first().download(
                "assets/mp3",
                filename="background_audio.mp3",
            )
        else:
            print_substep("Background audio found, download not needed")

    print_substep("Done!", style="bold green")


def chop_background_video(video_length):
    print_substep("Processing background")

    background = VideoFileClip("assets/mp4/background.mp4")
    start_time, end_time = get_start_and_end_times(video_length + 1, background.duration)
    ffmpeg_extract_subclip(
        "assets/mp4/background.mp4",
        start_time,
        end_time,
        targetname="assets/mp4/clip.mp4",
    )

    print_substep("Done!", style="bold green")


def chop_background_audio(video_length):
    if os.getenv('BACKGROUND_AUDIO_URL') != '':
        print_substep("Processing background audio")

        background = AudioFileClip("assets/mp3/background_audio.mp3")
        start_time, end_time = get_start_and_end_times(video_length + 1, background.duration)
        background = background.subclip(start_time, end_time)
        background.write_audiofile("assets/mp3/clip.mp3")

        print_substep("Done!", style="bold green")
