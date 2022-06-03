import os

from gtts import gTTS
from pathlib import Path
from mutagen.mp3 import MP3
from utils.console import print_step, print_substep
from rich.progress import track
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
    engine = pyttsx3.init()

    #engine.save_to_file('Hello World', 'test.mp3')
    print_step("Converting text to mp3")
    length = 0

    # Create a folder for the mp3 files.
    Path("assets/mp3").mkdir(parents=True, exist_ok=True)

    #tts = gTTS(text=reddit_obj["thread_title"], lang="en")
    #tts.save(f"assets/mp3/title.mp3")
    engine.save_to_file(reddit_obj["thread_title"], f"assets/mp3/title.mp3")
    engine.runAndWait()

    length += get_mp3_seconds(f"assets/mp3/title.mp3")

    idx = 0
    for comment in reddit_obj["comments"]:

        if length > int(os.getenv("MAX_SECONDS")):
            break

        if len(comment["comment_body"]) > int(os.getenv("MAX_COMMENT_CHARS")):
            continue

        #tts = gTTS(text=comment["comment_body"], lang="en")
        #tts.save(f"assets/mp3/{str(idx)}.mp3")

        engine.save_to_file(comment["comment_body"], f"assets/mp3/{str(idx)}.mp3")
        engine.runAndWait()

        length += get_mp3_seconds(f"assets/mp3/{str(idx)}.mp3")

        idx += 1

    print_substep(str(idx) + " comments processed")
    print_substep(str(length) + "s of total length")
    print_substep("Done!", style="bold green")

    engine.runAndWait()
    ## ! Return the index so we know how many screenshots of comments we need to make.
    return length, idx
