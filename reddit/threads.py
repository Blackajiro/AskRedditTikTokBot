import sys

from utils.console import print_markdown, print_step, print_substep
import praw
import random
import os
import json


def get_threads():
    print_step("Getting threads")

    content = {}

    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="Accessing threads",
        username=os.getenv("REDDIT_USERNAME"),
        password=os.getenv("REDDIT_PASSWORD"),
    )

    #Il primo arg può contenere il link al thread oppure il nome di un subreddit

    if len(sys.argv) > 1 and "www." in sys.argv[1]:
        submission = reddit.submission(url=sys.argv[1])
    else:
        if len(sys.argv) == 1:
            allowed_subreddits = json.loads(os.getenv("ALLOWED_SUBREDDITS"))
            subreddit = allowed_subreddits[random.randrange(0, len(allowed_subreddits)) - 1]
        else:
            subreddit = sys.argv[1]
        subreddit = reddit.subreddit(subreddit)
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