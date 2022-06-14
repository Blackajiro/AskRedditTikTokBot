import os
import re

from gtts import gTTS
from pathlib import Path
from mutagen.mp3 import MP3
from utils.console import print_step, print_substep

from utils.arguments_manager import args_config
import pyttsx3
from datetime import datetime
import subprocess

from utils.explicit_content_manager import censor_sexual_words

#from pydub import AudioSegment
#import soundfile as sf
#import pyrubberband as pyrb


#def time_stretch_mp3(filename):
    #filepath = f"assets/mp3/{str(filename)}"

    #sound = AudioSegment.from_mp3(f"{filepath}.mp3")
    #sound.export(f"{filepath}.wav", format="wav")

    #y, sr = sf.read(f"{filepath}.wav")

    # Play back at 1.5X speed
    #y_stretch = pyrb.time_stretch(y, sr, 1.5)

    # Play back two 1.5x tones
    #y_shift = pyrb.pitch_shift(y, sr, 1.5)

    #sf.write(f"{filepath}.wav", y_stretch, sr, format='wav')

    #sound = AudioSegment.from_wav(f"{filepath}.wav")
    #sound.export(f"{filepath}.mp3", format="mp3")


def do_tts(string, title):
    print_substep('Generating ' + str(title) + '.mp3')

    length = 0
    if os.getenv("TTS_LIBRARY") == 'gtts':
        tts = gTTS(text=string, lang="en")
        tts.save(f"assets/mp3/{str(title)}.mp3")
        length = MP3(f"assets/mp3/{str(title)}.mp3").info.length
    elif os.getenv("TTS_LIBRARY") == 'pyttsx3':
        pyttsx3_tts(string, str(title))
        length = get_mp3_seconds(f"assets/mp3/{str(title)}.mp3")
    else:
        print("TTS_LIBRARY not defined")
        exit(-1)
    return length


def pyttsx3_tts(string, title):
    tts_engine = pyttsx3.init()
    if bool(os.getenv('TTS_VOICE')):
        tts_engine.setProperty('voice', os.getenv('TTS_VOICE'))
    tts_engine.save_to_file(string, f"assets/mp3/{title}.mp3")
    tts_engine.runAndWait()
    del tts_engine


def get_mp3_seconds(path):
    command = f"ffmpeg -i {path}"
    duration = subprocess.getoutput(command)
    i = duration.find("Duration: ") + len("Duration: ")
    duration = duration[i:]
    j = duration.find(',')
    duration = duration[3:j]
    td = datetime.strptime(duration, '%M:%S.%f') - datetime(1900, 1, 1, 0, 0, 0, 0)
    return td.total_seconds()


def save_text_to_mp3(reddit_obj):
    print_step("Converting text to mp3")

    length = 0

    # Create a folder for the mp3 files.
    Path("assets/mp3").mkdir(parents=True, exist_ok=True)

    # Title
    thread_title = censor_sexual_words(reddit_obj["thread_title"])
    thread_title = re.sub(r'http\S+', '', thread_title)
    length += do_tts(thread_title, 'title')

    # Body
    idx = 0
    if args_config['mode'] == 'ask':

        for comment in reddit_obj["comments"]:

            if length > args_config['length']:
                break

            if not ('deleted' in comment) and not ('removed' in comment):

                comment_body = censor_sexual_words(comment["comment_body"])
                comment_body = re.sub(r'http\S+', '', comment_body)

                if len(comment_body) < args_config['minchars'] or len(comment_body) > args_config[
                    'maxchars']:
                    continue

                length += do_tts(comment_body, idx)

                idx += 1

    elif args_config['mode'] == 'story':

        for sentence in reddit_obj["thread_selftext"]:
            length += do_tts(censor_sexual_words(sentence), idx)
            idx += 1

    else:
        exit(-1)

    # Done! return length and screen number
    print_substep(str(idx) + " strings processed")
    print_substep(str(length) + "s of total length")
    print_substep("Done!", style="bold green")

    return length, idx
