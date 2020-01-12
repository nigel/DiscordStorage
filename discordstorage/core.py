import os,io,aiohttp,asyncio, discord
from .Session import Session

class Core:

    def __init__(self,directory,token,channel):
        self.directory = directory #set root directory for downloaded/files to be uploaded
        self.session = Session(token,channel) #discord API
        self.client = self.session.getClient() #discord API client object

    #check if the client is connected to discord servers
    def isready(self):
        return not(self.session.getLoop() == None)

    #starts conenction to discord servers. 
    #RUNS ON MAIN THREAD, ASYNC.
    def start(self):
        self.session.start()

    #Halts all connection to discord servers.
    def logout(self):
         future = asyncio.run_coroutine_threadsafe(self.session.logout(), self.session.getLoop())
    
    #runs the async_upload in a threadsafe way,
    #can be run from anything outisde of main thread.
    def upload(self,inp,code):
         future = asyncio.run_coroutine_threadsafe(self.async_upload(inp,code), self.session.getLoop())
         try:
            return future.result()
         except Exception as exc:
            print(exc)
            return -1
         
    #runs the async_download in a threadsafe way,
    #can be run from an ything outside of main thread.
    def download(self,inp):
        future = asyncio.run_coroutine_threadsafe(self.async_download(inp), self.session.getLoop())
        try:
            return future.result()
        except Exception as exc:
            print('[ERROR] ' + exc)
            return -1

    #Downloads a file from the server.
    #The list object in this format is needed: [filename,size,[DL URLs]]
    #RUNS ON MAIN THREAD, ASYNC.
    async def async_download(self,inp):
            os.makedirs(os.path.dirname(self.directory + "downloads/" + inp[0]), exist_ok=True)
            f = open(self.directory + "downloads/" + inp[0],'wb')
            for i in range(0,len(inp[2])):
                    #user agent is not in compliance with Discord API rules. Change accordingly if needed
                    agent = {'User-Agent':'DiscordStorageBot (http://github.com/nigel/discordstorage)'}
                    async with aiohttp.ClientSession() as session:
                        async with session.get(inp[2][i],headers=agent) as r:
                                if r.status == 200:
                                        async for data in r.content.iter_any():
                                                f.write(data)
            f.close()
            #files[code] = [name,size,[urls]]

    #Uploads a file to the server from the root directory, or any other directory specified
    #inp = directory, code = application-generated file code
    #RUNS ON MAIN THREAD, ASYNC.
    async def async_upload(self,inp,code):
            urls = []
            f = open(inp,'rb')
            for i in range(0,self.splitFile(inp)):
                    o = io.BytesIO(f.read(8000000))
                    discord_file = discord.File(fp=o,filename=code+"." + str(i))
                    await self.session.getChannel().send(file=discord_file)
                    async for message in self.session.getChannel().history(limit=None):
                            if message.author == self.client.user:
                                    urls.append(message.attachments[0].url)
                                    break
            f.close()

            return [os.path.basename(inp),os.path.getsize(inp),urls]

    #Finds out how many file blocks are needed to upload a file.
    #Regular max upload size at a time: 8MB.
    #Discord NITRO max upload size at a time: 50MB.
    #Change accordingly if needed.
    def splitFile(self,f):
            if (os.path.getsize(f)/8000000) > 1:
                    return int(os.path.getsize(f)/8000000) + 1
            else:
                    return 1
