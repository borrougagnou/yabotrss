#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor, as_completed # implement threading
import logging # implement log system
import sys # for the log file
import time # sleep between each iteration
import datetime # have a date and time for the "Synchronized" line
import sqlite3 # backup rss feed into database
import requests # if we need to download image
import urllib.parse # when we need to convert url with weird character into url encoded
import feedparser # parse rss feed

from bs4 import BeautifulSoup # parse html for parse_html
from html import unescape # clean html
import re # clean html


DEBUG = False
SHOW_SKIPPED = True

# SQLite Database Setup
DB_FILE = f"{__file__.rsplit('/', 1)[0]}/../database/rss_feed.db"
FETCH_INTERVAL = 600 # 10min
THREAD_LIMIT = 6

# RSS Feed URL to Function Mapping
RSS_FEED_URLS = [
    {
        "name": "The Hacker News",
        "url": "https://thehackernews.com/rss.xml",
        "function": "fetch_thehackernews_entries"
    },
    {
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/features/index.xml",
        "function": "fetch_theverge_entries"
    },
    {
        "name": "dev.to",
        "url": "https://dev.to/feed",
        "function": "fetch_devto_entries"
    },
    {
        "name": "Waylonwalker",
        "url": "https://waylonwalker.com/archive/rss.xml",
        "function": "fetch_waylonwalker_entries"
    },
    {
        "name": "Ars Technica",
        "url": "https://feeds.arstechnica.com/arstechnica/index",
        "function": "fetch_arstechnica_entries"
    },
    {
        "name": "Medium",
        "url": "https://medium.com/feed/tag/servers",
        "function": "fetch_medium_entries"
    },
    # Add more RSS feeds and their functions here
]

##########################
### PARSE RSS FEED URL ###
##########################

def fetch_thehackernews_entries(feed_url: str, sitename: str):
    """Fetch entries from The Hacker News RSS feed."""
    feed = feedparser.parse(feed_url)
    #if DEBUG:
    #    entry = feed.entries[0]
    #    print(f"==========")
    #    print(f" - DEBUG ENTRY KEY: {entry.keys()}\n")
    #    print(f" - DEBUG ENTRY ALL: {entry}")
    #    print(f"==========")
    #    return

    for entry in feed.entries:
        if DEBUG:
            print(f"==========")
            print(f" - DEBUG ENTRY KEY: {entry.keys()}\n")
            print(f" - DEBUG ENTRY ALL: {entry}")

        # Skip if the title or description contains "ads"
        if " ads " in entry.title.lower() or " ads " in entry.summary.lower():
            if SHOW_SKIPPED:
                print(f"Skipped: [{sitename}] {entry.title}\n")
            continue

        # Manage the summary content
        summary = None
        summary = entry.summary

        # Manage the img content
        img = None
        # Find the first link with a valid image extension
        if hasattr(entry, "links"):
            for link_info in entry.links:
                if "type" in link_info and any(
                    ext in link_info["type"] for ext in ["jpeg", "jpg", "png", "webp"]
                ):
                    image_url = link_info["href"]
                    #img = "data:image/jpeg;base64," + convert_image_to_base64(image_url)
                    img = image_url
                    break

        if DEBUG:
            print(f"==========\n"
                  f"#### ENTRY FOR DDB:\n"
                  f"-SITE:  [{sitename}]\n"
                  f"-ID:    [{entry.id}]\n"
                  f"-LINK:  [{entry.link[:80]}]\n"
                  f"-TITLE: [{entry.title[:80]}]\n"
                  f"-DESC:  [{summary[:80]}]\n"
                  f"-IMG:   [{img}]\n"
                  f"==========\n\n")

        # Save entry to the database
        save_entry(entry.id, sitename, entry.title, entry.link, summary, img)
    return

def fetch_devto_entries(feed_url: str, sitename: str):
    """Fetch entries from Dev.to RSS feed."""
    feed = feedparser.parse(feed_url)
    #if DEBUG:
    #    entry = feed.entries[0]
    #    print(f"==========")
    #    print(f" - DEBUG ENTRY KEY: {entry.keys()}\n")
    #    print(f" - DEBUG ENTRY ALL: {entry}")
    #    print(f"==========")
    #    return

    for entry in feed.entries:
        if DEBUG:
            print(f"==========")
            print(f" - DEBUG ENTRY KEY: {entry.keys()}\n")
            print(f" - DEBUG ENTRY ALL: {entry}")

        # Skip if the title or description contains "ads"
        if " ads " in entry.title.lower() or " ads " in entry.summary.lower():
            if SHOW_SKIPPED:
                print(f"Skipped: [{sitename}] {entry.title}\n")
            continue

        # Manage the summary content
        summary = None
        summary = parse_html(entry.summary)  # Clean HTML from summary

        # Manage the img content
        img = None

        if DEBUG:
            print(f"==========\n"
                  f"#### ENTRY FOR DDB:\n"
                  f"-SITE:  [{sitename} - {entry.author}]\n"
                  f"-ID:    [{entry.id}]\n"
                  f"-LINK:  [{entry.link[:80]}]\n"
                  f"-TITLE: [{entry.title[:80]}]\n"
                  f"-DESC:  [{summary[:80]}]\n"
                  f"-IMG:   [{img}]\n"
                  f"==========\n\n")

        # Save entry to the database
        save_entry(entry.id, f"{sitename} - {entry.author}", entry.title, entry.link, summary, img)
    return

def fetch_waylonwalker_entries(feed_url: str, sitename: str):
    """Fetch entries from Waylon Walker RSS feed."""
    feed = feedparser.parse(feed_url)
    #if DEBUG:
    #    entry = feed.entries[0]
    #    print(f"==========")
    #    print(f" - DEBUG ENTRY KEY: {entry.keys()}\n")
    #    print(f" - DEBUG ENTRY ALL: {entry}")
    #    print(f"==========")
    #    return

    for entry in feed.entries:
        if DEBUG:
            print(f"==========")
            print(f" - DEBUG ENTRY KEY: {entry.keys()}\n")
            print(f" - DEBUG ENTRY ALL: {entry}")

        # Skip if the title or description contains "ads"
        if " ads " in entry.title.lower() or " ads " in entry.summary.lower():
            if SHOW_SKIPPED:
                print(f"Skipped: [{sitename}] {entry.title}\n")
            continue

        # Manage the summary content
        summary = None
        summary = entry.summary  # Clean HTML from summary

        # Manage the img content
        img = None
        # Find the first link with a valid image extension
        if hasattr(entry, "links"):
            for link_info in entry.links:
                if "type" in link_info and any(
                    ext in link_info["type"] for ext in ["jpeg", "jpg", "png", "webp"]
                ):
                    img = link_info["href"]
                    break

        if DEBUG:
            print(f"==========\n"
                  f"#### ENTRY FOR DDB:\n"
                  f"-SITE:  [{sitename}]\n"
                  f"-ID:    [{entry.id}]\n"
                  f"-LINK:  [{entry.link[:80]}]\n"
                  f"-TITLE: [{entry.title[:80]}]\n"
                  f"-DESC:  [{summary[:80]}]\n"
                  f"-IMG:   [{img}]\n"
                  f"==========\n\n")

        # Save entry to the database
        save_entry(entry.id, sitename, entry.title, entry.link, summary, img)
    return

def fetch_theverge_entries(feed_url: str, sitename: str):
    """Fetch entries from The Verge RSS feed."""
    feed = feedparser.parse(feed_url)
    #if DEBUG:
    #    entry = feed.entries[0]
    #    print(f"==========")
    #    print(f" - DEBUG ENTRY KEY: {entry.keys()}\n")
    #    print(f" - DEBUG ENTRY ALL: {entry}")
    #    print(f"==========")

    for entry in feed.entries:
        if DEBUG:
            print(f"==========")
            print(f" - DEBUG ENTRY KEY: {entry.keys()}\n")
            print(f" - DEBUG ENTRY ALL: {entry}")

        # Skip if the title or description contains "ads"
        if " ads " in entry.title.lower() or " ads" in entry.summary.lower():
            if SHOW_SKIPPED:
                print(f"Skipped: [{sitename}] {entry.title}\n")
            continue

        # Manage the summary content
        summary = None
        summary = parse_html(entry.summary)  # Clean HTML from summary

        # Manage the img content
        img = None
        img = parse_html_img(entry.summary) # Search IMG from summary

        if DEBUG:
            print(f"==========\n"
                  f"#### ENTRY FOR DDB:\n"
                  f"-SITE:  [{sitename}]\n"
                  f"-ID:    [{entry.id}]\n"
                  f"-LINK:  [{entry.link[:80]}]\n"
                  f"-TITLE: [{entry.title[:80]}]\n"
                  #f"-DESC:  [{entry.summary_detail.type}][{summary[:80]}]\n"
                  f"-DESC:  [{summary[:80]}]\n"
                  f"-IMG:   [{img}]\n"
                  f"==========\n\n")

        # Save entry to the database
        save_entry(entry.id, sitename, entry.title, entry.link, summary, img)
    return

def fetch_arstechnica_entries(feed_url: str, sitename: str):
    """Fetch entries from ArsTechnica RSS feed."""
    feed = feedparser.parse(feed_url)
#    if DEBUG:
#        entry = feed.entries[0]
#        print(f"==========")
#        print(f" - DEBUG ENTRY KEY: {entry.keys()}\n")
#        print(f" - DEBUG ENTRY ALL: {entry}")
#        print(f"==========")

    for entry in feed.entries:
        if DEBUG:
            print(f"==========")
            print(f" - DEBUG ENTRY KEY: {entry.keys()}\n")
            print(f" - DEBUG ENTRY ALL: {entry}")

        # Skip if the title or description contains "ads"
        if " ads " in entry.title.lower() or " ads " in entry.summary.lower():
            if SHOW_SKIPPED:
                print(f"Skipped: [{sitename}] {entry.title}\n")
            continue

        # Manage the summary content
        summary = None
        summary = parse_html(entry.summary)  # Clean HTML from summary

        # Manage the img content
        img = None
        # Add image if available
        if hasattr(entry, "media_content") and entry.media_content:
            img=entry.media_content[0]['url']

        if DEBUG:
            print(f"==========\n"
                  f"#### ENTRY FOR DDB:\n"
                  f"-SITE:  [{sitename}]\n"
                  f"-ID:    [{entry.id}]\n"
                  f"-LINK:  [{entry.link[:80]}]\n"
                  f"-TITLE: [{entry.title[:80]}]\n"
                  #f"-DESC:  [{entry.summary_detail.type}][{summary[:80]}]\n"
                  f"-DESC:  [{summary[:80]}]\n"
                  f"-IMG:   [{img}]\n"
                  f"==========\n\n")

        # Save entry to the database
        save_entry(entry.id, sitename, entry.title, entry.link, summary, img)
    return

def fetch_medium_entries(feed_url: str, sitename: str):
    """Fetch entries from Medium RSS feed."""
    feed = feedparser.parse(feed_url)
    #if DEBUG:
    #    entry = feed.entries[0]
    #    print(f"==========")
    #    print(f" - DEBUG ENTRY KEY: {entry.keys()}\n")
    #    print(f" - DEBUG ENTRY ALL: {entry}")
    #    print(f"==========")
    #    return

    for entry in feed.entries:
        if DEBUG:
            print(f"==========")
            print(f" - DEBUG ENTRY KEY: {entry.keys()}\n")
            print(f" - DEBUG ENTRY ALL: {entry}")

        # Skip if the title or description contains "ads"
        if "I will write hospitality".lower() in entry.title.lower():
            if SHOW_SKIPPED:
                print(f"Skipped: [{sitename}] {entry.title}\n")
            continue
        if "hosting".lower() in entry.title.lower():
            if SHOW_SKIPPED:
                print(f"Skipped: [{sitename}] {entry.title}\n")
            continue

        # Manage the summary content
        summary = None
        soup = BeautifulSoup(entry.summary, 'html.parser')
        summary = soup.get_text()
        summary = summary.replace('\n', '').replace('\r', '')
        summary = summary.replace('Continue reading on Medium', '').replace('»', '')

        # Manage the img content
        img = None
        if hasattr(entry, "media_content") and entry.media_content:
            img=entry.media_content[0]['url']
        elif hasattr(entry, "content") and entry.content:
            img=parse_html_img(entry.content[0]['value'])
        elif hasattr(entry, "summary") and entry.summary:
            img=parse_html_img(entry.summary)

        if DEBUG:
            print(f"==========\n"
                  f"#### ENTRY FOR DDB:\n"
                  f"-SITE:  [{sitename} - {entry.author}]\n"
                  f"-ID:    [{entry.id}]\n"
                  f"-LINK:  [{entry.link[:80]}]\n"
                  f"-TITLE: [{entry.title[:80]}]\n"
                  f"-DESC:  [{summary[:80]}]\n"
                  f"-IMG:   [{img}]\n"
                  f"==========\n\n")

        # Save entry to the database
        save_entry(entry.id, f"{sitename} - {entry.author}", entry.title, entry.link, summary, img)
    return

#async def fetch_TEMPLATE_entries(feed_url: str, sitename: str):
#    """Fetch entries from <NAME> RSS feed."""
#    feed = feedparser.parse(feed_url)
#    #if DEBUG:
#    #    entry = feed.entries[0]
#    #    print(f"==========")
#    #    print(f" - DEBUG ENTRY KEY: {entry.keys()}\n")
#    #    print(f" - DEBUG ENTRY ALL: {entry}")
#    #    print(f"==========")
#    #    return
#
#    for entry in feed.entries:
#        if DEBUG:
#            print(f"==========")
#            print(f" - DEBUG ENTRY KEY: {entry.keys()}\n")
#            print(f" - DEBUG ENTRY ALL: {entry}")
#
#        # Skip if the title or description contains "ads"
#        if " ads " in entry.title.lower() or " ads " in entry.summary.lower():
#            if SHOW_SKIPPED:
#                print(f"Skipped: [{sitename}] {entry.title}\n")
#            continue
#
#        # Manage the summary content
#        summary = None
#        soup = BeautifulSoup(entry.summary, 'html.parser')
#        summary = soup.get_text()
#        summary = summary.replace('\n', '').replace('\r', '')
#
#        # Manage the img content
#        img = None
#        if hasattr(entry, "media_content") and entry.media_content:
#            img=entry.media_content[0]['url']
#        elif hasattr(entry, "content") and entry.content:
#            img=parse_html_img(entry.content[0]['value'])
#        elif hasattr(entry, "summary") and entry.summary:
#            img=parse_html_img(entry.summary)
#
#        if DEBUG:
#            print(f"==========\n"
#                  f"#### ENTRY FOR DDB:\n"
#                  f"-SITE:  [{sitename}]\n"
#                  f"-ID:    [{entry.id}]\n"
#                  f"-LINK:  [{entry.link[:80]}]\n"
#                  f"-TITLE: [{entry.title[:80]}]\n"
#                  #f"-DESC:  [{entry.summary_detail.type}][{summary[:80]}]\n"
#                  f"-DESC:  [{summary[:80]}]\n"
#                  f"-IMG:   [{img}]\n"
#                  f"==========\n\n")
#
#        # Save entry to the database
#        save_entry(entry.id, sitename, entry.title, entry.link, summary, img)
#    return


##########################

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rss_fetcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def clean_html(raw_html: str) -> str:
    """Clean and decode HTML content."""
    cleanr = re.compile('<.*?>')  # Regex to remove HTML tags
    cleantext = re.sub(cleanr, '', str(raw_html))
    return unescape(cleantext)  # Decode HTML entities

def parse_html(raw_html: str) -> str:
    """Clean and decode HTML content."""
    soup = BeautifulSoup(raw_html, 'html.parser')
    #if soup.p is not None:
    if hasattr(soup, "p") and soup.p:
        try:
            return str(soup.p.get_text())
        except AttributeError:
            return "AttributeError"
    else:
        return str(clean_html(soup))

def parse_html_img(raw_html: str):
    """Clean and decode HTML content."""
    soup = BeautifulSoup(raw_html, 'html.parser')
    if hasattr(soup, "img") and soup.img:
        try:
            return soup.img['src']
        except AttributeError:
            return None
    else:
        return None

def is_url_image(image_url: str):
    response = requests.head(image_url, allow_redirects=True, timeout=5)
    content_type = response.headers.get('Content-Type', '')
    if content_type.startswith('image/'):
        return True
    return False

def custom_encode(url: str) -> str:
    safe_characters = ":/.?&#-_=+"

    # If the URL is already encoded, just return it
    if url == urllib.parse.unquote(url):
        return url

    # Function to encode only the "weird" characters
    encoded_url = ""

    # Iterate through each character in the URL
    for char in url:
        if char in safe_characters:
            encoded_url += char  # Keep the safe characters as they are
        else:
            # Encode the character and append to the result
            encoded_url += urllib.parse.quote(char)
    print(encoded_url)
    return encoded_url





def init_database():
    """Initialize the SQLite database."""
    if DEBUG:
        print(f"path of DB_NAME is: [{ DB_FILE }]")
    conn = sqlite3.connect(DB_FILE, timeout=5)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    cursor = conn.cursor()
    # Create table to store feed entries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rss_entries (
            id            TEXT PRIMARY KEY,
            sitename      TEXT,
            title         TEXT,
            link          TEXT,
            summary       TEXT,
            img           TEXT,
            timestamp     DATETIME DEFAULT CURRENT_TIMESTAMP,
            sent_discord  BOOLEAN DEFAULT 0,
            sent_slack    BOOLEAN DEFAULT 0,
            sent_telegram BOOLEAN DEFAULT 0,
            sent_other    BOOLEAN DEFAULT 0
        );
    ''')
    conn.commit()
    conn.close()

def save_entry(entry_id: str, sitename: str, title: str, link: str, summary: str, img: str):
    """Save a new RSS entry into the database."""
    conn = sqlite3.connect(DB_FILE, timeout=5)
    conn.execute("PRAGMA busy_timeout = 5000;")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO rss_entries (id, sitename, title, link, summary, img)
        VALUES (?, ?, ?, ?, ?, ?);
    ''', (entry_id, sitename, title[:250], link, summary[:4000], img)
    )
    conn.commit()
    conn.close()

def countdown_timer(ttl_seconds):
    while ttl_seconds > 0:
        # 365 days in a year
        years, time_remaining = divmod(ttl_seconds, 60 * 60 * 24 * 365)
        # 30 days in a month
        months, time_remaining = divmod(time_remaining, 60 * 60 * 24 * 30)
        # 7 days in a week
        weeks, time_remaining = divmod(time_remaining, 60 * 60 * 24 * 7)
        # 24 hours in a day
        days, time_remaining = divmod(time_remaining, 60 * 60 * 24)
        # 60 minutes in an hour
        hours, time_remaining = divmod(time_remaining, 60 * 60)
        # 60 seconds in a minute
        minutes, seconds = divmod(time_remaining, 60)

        countdown_str = "=== NEXT FETCH IN: "
        if years > 0:
            countdown_str += f"{years} year{'s' if years > 1 else ''}"
        elif months > 0:
            countdown_str += f"{months} month{'s' if months > 1 else ''}"
        elif weeks > 0:
            countdown_str += f"{weeks} week{'s' if weeks > 1 else ''}"
        elif days > 0:
            countdown_str += f"{days} day{'s' if days > 1 else ''}"
        elif hours > 0:
            countdown_str += f"{hours} hour{'s' if hours > 1 else ''}"
        elif minutes > 0:
            countdown_str += f"{minutes} minute{'s' if minutes > 1 else ''}"
        elif seconds > 0:
            countdown_str += f"{seconds} second{'s' if seconds > 1 else ''}"
        
        countdown_str += " ========================================"
        print(f"\r\033[K{countdown_str}", end="", flush=True)
        time.sleep(5)  # Wait for 5 seconds
        ttl_seconds -= 5  # Decrease the time by 5 seconds

    # Flush the countdown timer line and add "===" to separate each loop 
    print(f"\r\033[K===\n", end="", flush=True)




def fetch_rss_feeds():
    results = []
    with ThreadPoolExecutor(max_workers=THREAD_LIMIT) as executor:
        send_to_feed = {
            executor.submit(fetch_single_rss_feed, feed): feed['name']
            for feed in RSS_FEED_URLS
        }

        # Track completed and failed feeds
        completed_feeds = set()


        try:
            # Wait for all to complete
            # This timeout kills the entire loop if ANY feed takes >3min
            for future in as_completed(send_to_feed, timeout=180):
                feed_name = send_to_feed[future]
                try:
                    # Set a timeout PER FEED
                    result = future.result(timeout=120) # 2min per feed
                    if not result["success"]:
                        logger.error(f"[FAILED] {result['name']}: {result['error']}")
                except TimeoutError:
                    logger.error(f"[TIMEOUT] {feed_name}: TIMEOUT")
                except Exception as e:
                    logger.error(f"[ERROR] [{feed_name}] Exception: {e}")

        except concurrent.futures.TimeoutError as e:
            # This is the KEY !!: Handle timeout
            logger.error(f"Timeout waiting for feeds to complete: {e}")

            # Find which feeds didn't complete
            error_feeds = []
            for feed, future in send_to_feed.items():
                if feed['name'] not in completed_feeds:
                    error_feeds.append(feed)

            # Add timeout results for incomplete feeds
            for feed in error_feeds:
                results.append({
                    "name": feed["name"],
                    "function": feed["function"],
                    "success": False,
                    "error": f"Feed timeout after {timeout_per_feed}s"
                })
                logger.error(f"Feed {feed['name']} timed out and will be retried next cycle")

    return results


def fetch_single_rss_feed(feed):
    """
    Safely executes ANY feed function.
    Catches ALL errors so other threads continue even if one fails.
    """

    feed_name = feed.get("name", "Unknown")
    function_name = feed.get("function")
    feed_url = feed.get("url")
    result = {
        "name": feed_name,
        "function": function_name,
        "success": False,
        "error": None
    }

    try:
        logger.info(f"Executing {function_name} for {feed_name}")

        if function_name not in globals():
            raise ValueError(f"Function {function_name} not found")

        fetch_function = globals()[function_name]
        fetch_function(feed_url, feed_name)

        result["success"] = True
        logger.info(f"[OK] {feed_name} completed")

    except Exception as e:
        result["error"] = str(e)
        logger.error(f"[ERROR] {feed_name} FAILED: {e}", exc_info=True)
        # Don't use "raise", we want ALL errors visible

    return result


if __name__ == "__main__":
    # Initialize logging
    logger.info("RSS Fetcher starting...")

    try:
        init_database()
    except Exception as e:
        logger.critical(f"Database init failed, exiting: {e}")
        sys.exit(1)


    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "once":
            # Run all feed once and exit - GOOD FOR DEBUGGING
            logger.info("Running single fetch cycle")
            results = fetch_rss_feeds()

            for result in results:
                if result["error"]:
                    print(f"[ERROR]: {result['error']}")

        elif command == "continuous":
            # Run all feed continuously at specified intervals.
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else FETCH_INTERVAL
            logger.info(f"Running continuous fetch cycle (interval: {interval}s)")

            while True:
                try:
                    fetch_rss_feeds()
                except KeyboardInterrupt:
                    logger.info("Keyboard interrupt, shutting down...")
                    break
                except Exception as e:
                    logger.error(f"Unexpected error in fetch loop: {e}", exc_info=True)
                finally:
                    countdown_timer(interval)

        elif command == "test":
            # Test a SINGLE feed - BEST FOR DEBUGGING
            if len(sys.argv) < 3:
                print("Usage: python rss_fetcher.py test <feed_name>")
                sys.exit(1)

            feed_name = sys.argv[2]
            feed = next((f for f in RSS_FEED_URLS if f["name"] == feed_name), None)

            if not feed:
                print(f"Feed '{feed_name}' not found")
                print(f"Available: {', '.join(f['name'] for f in RSS_FEED_URLS)}")
                sys.exit(1)

            logger.info(f"Testing single feed: {feed_name}")
            result = fetch_single_rss_feed(feed)
            print(f"\nResult: {'Success' if result['success'] else 'Failed'}")
            if result['error']:
                print(f"Error: {result['error']}")

        else:
            print(f"Unknown command: {command}")
            print("\nUsage:")
            print("  python rss_fetcher.py once              - Run once and exit")
            print("  python rss_fetcher.py continuous [secs] - Run continuously")
            print("  python rss_fetcher.py test <feed_name>  - Test single feed")
            sys.exit(1)


    else:
        # Default: run once
        fetch_rss_feeds()

