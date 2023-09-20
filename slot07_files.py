"""
    DECANUM - Robot Inventor MicroPython Software -
    Project     : Framework for LEGO Robot Inventor MSHub
                : Application Files read / write sample  
    Application : slot07_files.py
    Libraries   : sloy15_baselib.py
    Auth        : remybeaudenon@yahoo.com
    Date        : 08/2023
"""
import hub, time ,os,gc
from micropython import const

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

# ----Main Program----
TRACE = True # Enable or desable flag
Fw.Log.trace('Main:Thread() Welcome to Discovery Hub os:{}version:{} fw:{}'. \
            format(sys.platform ,sys.version,LegoFw.__VERSION__))




# -- Sensors port---

# -- global instance ---
gc.collect()
hub    = MSHub()
Fw.Speaker.beep3()
try:
    tab_fname = "/projects/test.dat"
    print("len: {}".format(os.stat(tab_fname)[6]))
except:
    None

try :
    persist = Fw.Persit()

    Fw.Persit.listdir(Fw.Persit.cwd() )

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


# ---------------------------------------------
# ---------- Process Tasks loop ---------------
# ---------------------------------------------



# ---------------------------------------------

# -- Exit Program --
Fw.Speaker.play_sound('Mission Accomplished')
raise Exception("Exit")



