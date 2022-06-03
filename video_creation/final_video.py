import os

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    concatenate_videoclips,
    concatenate_audioclips,
    CompositeAudioClip,
    CompositeVideoClip,

)
from moviepy.audio.fx.volumex import volumex
import skimage
from moviepy.video.fx.crop import crop
from moviepy.video.fx.resize import resize

from utils.console import print_step

W, H = 1080, 1920


def blur(image):
    return skimage.filters.gaussian(image.astype(float), sigma=int(os.getenv("GAUSSIAN_BLUR_SIGMA")))


def make_final_video(number_of_clips):
    print_step("Creating the final video")

    # Init background clip
    background_clip = VideoFileClip("assets/mp4/clip.mp4", audio=False)

    # Adding background audio
    if os.getenv('BACKGROUND_AUDIO_URL') != '':
        background_audio_clip = AudioFileClip("assets/mp3/clip.mp3")
        new_audioclip = CompositeAudioClip([background_audio_clip]).fx(volumex, 0.3)
        background_clip.audio = new_audioclip

    # vfx
    if os.getenv('GAUSSIAN_BLUR_SIGMA') != 0:
        background_clip.fl_image(blur)

    # Resizing
    background_clip = resize(background_clip, height=H)
    background_clip = crop(background_clip, x1=1166.6, y1=0, x2=2246.6, y2=1920)

    # Gather all audio clips
    audio_clips = []
    for i in range(0, number_of_clips):
        audio_clips.append(AudioFileClip(f"assets/mp3/{i}.mp3"))
    audio_clips.insert(0, AudioFileClip(f"assets/mp3/title.mp3"))
    audio_concat = concatenate_audioclips(audio_clips)
    audio_composite = CompositeAudioClip([audio_concat])

    # Gather all images
    image_clips = []
    for i in range(0, number_of_clips):
        image_clips.append(
            ImageClip(f"assets/png/comment_{i}.png")
                .set_duration(audio_clips[i + 1].duration)
                .set_position("center")
                .resize(width=W - 100),
        )

    # Adding title image
    image_clips.insert(
        0,
        ImageClip(f"assets/png/title.png")
            .set_duration(audio_clips[0].duration)
            .set_position("center")
            .resize(width=W - 100),
    )

    image_concat = concatenate_videoclips(image_clips).set_position(
        ("center", "center")
    )
    image_concat.audio = audio_composite

    final = CompositeVideoClip([background_clip, image_concat])
    final.write_videofile(
        "assets/final_video.mp4", fps=30, audio_codec="aac", audio_bitrate="192k"
    )

    for i in range(0, number_of_clips):
        pass
