#!/usr/bin/env python3
import discord
from discord.ext import tasks
import sqlite3 # backup rss feed into database
import requests # if we need to download image
import base64 # if image need to be converted in base64
from io import BytesIO # (to base64) binary stream using an in-memory bytes buffer
import feedparser # parse rss feed

from bs4 import BeautifulSoup # parse html for parse_html
from html import unescape # clean html
import re # clean html and convert url with weird character into url encoded

DEBUG = False
ALLOW_SEND = False
ALLOW_MARKED_SEND = True
SHOW_SKIPPED = False

# Discord Bot Token and Channel ID
DISCORD_TOKEN = "ADD_YOUR_DISCORD_TOKEN_HERE"
DISCORD_CHANNEL_ID = "ADD_YOUR_DISCORD_CHANNEL_ID_HERE"  # Replace with your channel ID

# SQLite Database Setup
DB_FILE = "rss_feed.db"

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

def fetch_arstechnica_entries(feed_url, sitename):
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
            #img=custom_encode(entry.media_content[0]['url'])

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
    """Fetch entries from <NAME> RSS feed."""
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
                  #f"-DESC:  [{entry.summary_detail.type}][{summary[:80]}]\n"
                  f"-DESC:  [{summary[:80]}]\n"
                  f"-IMG:   [{img}]\n"
                  f"==========\n\n")

        # Save entry to the database
        save_entry(entry.id, f"{sitename} - {entry.author}", entry.title, entry.link, summary, img)
    return

#def fetch_TEMPLATE_entries(feed_url: str, sitename: str):
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
    try:
        response = requests.head(image_url, allow_redirects=True, timeout=5)
        # If the server refuses HEAD, fall back to GET
        if response.status_code == 405:
            response = requests.get(image_url, stream=True, timeout=5)
    except requests.RequestException:
        # network error, timeout, DNS failure, etc.
        return False

    content_type = response.headers.get('Content-Type', '')
    if DEBUG:
        print("IMAGE_URL:", image_url)
        print("STATUS_CODE:", response.status_code)
        print("CONTENT_TYPE:", content_type)

    if content_type.startswith('image/'):
        return True
    return False

def custom_encode(url: str) -> str:
    unreserved = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' + '0123456789' + "-._~"
    custom_safe_characters = ":/.?&#-_=+"

    safe_characters = set(unreserved + custom_safe_characters)

    # matches valid percent‑encodings "%2F", "%E2", etc.
    PERCENT_ENCODED_PATTERN = re.compile(r'%[0-9A-Fa-f]{2}')

    encoded_url = ""
    i = 0
    n = len(url)
    while i < n:
        char = url[i]

        if char == '%' and i + 2 < n and PERCENT_ENCODED_PATTERN.match(url[i:i+3]):
            encoded_url += f"{url[i:i+3]}"
            i += 3
            continue
        elif char in safe_characters:
            encoded_url += char  # Keep the safe characters as they are
        else:
            # Percent-encode each byte of the UTF-8 representation
            for byte in char.encode('utf-8'):
                encoded_url += f"%{byte:02X}"

        i += 1

    if DEBUG:
        print(f"encoded_url: [{encoded_url}]")
    return encoded_url

# NOT USED YET
def convert_image_to_base64(image_url):
    """Convert an image URL to Base64."""
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image = BytesIO(response.content)
        base64_image = base64.b64encode(image.read()).decode('utf-8')
        return base64_image
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None




def initialize_database():
    """Initialize the SQLite database."""
    conn = sqlite3.connect(DB_FILE, timeout=5)
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
            sent          BOOLEAN DEFAULT 0,
            timestamp     DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_entry(entry_id: str, sitename: str, title: str, link: str, summary: str, img: str):
    """Save a new RSS entry into the database."""
    conn = sqlite3.connect(DB_FILE, timeout=5)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO rss_entries (id, sitename, title, link, summary, img)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (entry_id, sitename, title[:250], link, summary[:4000], img))
    conn.commit()
    conn.close()

def mark_entry_as_sent(entry_id):
    """Mark an RSS entry as sent in the database."""
    conn = sqlite3.connect(DB_FILE, timeout=5)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE rss_entries
        SET sent = 1
        WHERE id = ?
    ''', (entry_id,))
    conn.commit()
    conn.close()

def get_unsent_entries():
    """Retrieve unsent RSS entries from the database."""
    conn = sqlite3.connect(DB_FILE, timeout=5)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, sitename, title, link, summary, img
        FROM rss_entries
        WHERE sent = 0
    ''')
    unsent_entries = cursor.fetchall()
    conn.close()
    return unsent_entries



# Initialize the database
initialize_database()

# Discord Client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@tasks.loop(minutes=10)  # Check for new entries every 10 minutes
async def fetch_rss_feeds():
    channel = client.get_channel(int(DISCORD_CHANNEL_ID))
    if channel is None:  # If the channel is not found
        print(f"Error: Could not find the channel with ID {DISCORD_CHANNEL_ID}")
        return

    for feed in RSS_FEED_URLS:
        feed_name = feed["name"]
        feed_url  = feed["url"]
        function_name = feed["function"]

        # Dynamically call the associated function for each feed
        entries = globals()[function_name](feed_url, feed_name)


    # Send unsent entries
    unsent_entries = get_unsent_entries()

    print(f"entry to be send: {unsent_entries}")
    for entry_id, sitename, title, link, summary, img in unsent_entries:
        # Create a rich embed
        if summary == "none":
            embed = discord.Embed(
                title=title,
                url=link,
                color=0xffffff  # Use white color
            )
        else:
            embed = discord.Embed(
                title=title,
                url=link,
                description=summary,  # Description from RSS
                color=0xffffff  # Use white color
            )

        # Add website name at the top of the posts
        embed.set_author(name=f"{sitename}")

        # Add an image if available
        if img and is_url_image(img):
            img=custom_encode(img)
            embed.set_image(url=f"{img}")
        # embed.set_image(url=entry.media_content[0]['url'])


        # Send the embed to the Discord channel
        if ALLOW_SEND:
            try:
                await channel.send(
                        content=f"{link}",
                        embed=embed
                )
                #await channel.send(embed=embed)
                if ALLOW_MARKED_SEND:
                    # Mark the entry as sent in the database
                    mark_entry_as_sent(entry_id)
                    print(f"done: {entry_id}")
            except Exception as e:
                print("==========")
                print(f"ERROR WITH ID: {entry_id}")
                print(e)
                print("==========")
        else:
            if ALLOW_MARKED_SEND:
                # Mark the entry as sent in the database
                mark_entry_as_sent(entry_id)
                print(f"done: {entry_id}")



@client.event
async def on_ready():
    global task_started
    print(f"Logged in as {client.user}")

    if DEBUG:
        print("DEBUG enabled !")
        text_channel_list = []
        for guild in client.guilds:
           for channel in guild.text_channels:
              text_channel_list.append(channel)
              print(f"{guild.name}\t| {channel.id}\t| {channel}")

    # The first time the bot connects, Any time it reconnects (due to Discord downtime or internet hiccups).
    if not task_started:
        client.loop.create_task(fetch_rss_feeds())
        task_started = True
    #fetch_rss_feeds.start()


task_started = False
if __name__ == "__main__":
    initialize_database()
    # Run the bot
    client.run(DISCORD_TOKEN)

