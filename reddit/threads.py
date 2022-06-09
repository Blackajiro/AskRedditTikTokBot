import os
import random

from utils.arguments_manager import args_config
import praw
from utils.console import print_step, print_substep
import nltk.data
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
        #nltk.download()
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = tokenizer.tokenize(submission.selftext) #  this is the post text
        content["thread_title"] = submission.title
        content["comments"] = []

        max_sentence_len = 0
        for s in sentences:
            max_sentence_len = max(max_sentence_len, len(s))
        chars_per_screen = 400
        if max_sentence_len > chars_per_screen:
            print("Sentences are too long")
            exit(-1)
        i = 0
        j = 0
        chars = 0
        content['thread_selftext'] = ['']
        while i < len(sentences):
            chars += len(sentences[i])
            if chars > chars_per_screen:
                chars = 0
                j += 1
                content['thread_selftext'].append('')
            else:
                content['thread_selftext'][j] += sentences[i] + ' '
                i += 1

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