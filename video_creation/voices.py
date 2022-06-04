import os

from gtts import gTTS
from pathlib import Path
from mutagen.mp3 import MP3
from utils.console import print_step, print_substep

from utils.arguments_manager import args_config
import pyttsx3
from datetime import datetime
import subprocess


def get_mp3_seconds(path):
    command = f"ffmpeg -i {path}"
    duration = subprocess.getoutput(command)
    i = duration.find("Duration: ") + len("Duration: ")
    duration = duration[i:]
    j = duration.find(',')
    duration = duration[3:j]
    td = datetime.strptime(duration, '%M:%S.%f') - datetime(1900, 1, 1)
    return td.total_seconds()


def save_text_to_mp3(reddit_obj):
    print_step("Converting text to mp3")
    engine = pyttsx3.init()
    length = 0

    # Create a folder for the mp3 files.
    Path("assets/mp3").mkdir(parents=True, exist_ok=True)

    # Title
    if os.getenv("TTS_LIBRARY") == 'gtts':
        tts = gTTS(text=reddit_obj["thread_title"], lang="en")
        tts.save(f"assets/mp3/title.mp3")
        length += MP3(f"assets/mp3/title.mp3").info.length
    elif os.getenv("TTS_LIBRARY") == 'pyttsx3':
        engine.save_to_file(reddit_obj["thread_title"], f"assets/mp3/title.mp3")
        engine.runAndWait()
        length += get_mp3_seconds(f"assets/mp3/title.mp3")
    else:
        print("TTS_LIBRARY not defined")
        exit(-1)

    # Comments
    idx = 0
    for comment in reddit_obj["comments"]:

        if length > args_config['length']:
            break
        if not ('deleted' in comment) and not ('removed' in comment):
            if len(comment["comment_body"]) < args_config['minchars'] or len(comment["comment_body"]) > args_config['maxchars']:
                continue
            if os.getenv("TTS_LIBRARY") == 'gtts':
                tts = gTTS(text=comment["comment_body"], lang="en")
                tts.save(f"assets/mp3/{str(idx)}.mp3")
                length += MP3(f"assets/mp3/{str(idx)}.mp3").info.length
            elif os.getenv("TTS_LIBRARY") == 'pyttsx3':
                engine.save_to_file(comment["comment_body"], f"assets/mp3/{str(idx)}.mp3")
                engine.runAndWait()
                length += get_mp3_seconds(f"assets/mp3/{str(idx)}.mp3")
            idx += 1

    # Done! return length and screen number

    print_substep(str(idx) + " comments processed")
    print_substep(str(length) + "s of total length")
    print_substep("Done!", style="bold green")

    return length, idx
