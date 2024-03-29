"""
    DECANUM - Robot Inventor MicroPython Software -
    Project     : Framework for LEGO Robot Inventor MSHub
                : Application Dummy sample 
    Application : slot01_dummy.py
    Libraries   : sloy15_baselib.py
    Auth        : remybeaudenon@yahoo.com
    Date        : 08/2023
"""
import hub, time
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
Fw.MatrixLight.off()

# -- start Program --

# ---------------------------------------------
# ---------- Process Tasks loop ---------------
# ---------------------------------------------



# ---------------------------------------------

# -- Exit Program --
Fw.Speaker.play_sound('Mission Accomplished')
raise Exception("Exit")


