#!/usr/bin/env python3
import discord
from discord.ext import tasks
import datetime # have a date and time for the "entry to be send" line
import sqlite3 # backup rss feed into database
import requests # if we need to download image
import re # when we need to convert url with weird character into url encoded
import asyncio


# Discord Bot Token and Channel ID
DISCORD_TOKEN = "ADD_YOUR_DISCORD_TOKEN_HERE"
DISCORD_CHANNEL_ID = "ADD_YOUR_DISCORD_CHANNEL_ID_HERE"  # Replace with your channel ID

DEBUG = False
ALLOW_SEND = False
ALLOW_MARKED_SEND = True

# SQLite Database Setup
DB_FILE = f"{__file__.rsplit('/', 1)[0]}/../database/rss_feed.db"
DB_COLUMN_CHECK='sent_discord'
FETCH_INTERVAL = 600 # 10min



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



def init_database():
    """Initialize the SQLite database."""
    if DEBUG:
        print(f"path of DB_NAME is: [{ DB_FILE }]")
    conn = sqlite3.connect(DB_FILE, timeout=5)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    conn.close()

def mark_entry_as_sent(entry_id):
    """Mark an RSS entry as sent in the database."""
    conn = sqlite3.connect(DB_FILE, timeout=5)
    cursor = conn.cursor()
    cursor.execute(f'''
        UPDATE rss_entries
        SET {DB_COLUMN_CHECK} = 1
        WHERE id = ?;
    ''', (entry_id,))
    conn.commit()
    conn.close()

def get_unsent_entries():
    """Retrieve unsent RSS entries from the database."""
    conn = sqlite3.connect(DB_FILE, timeout=5)
    cursor = conn.cursor()
    cursor.execute(f'''
        SELECT id, sitename, title, link, summary, img
        FROM rss_entries
        WHERE {DB_COLUMN_CHECK} = 0;
    ''')
    unsent_entries = cursor.fetchall()
    conn.close()
    return unsent_entries



# Discord Client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def pull_and_send():
    await client.wait_until_ready()
    channel = client.get_channel(int(DISCORD_CHANNEL_ID))
    if channel is None:  # If the channel is not found
        print(f"Error: Could not find the channel with ID {DISCORD_CHANNEL_ID}")
        return

    while not client.is_closed():
        # Get feed from database that hasn't yet been sent.
        unsent_entries = get_unsent_entries()

        print(f"{datetime.datetime.now().strftime('%Y %b %d %H:%M:%S')}: entry to be send: {unsent_entries}")
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


            # Send the embed to the Discord channel
            if ALLOW_SEND:
                try:
                    await channel.send(
                            content=f"{link}",
                            embed=embed
                    )
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

        await asyncio.sleep(FETCH_INTERVAL)

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
        client.loop.create_task(pull_and_send())
        task_started = True


task_started = False
if __name__ == "__main__":
    init_database()
    # Run the bot
    client.run(DISCORD_TOKEN)

