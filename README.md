# Yet Another Bot RSS

This bot read RSS Flux from different source and send the title, description (and image maybe) on different platform.

it requier few skill in python language if you want put your own rss.

## Requirement

- Python 3
- Account on:
    - https://discord.com/developers/applications

pip requirement:
```
    - discord.py
    - feedparser
    - beautifulsoup4
    - requests
```



## How to use

### Discord Part:
#### Application Menu
- [Create New Application](https://discord.com/developers/applications?new_application=true)
- Give it a name
- "Installation":
    - "Installation Contexts":
        - Check "User Install"
        - Check "Guild Install"
    - "Default Install Settings":
        - "Guild Install":
            - Scope: 'applications.command', 'bot'
            - Permissions: 'Embed Links', 'Read Message History', 'Send Messages', 'Send Messages in Threads', 'View Channels'
- "Bot":
    - Token: "Reset Token" :warning: put the new token in the "DISCORD_TOKEN" variable in the index.py file !
    - "Authorization Flow":
        - Check "Public Bot"
    - "Privileged Gateway Intents":
        - Check "Message Content Intent"

#### Discord website
- Add your bot on your server
- Enable the "[Developper mode](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID)" in discord
- [Copy your channel ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID) :warning: put the channel ID into the "DISCORD_CHANNEL_ID" variable in the index.py file !

### Python part:
- Edit the "index.py" file.
- put your Token Application in the "DISCORD_TOKEN" line
- put your Channel ID in the "DISCORD_CHANNEL_ID" line
- Change the variable "ALLOW_SEND" to False
- save and execute: `python3 index.py`
- Wait the script to finish the first launch, then quit.
- Change the variable "ALLOW_SEND" to True
- save and execute: `python3 index.py`
- Let the script running


## How It work !
The script begin to create a database file (if not exist), then it will check the RSS_FEED_URLS variable, and execute each "rss parser". Each rss parser will save into the database items of the feed like: the id, the title, the summary and if possible the image.
<br/><br/>
After the parsing step, the script will check unsent entries in the database and send all of theses entries in discord then mark each entry as sent.

### How to begin
**First thing to do**: :warning: CHANGE THE VARIABLE "ALLOW_SEND" TO FALSE ! :warning:
<br/> if you don't do that, the script will execute ALL EXISTING FEED into discord ! a massive flood !

Change this value to false, when you don't have launched the script for the first time/few days
<br/> after this step done, kill the script, change the variable to True, then re-execute the script

### Use existing Feed
Just uncomment the feed you want from the RSS_FEED_URLS (don't forgot change the value of ALLOW_SEND) then execute the script.


### How to Create a new Feed
There are 2 places you need to check:

#### __"RSS_FEED_URLS"__
Contain all the RSS feed the boot will parse, you will see:
 - `name` : a name of the website you want parse (eg: Ars Technica)
 - `url` : the url of the feed (on some website you can found it in the footer of the website)
 - `function` : it's a Dynamic Function Call, it contain the function name of the parser engine.


#### __"### PARSE RSS FEED URL ###"__
This part of the script contain engine for each parser !
 - Look at the template if you want create a new one
 - Create a new one based on the template (don't forgot, the name of the function should match the function name of the "RSS_FEED_URLS")
 - `DEBUG = True` in the script
 - Uncomment the first "if DEBUG" part to check the "returned value" and "index" of the feed link.
 - Execute the script, wait the information, kill the script
 - Look at the given information, if the summary doesn't contain "html" just plain/text, you can simply remove the 3 soup line, and just change "summary = None" by "summary = entry.summary"
 - For image it should be ok too
 - If you want to know the author, you can just put it in the "sitename" variable at the end like this: `save_entry(entry.id, f"{sitename} - {entry.author}", entry.title, entry.link, summary, img)` 


## FAQ
[TODO]

