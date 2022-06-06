import sys

from dotenv import load_dotenv
from utils.console import *
from reddit.threads import *
from video_creation.background import *
from video_creation.voices import *
from video_creation.screenshot_downloader import *
from video_creation.final_video import *
from utils.arguments_manager import *

import threading
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox


class Gui:

    def __init__(self):
        load_dotenv()

        self.root = tk.Tk()
        self.root.geometry('550x320')
        self.root.title('AskReddit TikTok Bot')
        self.root.grid()

        self.curr_row = 0
        self.curr_padx = 10
        self.curr_pady = 10

        # Thread Type

        self.thread_type = tk.IntVar()
        self.thread_type_label = tk.Label(self.root, text='Thread Type:')
        self.thread_type_radio1 = tk.Radiobutton(self.root, text="Ask", variable=self.thread_type, value=1,
                                                 command=lambda: self.on_thread_type_change())
        self.thread_type_radio2 = tk.Radiobutton(self.root, text="Story", variable=self.thread_type, value=2,
                                                 command=lambda: self.on_thread_type_change())
        self.thread_type_label.grid(sticky='W', column=0, row=self.curr_row, padx=self.curr_padx, pady=self.curr_pady)
        self.thread_type_radio1.grid(sticky='W', column=1, row=self.curr_row, padx=self.curr_padx, pady=self.curr_pady)
        self.thread_type_radio2.grid(sticky='W', column=2, row=self.curr_row, padx=self.curr_padx, pady=self.curr_pady)

        # Source

        self.curr_row += 1

        self.source_label = tk.Label(self.root, text='Subreddit Name:')
        self.source = tk.Entry(self.root, width=40)
        self.source_label.grid(sticky='W', column=0, row=self.curr_row, padx=self.curr_padx, pady=self.curr_pady)
        self.source.grid(sticky='W', column=1, row=self.curr_row, padx=self.curr_padx, pady=self.curr_pady,
                         columnspan=3)

        # Url

        self.curr_row += 1

        self.url_label = tk.Label(self.root, text='Direct Url:')
        self.url = tk.Entry(self.root, width=40)
        self.url_label.grid(sticky='W', column=0, row=self.curr_row, padx=self.curr_padx, pady=self.curr_pady)
        self.url.grid(sticky='W', column=1, row=self.curr_row, padx=self.curr_padx, pady=self.curr_pady, columnspan=3)

        # Length

        self.curr_row += 1
        self.seconds_row = self.curr_row

        self.seconds_label = tk.Label(self.root, text='Video Length:')
        self.seconds = tk.Entry(self.root, width=5)
        self.seconds.insert(0, '40')

        # Minc / Maxc
        # Rendering with radio

        self.curr_row += 1
        self.minc_row = self.curr_row

        self.minc_label = tk.Label(self.root, text='Min Comment Chars:')
        self.minc = tk.Entry(self.root, width=5)
        self.minc.insert(0, '20')
        self.maxc_label = tk.Label(self.root, text='Max Comment Chars:')
        self.maxc = tk.Entry(self.root, width=5)
        self.maxc.insert(0, '250')

        # button

        self.curr_row += 2

        self.start_button = ttk.Button(
            self.root,
            text='Generate',
            command=lambda: self.on_generate()
        )
        self.start_button.grid(sticky='W', column=0, row=self.curr_row, padx=self.curr_padx, pady=self.curr_pady)

        # progressbar

        self.pb = ttk.Progressbar(
            self.root,
            orient='horizontal',
            mode='determinate',
            length=280
        )
        self.pb.grid(sticky='W', column=1, row=self.curr_row, padx=self.curr_padx, pady=self.curr_pady, columnspan=3)

        # status

        self.curr_row += 1

        self.text = tk.StringVar()
        self.text.set("")
        self.status_text = tk.Label(self.root, textvariable=self.text, fg='#32CD32')

        # Set default as ask
        self.thread_type.set(1)
        self.on_thread_type_change()

        self.root.mainloop()

    def on_thread_type_change(self):
        if self.thread_type.get() == 1:
            self.minc_label.grid(sticky='W', column=0, row=self.minc_row, padx=self.curr_padx, pady=self.curr_pady)
            self.minc.grid(sticky='W', column=1, row=self.minc_row, padx=self.curr_padx, pady=self.curr_pady)
            self.maxc_label.grid(sticky='W', column=2, row=self.minc_row, padx=self.curr_padx, pady=self.curr_pady)
            self.maxc.grid(sticky='W', column=3, row=self.minc_row, padx=self.curr_padx, pady=self.curr_pady)
            self.seconds_label.grid(sticky='W', column=0, row=self.seconds_row, padx=self.curr_padx, pady=self.curr_pady)
            self.seconds.grid(sticky='W', column=1, row=self.seconds_row, padx=self.curr_padx, pady=self.curr_pady)
        else:
            self.minc_label.grid_forget()
            self.minc.grid_forget()
            self.maxc_label.grid_forget()
            self.maxc.grid_forget()
            self.seconds_label.grid_forget()
            self.seconds.grid_forget()

    def on_generate(self):
        self.pb['value'] = 0
        self.start_button['state'] = tk.DISABLED
        self.status_text.grid(sticky='W', column=0, row=self.curr_row, padx=self.curr_padx, pady=0,
                              columnspan=4)
        t1 = threading.Thread(target=self.generate)
        t1.start()

    def update_step(self, text, progress_percentage):
        self.text.set(text)
        self.pb['value'] = progress_percentage

    def generate(self):

        args_config['source'] = self.source.get()
        args_config['url'] = self.url.get()
        if args_config['source'] == '' and args_config['url'] == '':
            args_config['source'] = 'askreddit'

        args_config['length'] = int(self.seconds.get())
        args_config['minc'] = int(self.minc.get())
        args_config['maxc'] = int(self.maxc.get())

        try:

            # Backgrounds
            self.update_step('Downloading Background...', 0)
            download_background()
            self.update_step('Downloading Background Audio...', 15)
            download_background_audio()

            # Thread
            self.update_step('Getting Thread...', 30)
            reddit_object = get_threads()

            # Audio and Video process
            self.update_step('Generating TTS...', 50)
            length, number_of_comments = save_text_to_mp3(reddit_object)
            self.update_step('Taking Screenshots...', 60)
            download_screenshots_of_reddit_posts(reddit_object, number_of_comments)
            self.update_step('Processing Background...', 80)
            chop_background_video(length)
            self.update_step('Processing Background Audio...', 80)
            chop_background_audio(length)

            # Final editing
            self.update_step('Generating Final Video...', 90)
            make_final_video(number_of_comments)

            self.update_step('Done!', 100)

        except Exception as e:
            tk.messagebox.showinfo("Exception",  str(e))
            self.update_step('', 0)
            self.status_text.grid_forget()

        self.start_button['state'] = tk.ACTIVE


App = Gui()
