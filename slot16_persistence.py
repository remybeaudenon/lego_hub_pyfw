"""
    DECANUM - Robot Inventor MicroPython Software -
    Project     : Framework for LEGO Robot Inventor MSHub
                : Application Dummy sample 
    Application : slot16_persistence.py
    Libraries   : sloy15_baselib.py
    Auth        : remybeaudenon@yahoo.com
    Date        : 08/2023
"""
import hub, time ,os
from micropython import const
from mindstorms import MSHub

def import_from_slot(slot) :
    import sys,util
    print("Library loading from slot:{}".format(slot))
    hub.display.show( hub.Image("99999:90909:00000:00990:009900") )
    if '/projects' not in sys.path :
        sys.path.append('/projects')
    # Now import the module
    path = util.storage.get_path(slot) # './projects/40117'
    names = path.split('/') # ['.','projects','40117']
    name = names[-1] # '40117'
    return __import__(name)

# -- Libraries load  --
LIBRARY_SLOT = const(15)
Fw = import_from_slot(LIBRARY_SLOT)
Fw.Speaker.play_sound('Hello')
hub.light_matrix.off()

# -- start Program --

# ---------------------------------------------
# ---------- Process Tasks loop ---------------
# ---------------------------------------------

#from mindstorms.control import wait_for_seconds,Timer
#from mindstorms import MSHub, Motor, MotorPair, DistanceSensor,ColorSensor
#from micropython import const
#import math,sys,urandom,time
#import os ,json,gc 

class Persit :

    FILE_CTX = 'context.json'

    def __init__(self) :
        self.path = '/'


    @staticmethod
    def cwd() :
        path = os.getcwd()
        Fw.Log.trace("path : {}".format(path))
        return path

    @staticmethod
    def listdir(path) :
        alist = os.listdir(path)
        Fw.Log.trace("list directory : {}".format(alist))
        return alist

    @staticmethod
    def chdir(path) :
        rc = None
        try :
            rc = os.chdir(path)
            Fw.Log.trace("Log.chdir() path: {} \trc:{}".format(path,rc))
        except Exception as e :
            Fw.Log.trace("Log.chdir() path: {} Exception: {}".format(path,e))
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
            Fw.Log.trace("Log.mkdir() path: {} \trc:{}".format(path,rc))
        except Exception as e :
            Fw.Log.trace("Log.mkdir() path: {} Exception: {}".format(path,e))
        return rc

    @staticmethod
    def rmdir(path) :
        rc = os.rmdir(path)
        Fw.Log.trace("Log.rmdir() path: {} \trc:{}".format(path,rc))
        return rc

# ----Main Program----
hub    = MSHub()
LIBRARY_SLOT = const(16) 

# -- LIBRARY MAIN ---
print("library loaded into robot slot:{}".format(LIBRARY_SLOT))
hub.speaker.play_sound('charging')



