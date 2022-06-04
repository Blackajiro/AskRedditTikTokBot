import os
import random

from utils.arguments_manager import args_config
import praw
from utils.console import print_step, print_substep


def get_threads():
    print_step("Getting thread")

    content = {}

    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="Accessing threads",
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
    )

    if bool(args_config['url']):
        submission = reddit.submission(url=args_config['url'])
    else:
        subreddit = reddit.subreddit(args_config['source'])
        threads = subreddit.hot(limit=25)
        submission = list(threads)[random.randrange(0, 25)]

    print_substep(f"Thread found: {submission.title}")

    try:

        content["thread_url"] = submission.url
        content["thread_title"] = submission.title
        content["comments"] = []

        for top_level_comment in submission.comments:
            content["comments"].append(
                {
                    "comment_body": top_level_comment.body,
                    "comment_url": top_level_comment.permalink,
                    "comment_id": top_level_comment.id,
                }
            )

    except AttributeError as e:
        pass

    print_substep("Done!", style="bold green")
    return content