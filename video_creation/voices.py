import os

from gtts import gTTS
from pathlib import Path
from mutagen.mp3 import MP3
from utils.console import print_step, print_substep
from rich.progress import track


def save_text_to_mp3(reddit_obj):
    print_step("Converting text to mp3")
    length = 0

    # Create a folder for the mp3 files.
    Path("assets/mp3").mkdir(parents=True, exist_ok=True)

    tts = gTTS(text=reddit_obj["thread_title"], lang="en")
    tts.save(f"assets/mp3/title.mp3")
    length += MP3(f"assets/mp3/title.mp3").info.length

    idx = 0
    for comment in reddit_obj["comments"]:

        if length > int(os.getenv("MAX_SECONDS")):
            break

        if len(comment["comment_body"]) > int(os.getenv("MAX_COMMENT_CHARS")):
            continue

        tts = gTTS(text=comment["comment_body"], lang="en")
        tts.save(f"assets/mp3/{str(idx)}.mp3")
        length += MP3(f"assets/mp3/{str(idx)}.mp3").info.length

        idx += 1

    print_substep(str(idx) + " comments processed")
    print_substep(str(length) + "s of total length")
    print_substep("Done!", style="bold green")

    # ! Return the index so we know how many screenshots of comments we need to make.
    return length, idx
