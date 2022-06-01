# AskReddit TikTok Bot

Based on elebumm's RedditVideoMakerBot

## Requirements

- Python 3.6+
- Playwright
- ffmpeg
- Reddit app

## Installation

1. Clone this repository
2. Rename `.env.template` to `.env` and replace all values with the appropriate fields. To get Reddit keys (**required**), visit [the Reddit Apps page.](https://www.reddit.com/prefs/apps). Set up a script, enter localhost:8080 as uri and copy user and secret.
3. Run `pip3 install -r requirements.txt`

## Usage

1. Customize .env with length, allowed subreddits and the background video url
2. Run `python3 main.py`
3. Let the script do the magic
4. Done!

You can pass an argument to force a specific subreddit or thread:
- `python3 main.py askreddit`
- `python3 main.py https://www.reddit.com/yourthread`