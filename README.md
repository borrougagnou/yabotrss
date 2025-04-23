# Yet Another Bot RSS

This bot read RSS Flux from different source and send the title, description (and image maybe) on different platform.

![Example of Discord screenshot](/img/Example-on-Discord-YabootRSS.png)

it requier few skill in python language if you want add your own rss feed.


## Changelog
#### 20250424
- Update requirements.txt
- Fixed image bug with character encoding and image checking

#### 20250228
- Fixed if the img link not exist

#### 20250227
- Update requirements.txt
- Fixed "Medium" RSS - Skip

#### 20241227
- Added new Async file : `index_async.py`
- Blocking "Medium" Ads.
- Reformat README.md

#### 20241217
- Fixed "Medium" RSS
- Fixed Rich Embed showing `**` in the title


## Summary
- [YabotRSS](#yet-another-bot-rss)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Parallel Code Execution](#parallel-code-execution)
    - [Adding Discord Connections](#adding-discord-connections)
        - [Configure discord](#-configure-discord-)
        - [Configure bot for discord](#-configure-the-bot-for-discord-)
    - [First Step](#first-step-)
    - [Execution](#execution-)
    - [Adding New RSS Flux](#adding-new-rss-flux)
        - [RSS_FEED_URLS](#-rss_feed_urls-)
        - [PARSE RSS FEED URL](#--parse-rss-feed-url--)
    - [Disable existing RSS Flux](#disable-existing-rss-flux)
  - [Debug](#debug-)
  - [FAQ](#faq)


## Requirements

- Python 3.9+
- Account on one of a compatible website:
    - Discord: https://discord.com/developers/applications
    - Telegram: #TODO
    - Slack: #TODO


## Installation

- `git clone https://github.com/borrougagnou/yabotrss.git`
- `pip install -r requirements.txt`

## Usage
### Parallel Code Execution:
Now you have the choice between 2 bots:
- `index.py` - the script will fetch each feed, one by one
- `index_async.py` - the script will fetch each feed in parallels


### Adding Discord Connections:

#### > Configure Discord :
---
[Create A New Discord Application](https://discord.com/developers/applications?new_application=true)

      - Give it a name
      > "Installation":
          > "Installation Contexts":
              - Check "User Install"
              - Check "Guild Install"
          > "Default Install Settings":
              > "Guild Install":
                  - Scope: 'applications.command', 'bot'
                  - Permissions: 'Embed Links', 'Read Message History', 'Send Messages', 'Send Messages in Threads', 'View Channels'
      > "Bot":
          > Token: "Reset Token" :warning: put the new token in the "DISCORD_TOKEN" variable in the index.py file !
          > "Authorization Flow":
              - Check "Public Bot"
          > "Privileged Gateway Intents":
              - Check "Message Content Intent"

Now add your bot on your server
> [!IMPORTANT]
> Enable the "[Developper mode](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID)" in your discord client

#### > Configure the bot for discord :
---
- Copy your Discord Token. Get it from [Discord Developers Portal](https://discord.com/developers/applications)

      > <your discord app>
          > "Bot" (left menu):
              > Token: "Reset Token" and copy the new one !

- Found a discord channel : [How to find the Channel ID number](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID)
-  Open and edit the `index.py` or the `index_async.py` file and put your:
   ```python
   # Discord Bot Token and Channel ID
   DISCORD_TOKEN = "ADD_YOUR_DISCORD_TOKEN_HERE" 
   DISCORD_CHANNEL_ID = "ADD_YOUR_DISCORD_CHANNEL_ID_HERE"  # Replace with your channel ID
   ```

### First Step :
> [!WARNING]
> The script need to generate a database with all feed, but at this step, the bot don't know what feed was already sent on platform or no.

To prevent a flood (and a ban from the platform) edit the bot and change the variable:
```python
ALLOW_SEND = False
```
Execute the bot: `python3 index.py` or `python3 index_async.py`.

Wait few second after the last "`Done: XXX`", then exit the bot by pressing CTRL+C

### Execution :
Change the variable:
```python
ALLOW_SEND = True
```
save and execute again: `python3 index.py` or `python3 index_async.py`.

Let the script running

### Adding New RSS Flux
> [!IMPORTANT]
> This step require to have few skill in Python language.

There are 2 places you need to check:
<br/>

#### > "<ins>RSS_FEED_URLS</ins>" :
Contain all the RSS feed the boot will parse, you will see:
 - `name` : a name of the website you want parse (eg: Ars Technica)
 - `url` : the url of the feed (on some website you can found it in the footer of the website)
 - `function` : it's a Dynamic Function Call, it contain the function name of the parser engine.


#### > "<ins>### PARSE RSS FEED URL ###</ins>" :
This part of the script contain engine for each parser !
 - Copy/Look at the template if you want create a new one
 - Create a new one based on the template (don't forgot, the name of the function should match the function name of the "RSS_FEED_URLS")
 - `DEBUG = True` in the script
 - Uncomment the first "if DEBUG" part to check the "returned value" and "index" of the feed link.
 - Execute the script, wait the information, kill the script
 - Look at the given information, if the summary doesn't contain "html" just plain/text, you can simply remove the 3 soup line, and just change "summary = None" by "summary = entry.summary"
 - For image it should be ok too
 - If you want to know the author, you can just put it in the "sitename" variable at the end like this: `save_entry(entry.id, f"{sitename} - {entry.author}", entry.title, entry.link, summary, img)` 


### Disable existing RSS Flux
Just uncomment the feed you want from the RSS_FEED_URLS then execute the bot.

---

## Debug !
The script begin to create a database file (if not exist), then it will check the RSS_FEED_URLS variable, and execute each "rss parser". Each rss parser will save into the database items of the feed like: the id, the title, the summary and if possible the image.
<br/><br/>
After the parsing step, the script will check unsent entries in the database and send all of theses entries in discord then mark each entry as sent.


## FAQ
[TODO]


