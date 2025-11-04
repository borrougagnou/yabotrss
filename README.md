# Yet Another Bot RSS

This bot read RSS Flux from different source and send the title, description (and image maybe) on different platform like discord/telegram/slack/...

![Example of Discord screenshot](/img/Example-on-Discord-YabootRSS.png)


## Changelog
#### 20251104
- Changed some log with logging library for the server part
- Refactor again the script
  - The fetch RSS feed script use now thread instead of async
  - Debug async/await is way too difficult
- Removed old procedure, all of that are now deprecated
- Soon merge on master after the end of the test

#### 20250516
- Added datetime for each "rss fetch"/"push notifier"
- Refactor the script in 2 differents scripts and put the previous implementation in old_implementation
  - The first script will fetch RSS feed in database
  - The second script will take the feed from the database and send it to discord/slack/telegram/...
- Fixed some bug linked to duplicate post
- Fixed some bug from the rss fetch part
- Fixed some image bug from the discord notifier

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
- [YabotRSS](README.md#yet-another-bot-rss)
  - [RSS Fetcher](server_fetchrss/README.md#server_fetchrss)
    - [Requirements](server_fetchrss/README.md#requirements)
    - [Installation](server_fetchrss/README.md#installation)
    - [Execution](server_fetchrss/README.md#execution)
    - [What to do next ?](server_fetchrss/README.md#what-to-do-next-)
    - [Contribute](server_fetchrss/README.md#contribute)
      - [Add New RSS Flux](server_fetchrss/README.md#add-new-rss-flux)
        - [RSS_FEED_URLS](server_fetchrss/README.md#-rss_feed_urls-)
        - [PARSE RSS FEED URL](server_fetchrss/README.md#--parse-rss-feed-url--)
      - [Disable existing RSS Flux](server_fetchrss/README.md#disable-existing-rss-flux)
      - [Debug](server_fetchrss/README.md#debug-)
    - [FAQ](server_fetchrss/README.md#faq)
  - [Bot Sender](client_sendrss/README.md#client_sendrss)
    - [Requirements](client_sendrss/README.md#requirements)
    - [Installation](client_sendrss/README.md#installation)
    - [Setup on Discord](client_sendrss/README.md#setup-on-discord)
    - Setup on Slack
    - Setup on Telegram
    - [Contribute](client_sendrss/README.md#contribute)


## How it work

YabootRSS runs on 2 scripts:
  - The first script will fetch RSS feed and put it in database.
  - The second script will take the feed from the database and send it to discord/slack/telegram/...


## Fetch RSS feed

Please follow the instruction: [server_fetchrss/README.md](server_fetchrss/README.md)

## Send feed to client bot

Please follow the instruction: [client_sendrss/README.md](client_sendrss/README.md)

