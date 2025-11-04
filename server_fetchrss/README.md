# server_fetchrss

This README will cover the RSS Fetch part

## Summary
- [YabotRSS](../README.md#yet-another-bot-rss)
  - [RSS Fetcher](../server_fetchrss/README.md#server_fetchrss)
    - [Requirements](#requirements)
    - [Installation](#installation)
    - [Execution](#execution)
    - [What to do next ?](#what-to-do-next-)
    - [Contribute](#contribute)
      - [Add New RSS Flux](#add-new-rss-flux)
        - [RSS_FEED_URLS](#-rss_feed_urls-)
        - [PARSE RSS FEED URL](#--parse-rss-feed-url--)
      - [Disable existing RSS Flux](#disable-existing-rss-flux)
      - [Debug](#debug-)
    - [FAQ](#faq)
  - [Bot Sender](../client_sendrss/README.md#client_sendrss)
    - [Requirements](../client_sendrss/README.md#requirements)
    - [Installation](../client_sendrss/README.md#installation)
    - [Setup on Discord](../client_sendrss/README.md#setup-on-discord)
    - Setup on Slack
    - Setup on Telegram
    - [Contribute](../client_sendrss/README.md#contribute)


## Requirements

- Python 3.9+ (also tested with Python 3.13)
- pip/virtualenv


## Installation

- Clone the project
- open "server_fetchrss" folder
- create a virtualenv to isolate package from system
- update pip
- install requirement (I close/open virtualenv again because weird behaviour sometimes)

Or in one script:
```bash
if [ ! -d ".git" ] ; then
  git clone https://github.com/borrougagnou/yabotrss.git
  cd yabotrss
fi
cd server_fetchrss
virtualenv venv_server --python=python3 && source ./venv_server/bin/activate && pip install -U pip && deactivate && source ./venv_server/bin/activate
source ./venv_server/bin/activate && pip install -r requirements.txt && deactivate
cd ..
```


## Execution

> [!info]
> **First Step only !**
> The script need to generate a database with all feed
>
> Execute the bot to initiate the database
> Wait until the message "`Done: XXX`"

To execute the script:
```
source ./server_fetchrss/venv_server/bin/activate
python3 ./server_fetchrss/rss_fetcher.py continuous
```

Also the script possess multiple mode:

- python3 rss_fetcher.py once - This mode will fetch all feed once then exit")
- python3 rss_fetcher.py continuous [secs] - This mode will run indefinitely (sec by default: 10mins)")
- python3 rss_fetcher.py test <feed_name>  - This mode will test a single feed")



## What to do next ?

Follow the instruction in the [../client_sendrss/README.md](../client_botsender/README.md)


## Contribute

### Add New RSS Flux
> [!IMPORTANT]
> This step require to have few skill in Python language.

There are 2 places you need to check:
<br/>

### > "<ins>RSS_FEED_URLS</ins>" :
Contain all the RSS feed the boot will parse, you will see:
 - `name` : a name of the website you want parse (eg: Ars Technica)
 - `url` : the url of the feed (on some website you can found it in the footer of the website)
 - `function` : it's a Dynamic Function Call, it contain the function name of the parser engine.

### > "<ins>### PARSE RSS FEED URL ###</ins>" :
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

### Debug !
The script begin to create a database file (if not exist) in the root of the repository into the "database" folder, then it will check the RSS_FEED_URLS variable, and execute each "rss parser". Each rss parser will save into the database items of the feed like: the id, the title, the summary and if possible the image.
<br/><br/>
After the parsing step, the script will check unsent entries in the database and send all of theses entries in discord then mark each entry as sent.


## FAQ
How to debug ?

you can read the `rss_fetcher.log`

or use the debug breakpoints
```python
import pdb; pdb.set_trace()  # Add this line where you want to stop
```

