from mindstorms.control import wait_for_seconds,Timer
from mindstorms import MSHub, Motor, MotorPair, DistanceSensor,ColorSensor
from micropython import const
import math,sys,urandom,time
import os ,json,gc 



class LegoFw : 
    __VERSION__ ='1.0.2-0614'

class Log():

    @staticmethod
    def trace(data) :

        if not TRACE :
            return

        data_string =''
        if (type(data) == str ) :
            data_string = data
        elif (type(data) == list or type(data) == dict ) :
            data_string = ' ' + repr(data)
        elif (type(data) == int or type(data) == float ):
            data_string = ' ' + '{} value:{}'.format(type(data),data)
        else :
            data_string = 'Log:_writedata can\'t be converted.. {}'.format(type(data))
        header_record = ''
        lt= time.localtime()
        nowDay= '{:03d}'.format(lt[7])
        nowTime = '{:02d}:{:02d}:{:02d}'.format(lt[3],lt[4],lt[5])

        header_record = '{}\t{}\t'.format( nowDay,nowTime)
        line = header_record + data_string
        print(line)

class Speaker() :

    BRUITAGES = ['Activate','Affirmative','Bing','Bowling','Brick Eating','Bumper','Celebrate','Charging','Chuckle',\
            'countdown','Countdown Tick','Damage','Deactivate','Dial Down','Dial Up','Error','Explosion',\
            'Failure Chime','Fire','Flutter','Glitch','Goal','Grab','Growl',\
            'Hammer','Hit','Horn','Hydraulics Down','Hydraulics Up','Initialize','Kick','Laser',\
            'Ping','play','Power Down','Power Up','Punch','Reverse',\
            'Revving','Scanning','Shake','Shooting','Shut Down ','Slam Dunk','Slow down',\
            'Sonic Explosion','Static','Stomp','Strike','Success Chime','Theremin',\
            'Tweet','Void','Warp Speed','Whirl','Zap'
            ]
    VOIX = ['1234','Delivery','Dizzy','Exterminate','Goodbye','Ha','Ha Ha','Ha Ha Ha','Hello','Hi','HI 5','Hit','Humming','Laugh',\
            'Like','Mission Accomplished','No','Oh','Oh No','Oh Oh','Ouch','Sad','Seek and Destroy','Scared','Tadaa','Target Acquired','Target Destroyed',\
            'Void','Wow','Yes','Yipee','Yuck'
            ]

    @staticmethod
    def beep3():
        hub.speaker.beep(60, 0.1)
        hub.speaker.beep(70, 0.1)
        hub.speaker.beep(62, 0.1)

    @staticmethod
    def beep():
        hub.speaker.beep(60, 0.2)

    def play_sound(name = 'Bing') :

        if name in Speaker.BRUITAGES or name in Speaker.VOIX:
            hub.speaker.play_sound(name)
        else :
            hub.speaker.play_sound('Void')


class Persit :

    FILE_CTX = 'context.json'

    def __init__(self) :
        self.path = '/'


    @staticmethod
    def cwd() :
        path = os.getcwd()
        Log.trace("path : {}".format(path))
        return path

    @staticmethod
    def listdir(path) :
        alist = os.listdir(path)
        Log.trace("list directory : {}".format(alist))
        return alist

    @staticmethod
    def chdir(path) :
        rc = None
        try :
            rc = os.chdir(path)
            Log.trace("Log.chdir() path: {} \trc:{}".format(path,rc))
        except Exception as e :
            Log.trace("Log.chdir() path: {} Exception: {}".format(path,e))
        return rc

    def file_exists(file):
        try:
            ok = os.stat(file) != None
        except:
            ok = False
        return ok


    @staticmethod
    def mkdir(path) :
        rc = None
        try :
            rc = os.mkdir(path)
            Log.trace("Log.mkdir() path: {} \trc:{}".format(path,rc))
        except Exception as e :
            Log.trace("Log.mkdir() path: {} Exception: {}".format(path,e))
        return rc

    @staticmethod
    def rmdir(path) :
        rc = os.rmdir(path)
        Log.trace("Log.rmdir() path: {} \trc:{}".format(path,rc))
        return rc



# ----Main Program----
TRACE = True # Enable or desable flag
Log.trace('Main:Thread() Welcome to Discovery Hub os:{}  version:{} fw:{}'. \
               format(sys.platform ,sys.version,LegoFw.__VERSION__))

# -- Sensors port---

# -- global instance ---
gc.collect()
hub    = MSHub()
Speaker.beep3()
try:
    tab_fname = "/data/test.dat"
    print("len: {}".format(os.stat(tab_fname)[6])) 
except:
    None

try :
    persist = Persit()

    Persit.listdir(Persit.cwd() )

    prj = "/projects/"
    with open(prj+".slots","r") as f:
        slots = eval(f.read())
        for s in slots:
            base = prj+str(slots[s]['id'])
            print("--[{}]".format(base))


    #if Persit.chdir('/data') == None :
    #    Persit.mkdir('/data')
except Exception as e : 
    print("Exception ==> {}".format(e))
finally :
    os.sync()
    gc.collect()




   


# Open a file for reading
#file = open(cwd+'main.py', 'r')
# Read the first line of the file
#line = file.readline()
# Loop through the rest of the file and print each line
#while line:
#    print(line)
#    line = file.readline()

# Close the file when you're done
#file.close() 