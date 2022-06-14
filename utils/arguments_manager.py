import argparse

parser = argparse.ArgumentParser(description="Generates TikTok videos from a specific source. "
                                             " Example: generate.py -u 'reddit.com/thread' -l 30 -t 3 --no-audio",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-m", "--mode", type=str, help="Mode: ask/story [default=ask]", default="ask")

parser.add_argument("-s", "--source", type=str, help="Subreddit name [default=askreddit]", default="nosleep")
parser.add_argument("-u", "--url", type=str, help="Direct url")
parser.add_argument("-t", "--times", type=int, help="Number of videos to generate [default=1]", default=1)

parser.add_argument("-l", "--length", type=int, help="Max seconds of video [default=40]", default=40)
parser.add_argument("-minc", "--minchars", type=int, help="Minum number of chars per comment [default=0]", default=0)
parser.add_argument("-maxc", "--maxchars", type=int, help="Maximum number of chars per comment [default=150]", default=200)

parser.add_argument("--no-transparency", action="store_true", help="Disable screenshots transparency")
parser.add_argument("--no-audio", action="store_true", help="Disable background audio")

global args_config
args_config = vars(parser.parse_args())

