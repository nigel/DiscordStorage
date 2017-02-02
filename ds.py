from discordstorage import core
import threading,json,asyncio,random,sys,argparse,os,time


#Server.get_default_channel()


TOKEN_SECRET = "" #bot's secret token
ROOM_ID = "" #channel text ID
BOT_INFO = None
FILES = None

#Generates a file code from 0-4097
def genCode():
    code = str(random.randint(0,4098))
    if FILES == None:
        return code
    while code in FILES.keys():
        code = str(random.randint(0,4098))
    return code
#returns if the config file is configured or not.
def isConfigured():
    return os.path.isfile('config.discord')

#invokes file uploading, to be used on a thread that's not in main thread.
#writes to config file accordingly.
def tellupload(line1,line2,cmd,code,client):
    while not (client.isready()):
        time.sleep(0.5)
    if not os.path.isfile(cmd):
        print('[ERROR] File does not exist.')
        client.logout()
        return
    print(line2)
    flcode = client.upload(cmd,code)
    jobject = json.loads(line2)
    jobject[code] = flcode
    f = open('config.discord','w')
    f.write(line1)
    f.write(json.dumps(jobject))
    f.close()
    client.logout()

def GetHumanReadable(size,precision=2):
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f%s"%(precision,size,suffixes[suffixIndex])

#invokes file downloading, to be used on a thread that's not in main thread
def telldownload(client,inp):
    while not (client.isready()):
        time.sleep(0.5)
    client.download(inp)
    client.logout()

#parses cmd line arguments
def parseArgs(inp):
    commands = ['-h','-help','-i','-info','-c','-config','-l','-list','-d','-download','-u','-upload']
    if(len(inp) == 1):
        print('hello')
        print('----------------------\n|DiscordStorage v0.1 |')
        print('|github.com/nigelchen|\n----------------------')
        print('\nUsage: python ds.py [command] (target)\n')
        print('COMMANDS:')
        print('[-h, -help] :: Show the current message')
        print('[-i, -info] :: Displays the information about the application')
        print('[-c, -config] :: Begins steps to configuring this application.')
        print('[-l, -list] :: Lists all the file informations that has been uploaded to the server.')
        print('[-d, -download] (FILE CODE) :: Downloads a file from the server. A filecode is taken in as the file identifier.')
        print('[-u, -upload] (FILE DIRECTORY) :: Uploads a file to the server. The full file directory is taken in for the argument.\n')
    elif isConfigured():
        f = open('config.discord','r')
        first = f.readline()
        second = f.readline()
        f.close()
        TOKEN_SECRET = json.loads(first.replace("\\n",""))['TOKEN']
        for el in inp:
            if '-dl' == el or '-d' == el:
                if not ((not(FILES == None)) and (inp[inp.index(el)+1] in FILES.keys())):
                    print('\n[ERROR] File code not found\n')
                else:
                    obj = json.loads(second)[inp[inp.index(el)+1]]
                    print('DOWNLOADING: ' + obj[0] )
                    print('SIZE: ' + str(obj[1]))
                    client = core.Core(os.getcwd() + "/",TOKEN_SECRET,None)
                    threading.Thread(target=telldownload,args=(client,obj,)).start()
                    client.start()
                    break
            elif '-up' == el or '-u' == el:
                print('UPLOADING: ' + inp[inp.index(el)+1])
                client = core.Core(os.getcwd() + "/",TOKEN_SECRET,None)
                threading.Thread(target=tellupload,args=(first,second,inp[inp.index(el)+1],genCode(),client,)).start()
                client.start()
                break
            elif '-list' == el or '-l' == el:
                if not (FILES == None):
                    print('\nFILES UPLOADED TO DISCORD:\n')
                    for key in FILES.keys():
                        print('name: ' + str(FILES[key][0]) + ' | code: ' + str(key) + ' | size: ' + GetHumanReadable(FILES[key][1]) +'')
                    print('\n')
                    break

                #print('name: X.png | code: 4178 | size: 3213')


if not isConfigured():
    print('Welcome to DiscordStorage.')
    print('Go to http://github.com/nigelchen/DiscordStorage for instructions.')
    TOKEN_SECRET = input('Bot token ID (Will be stored in plaintext in config file):')
    print('Please enter the channel ID (leave blank for default):')
    ROOM_ID = input('Enter channel ID to store files in. Leave blank for default channel.')
    if len(ROOM_ID) <=0:
        ROOM_ID = None
    f = open('config.discord','w')
    f.write(str(json.dumps({'TOKEN':TOKEN_SECRET,'ROOM_ID':ROOM_ID})) + "\n")
    f.write(str(json.dumps({})))
    f.close()
else:
    f = open('config.discord','r')
    first = f.readline()
    second = f.readline()
    BOT_INFO = json.loads(first)
    FILES = json.loads(second)
    TOKEN_SECRET = json.loads(first.replace("\\n",""))['TOKEN']
    ROOM_ID = json.loads(first.replace("\\n",""))['ROOM_ID']
    f.close()




try:
    parseArgs(sys.argv)
except IndexError:
    print('\nUsage: python ds.py [command] (target)\n')
    print('COMMANDS:')
    print('[-h, -help] :: Show the current message')
    print('[-i, -info] :: Displays the information about the application')
    print('[-l, -list] :: Lists all the file informations that has been uploaded to the server.')
    print('[-d, -download] (FILE CODE) :: Downloads a file from the server. A filecode is taken in as the file identifier.')
    print('[-u, -upload] (FILE DIRECTORY) :: Uploads a file to the server. The full file directory is taken in for the argument.\n')
    


#
#threading.Thread(target=userinput).start()
#wclient.start()
'''
discordSession = Session.Session(TOKEN_SECRET)
discordStorage = core.Core('/Users/nigelchen/desktop/',discordSession.getLoop(),discordSession.getChannel(),discordSession.getClient())

threading.Thread(target=userinput).start()

discordSession.start()
'''
