import discord,asyncio

'''
this class uses discord.py
seperate API will be written soon
to reduce # of dependencies
Refer to the following documentation:
http://discordpy.readthedocs.io/en/latest/api.html
'''

global client,loop,channelid
client = discord.Client() #discord client object
loop = None #async loop. used by other classes to add coroutines
channelid = None

class Session:

    global client,loop,channelid

    def __init__(self,token,channel):
        global channelid
        self.token = token #bot token
        channelid = channel #channel ID the bot uploads files to
    #closes all connections
    #RUNS ON MAIN THREAD, ASYNC.
    async def logout(self):
        await client.close()
    #initializes the loop once connected to
    #discord servers. 
    #RUNS ON MAIN THREAD, ASYNC.
    @client.event
    async def on_ready():
        global client,loop,channelid
        loop = asyncio.get_event_loop()
        if client.get_channel(int(channelid)) == None:
            print("Channel ID doesn't exist, reconfigure the program or update config.discord")

    #Returns text channel bot is uploading files to
    def getChannel(self):
        return client.get_channel(int(channelid))

    #Connects to discord servers.
    #LEADS TO ASYNC LOOP. RUNS ON MAIN THREAD.
    def start(self):
        client.run(self.token)

    #Returns the client object
    def getClient(self):
        return client

    #Returns the async loop.
    def getLoop(self):
        return loop
