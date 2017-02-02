# Discord Storage
Utilize Discord servers as cloud storage! [This only works on python 3.X]

## Tutorial
#### Setting up the bot/server

##### 1) Creating the bot
In order for this program to work, you're going to need to create a discord bot so we can connect to the discord API. Go to [this](https://discordapp.com/developers/applications/me) link to create a bot. Make sure to create a user bot and ensure the bot is private. [Here's](http://i.imgur.com/QIWBksk.png) a picture to the configuration. **Keep note of the token under the Bot Users section and the client ID under App Details.**
##### 2) Setting up the server
The bot will need a place to upload files. Create a new discord server, make sure no one else is on it unless you want them to access your files.

##### 3) Adding your bot to the server
To add the bot to the server (assuming your bot isn't public), go to the following link: https://discordapp.com/oauth2/authorize?client_id={CLIENT_ID}&scope=bot&permissions=0
Replace {CLIENT_ID} with the client ID you copied earlier. Then, select the server you just made and authorize. Your server should now show your bot like [this](http://i.imgur.com/NnqQAv7.png).

#### Setting up the program
##### 1) Dependecies
Clone the repository and run ```pip install -r requirements.txt``` to install the dependencies for the program.
##### 2) Configuration
Run ```python ds.py``` to begin configuration of the bot. When prompted, copy and paste your **token** from when you created your bot. For the channel ID, just press enter for the bot to connect to the general text channel. Your configuration should look like [this](http://i.imgur.com/g72BDoG.png)

*You can delete ```config.discord``` to reconfigure the program.*
#### Commands
Usage: ```python ds.py [flag] {args}```

```-up /full_path/file.exe``` The -up or -u flag and the full file path uploads a file.

```-dl {FILE_CODE}``` The -dl or -d flag and the file code will download a file from the discord server. Refer to the ```-list``` command to see uploaded file codes.

```-list``` The -list or -l flag will list all the file names/codes/sizes uploaded to the discord server.


#### Disclaimer
You shouldn't be using this as your main source of file storage. Program was inspired by [snapchat-fs](https://github.com/hausdorff/snapchat-fs). 



