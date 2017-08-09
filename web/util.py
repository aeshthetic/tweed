import json
import os
import sys
import subprocess
import tweepy
import requests

auth = tweepy.OAuthHandler(
    os.environ['CONSUMER_KEY'], os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_TOKEN'],
                      os.environ['ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth)

SCRAPY_SPIDERS = (
    "profile_spider",
)

SCRAPY_DIR = os.path.join(
    os.path.abspath(os.path.pardir), "app", "scraper"
)

REFERENCE_DIR = os.path.join(
    os.path.abspath(os.path.pardir), "app", "data"
)

INITIAL_DIR = os.getcwd()


def run_spider(spider_name: str):
    """
    Runs a single spider and outputs
    to a JSON file. Log levels are
    set to WARN to reduce clutter.
    """

    spider_file_name = spider_name.lower() + ".json"
    spider_path = os.path.join(REFERENCE_DIR, spider_file_name)

    if os.path.exists(spider_path):
        os.remove(spider_path)
        print(f"Removed existing reference file {spider_file_name}.")

    subprocess.Popen(
        [
            "python3", "-m",
            "scrapy", "crawl", spider_name,
            "--loglevel", "WARN",
            "-o", spider_path
        ],
        stdout=sys.stdout,
        stderr=sys.stderr
    ).communicate()


def scrape_data():
    """
    Runs all spiders specified above
    and informs the user about the start
    and end of each spider.
    """

    print("Changing to scrapy directory...")
    os.chdir(SCRAPY_DIR)

    for spider in SCRAPY_SPIDERS:
        print(f"Running Spider {spider}... ")
        run_spider(spider)
        print("Done.")
    print("Scraping done. Changing back to initial directory.")
    os.chdir(INITIAL_DIR)


def tweets():
    """Collects oembed links and timestamps
    of the newest posts on twice's timeline
    and returns an array of dicts containing
    type timestamp and oembedlink"""
    timeline = api.user_timeline("jypetwice")
    ids = [status.id_str for status in timeline]
    links = [
        f"https://publish.twitter.com/oembed?url=https://twitter.com/JYPETWICE/status/{id}" for id in ids]
    objects = [json.loads(requests.get(link).content) if requests.get(
        link).status_code == 200 else "<p>Embed not found</p>" for link in links]
    timestamps = [status.created_at for status in timeline]
    embeds = [obj['html'] for obj in objects]
    return [{"type": "tweet", "embed": embed, "timestamp": timestamp} for (embed, timestamp) in dict(zip(embeds, timestamps)).items()]
