"""
    DECANUM - Robot Inventor MicroPython Software -
    Project     : Framework for LEGO Robot Inventor MSHub
                : Persistance library 
    Application : slot16_persistence.py
    
    Libraires   : slot15, slot 16 
    Auth        : remybeaudenon@yahoo.com
    Date        : 06/2023
"""

from mindstorms.control import wait_for_seconds,Timer
from mindstorms import MSHub, Motor, MotorPair, DistanceSensor,ColorSensor
from micropython import const
import math,sys,urandom,time
import os ,json,gc 

class LegoFw : 
    __VERSION__ ='1.0.2-0822'

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
hub    = MSHub()
LIBRARY_SLOT = const(16) 

# -- LIBRARY MAIN ---
print("library loaded into robot slot:{}".format(LIBRARY_SLOT))
hub.speaker.play_sound('charging')



