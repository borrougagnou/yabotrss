#!/usr/bin/env python3
import datetime # have a date and time for the "Synchronized" line
import sqlite3 # backup rss feed into database
import requests # if we need to download image
import urllib.parse # when we need to convert url with weird character into url encoded
import feedparser # parse rss feed
import asyncio

from bs4 import BeautifulSoup # parse html for parse_html
from html import unescape # clean html
import re # clean html


DEBUG = False
SHOW_SKIPPED = True

# SQLite Database Setup
DB_FILE = f"{__file__.rsplit('/', 1)[0]}/../database/rss_feed.db"
FETCH_INTERVAL = 600 # 10min

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

async def fetch_thehackernews_entries(feed_url: str, sitename: str):
    """Fetch entries from The Hacker News RSS feed."""
    feed = await asyncio.to_thread(feedparser.parse, feed_url)
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
        await asyncio.to_thread(save_entry, entry.id, sitename, entry.title, entry.link, summary, img)
    return

async def fetch_devto_entries(feed_url: str, sitename: str):
    """Fetch entries from Dev.to RSS feed."""
    feed = await asyncio.to_thread(feedparser.parse, feed_url)
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
        await asyncio.to_thread(save_entry, entry.id, f"{sitename} - {entry.author}", entry.title, entry.link, summary, img)
    return

async def fetch_waylonwalker_entries(feed_url: str, sitename: str):
    """Fetch entries from Waylon Walker RSS feed."""
    feed = await asyncio.to_thread(feedparser.parse, feed_url)
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
        await asyncio.to_thread(save_entry, entry.id, sitename, entry.title, entry.link, summary, img)
    return

async def fetch_theverge_entries(feed_url: str, sitename: str):
    """Fetch entries from The Verge RSS feed."""
    feed = await asyncio.to_thread(feedparser.parse, feed_url)
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
        await asyncio.to_thread(save_entry, entry.id, sitename, entry.title, entry.link, summary, img)
    return

async def fetch_arstechnica_entries(feed_url: str, sitename: str):
    """Fetch entries from ArsTechnica RSS feed."""
    feed = await asyncio.to_thread(feedparser.parse, feed_url)
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
        await asyncio.to_thread(save_entry, entry.id, sitename, entry.title, entry.link, summary, img)
    return

async def fetch_medium_entries(feed_url: str, sitename: str):
    """Fetch entries from <NAME> RSS feed."""
    feed = await asyncio.to_thread(feedparser.parse, feed_url)
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
        soup = await asyncio.to_thread(BeautifulSoup, entry.summary, 'html.parser')
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
        await asyncio.to_thread(save_entry, entry.id, f"{sitename} - {entry.author}", entry.title, entry.link, summary, img)
    return

#async def fetch_TEMPLATE_entries(feed_url: str, sitename: str):
#    """Fetch entries from <NAME> RSS feed."""
#    feed = await asyncio.to_thread(feedparser.parse, feed_url)
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
#        soup = await asyncio.to_thread(BeautifulSoup, entry.summary, 'html.parser')
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
#        await asyncio.to_thread(save_entry, entry.id, sitename, entry.title, entry.link, summary, img)
#    return


##########################

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


def handler_rss_feed_exception(loop, context):
    msg = context.get("exception", context["message"])
    print(f"{datetime.datetime.now().strftime('%Y %b %d %H:%M:%S')}: Caught exception in event loop:", msg)

async def fetch_rss_feeds():
    while True:
        try:
            # Collect all tasks for fetching feeds
            tasks = [
                    globals()[feed["function"]](feed["url"], feed["name"])
                    for feed in RSS_FEED_URLS
            ]

            # Run all tasks concurrently, log any failures but don’t kill the loop
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for index, error in enumerate(results):
                if isinstance(error, Exception):
                    print(f"{datetime.datetime.now().strftime('%Y %b %d %H:%M:%S')}: ERROR [{RSS_FEED_URLS[index]}]: ", error)

            print(f"{datetime.datetime.now().strftime('%Y %b %d %H:%M:%S')}: Synchronized")
        except Exception as e:
            print(f"{datetime.datetime.now().strftime('%Y %b %d %H:%M:%S')}: Error in fetch loop:", e)
        finally:
            await asyncio.sleep(FETCH_INTERVAL)


if __name__ == "__main__":
    init_database()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handler_rss_feed_exception)
    loop.run_until_complete(fetch_rss_feeds())
    #asyncio.run(fetch_rss_feeds())

