# client_sendrss

This README will cover the send RSS part

## Summary
- [YabotRSS](../README.md#yet-another-bot-rss)
  - [RSS Fetcher](../server_fetchrss/README.md#server_fetchrss)
    - [Requirements](../server_fetchrss/README.md#requirements)
    - [Installation](../server_fetchrss/README.md#installation)
    - [Execution](../server_fetchrss/README.md#execution)
    - [What to do next ?](../server_fetchrss/README.md#what-to-do-next-)
    - [Contribute](../server_fetchrss/README.md#contribute)
      - [Add New RSS Flux](../server_fetchrss/README.md#add-new-rss-flux)
        - [RSS_FEED_URLS](../server_fetchrss/README.md#-rss_feed_urls-)
        - [PARSE RSS FEED URL](../server_fetchrss/README.md#--parse-rss-feed-url--)
      - [Disable existing RSS Flux](../server_fetchrss/README.md#disable-existing-rss-flux)
      - [Debug](../server_fetchrss/README.md#debug-)
    - [FAQ](../server_fetchrss/README.md#faq)
  - [Bot Sender](../client_sendrss/README.md#client_sendrss)
    - [Requirements](#requirements)
    - [Installation](#installation)
    - [Setup on Discord](#setup-on-discord)
      - [New Application on discord.com](#new-application-on-discordcom)
      - [Configure discord_notifier.py](#configure-discord_notifierpy)
      - [Execute](#execute)
    - Setup on Slack
    - Setup on Telegram
    - [Contribute](#contribute)


## Requirements
- Python 3.9+
- pip/virtualenv

> [!WARNING]
> **First Step only !**
> The script need to take information from a database with all feed
>
> Read the RSS_Fetcher at first !
> Before moving forward in this documentation


## Installation
- Clone the project
- open "client_sendrss" folder
- create a virtualenv to isolate package from system
- update pip
- install requirement (I close/open virtualenv again because weird behaviour sometimes)

Or in one script:
```bash
if [ ! -d ".git" ] ; then
  git clone https://github.com/borrougagnou/yabotrss.git
  cd yabotrss
fi
cd client_sendrss
virtualenv venv_client --python=python3 && source ./venv_client/bin/activate && pip install -U pip && deactivate && source ./venv_client/bin/activate
source ./venv_client/bin/activate && pip install -r requirements.txt && deactivate
cd ..
```

---

## Setup on discord

### New Application on discord.com

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


### Configure discord_notifier.py

- Copy your Discord Token. Get it from [Discord Developers Portal](https://discord.com/developers/applications)

      > <your discord app>
          > "Bot" (left menu):
              > Token: "Reset Token" and copy the new one !

- Found a discord channel : [How to find the Channel ID number](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID)
-  Open and edit the `discord_notifier.py` file and put your:
   ```python
   # Discord Bot Token and Channel ID
   DISCORD_TOKEN = "ADD_YOUR_DISCORD_TOKEN_HERE" 
   DISCORD_CHANNEL_ID = "ADD_YOUR_DISCORD_CHANNEL_ID_HERE"  # Replace with your channel ID
   ```

Optionally, you also can move the database somewhere else by changing this value :`DB_FILE = "rss_feed.db"`. Don't forgot to edit the DB_FILE in the server too or use symbolic link !


### Execute

> [!WARNING]
> **IMPORTANT TO KNOW FOR THE FIRST LAUNCH !!!**
> 
> To prevent a flood (and a ban from the platform),
> open and edit the `discord_notifier.py` file and change ALLOW_SEND by False:
> ```python
> ALLOW_SEND = False
> ```


To execute:
```bash
source ./client_sendrss/venv_client/bin/activate
python3 ./client_sendrss/discord_notifier.py
```

---

## Setup on Slack
##TODO

---

## Setup on Telegram
##TODO

---

## Contribute
##TODO
