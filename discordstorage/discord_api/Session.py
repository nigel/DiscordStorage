import discord,asyncio

client = discord.Client()
loop = None
class Session:
    
    global client,loop

    def __init__(self,token):
        self.token = token
        
        self.channel = None

    @client.event
    async def on_ready():
        global loop
        print('ready')
        loop = asyncio.get_event_loop()

    def getChannel(self):
        return client.get_channel('271713258572873728')

    def start(self):
        client.run(self.token)

    def getClient(self):
        return client

    def getLoop(self):
        return loop
