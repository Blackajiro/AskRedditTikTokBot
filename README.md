# AskReddit TikTok Bot

## Requirements

- Python 3.6+
- Playwright
- ffmpeg
- Reddit account
- Reddit app

## Installation

1. Clone this repository
2. Rename `.env.template` to `.env` and replace all values with the appropriate fields. To get Reddit keys (**required**), visit [the Reddit Apps page.](https://www.reddit.com/prefs/apps) Set up a script, enter http://localhost:8080 as uri and copy user and secret.
3. Run `pip3 install -r requirements.txt`

## Usage

1. Customize .env
2. Run `python3 generate.py`
3. Let the script do the magic
4. Done!

`generate.py -h` for help