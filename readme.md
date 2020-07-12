# Haven the Discord Music Bot
<p align="center">
    <img src="https://bitbucket.org/alexanderpaul/marinas-utility-music/raw/cade778b68c69033d66f5b59980c95006d3357f7/haven.jpg" width="350">
</p>

## Dependencies
* discord.py rewrite w/ voice - ```pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]```
* a lower version of yarl - ```pip install "yarl<1.2"```
* libopus - ```pip install opuslib```
* [ffmpeg](https://www.ffmpeg.org/download.html) - installed on your computer and set to path
* asyncio
* youtube_dl
* requests
* isodate

## Setting it up:  
* Clone/download the repository  
* Create a [Discord](https://discordapp.com/) account
* Go to User Settings -> Appearance and enable Developer Mode
* Create a Discord server then copy your Server's ID by right-clicking the server name on the upper left and keep it for later use
* Copy your USER ID by typing \\ and mentioning/tagging yourself using @<name\> after it. Only get the numbers. 
* Create text channel to be used solely for spamming the music commands then copy the channel's ID using right-click again and keep it for later  
* Create a voice channel for the bot to connect into then copy its channel ID as well  
* [Create an application on Discord](https://discordapp.com/developers/applications/me)  
* Scroll down to Bot section and click Create a Bot User  
* In the Bot section, beside the "Token" click the "click to reveal" and copy and paste it for later   
* Scroll up and below the "OAUTH2 URL GENERATOR", click "GENERATE OAuth URL"  
* On Bot Permissions, make sure to tick the necessary permissions for the bot to work properly such as:  
    * View Channels
    * Send Messages
    * Embed Links
    * Read Message History
    * Connect
    * Speak
    * Use Voice Activity
* When you're done ticking the permissions, copy the generated url above it and paste it on your browser and select the server you want the bot to join into  
* Go to your freshly stolen repo and enter the necessary token and ID's you've copied to their correct variables on the config.py file
* Open a terminal and go to your repos directory and run ```python main.py``` and the bot should go online and send a message on the spam channel
* Use !help on the music spam channel you've created for a list of commands 
* You may configure a custom prefix in the config.py