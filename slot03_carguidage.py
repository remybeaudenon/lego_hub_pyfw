"""
    DECANUM - Robot Inventor MicroPython Software -
    Project     : Guidage vehicule 2 pairMotor avec joystick ( motor)  
                : et mémorisation du circuit.  
    Application : slot03_carguidage.py
    Libraries   : slot15_baselib.py
    Auth        : remybeaudenon@yahoo.com
    Date        : 06/2023
"""
import hub, time , sys
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

# -- Start Program --
LIBRARY_SLOT = const(15)

Fw = import_from_slot(LIBRARY_SLOT)
Fw.Speaker.play_sound('Hello')
Fw.MatrixLight.off()

# -- start Program --

# ---------------------------------------------
# ---------- Process Tasks loop ---------------
# ---------------------------------------------

class ProcessCtrl():

    @staticmethod
    def dummy() :
        timer    = Fw.TimerCtrl()
        while True:
            while True:
                Fw.Speaker.play_random()
                timer.reset()
                yield from timer.wait_y(30)
            yield
    @staticmethod
    def bouton_optique() :
        #bo = Fw.BoutonOptique()
        while True:
            yield bo.update_y()

    @staticmethod
    def manette_drive() :
        while True:
            yield manette.update_y()

    @staticmethod
    def run() :
        timer = Fw.TimerCtrl()
        select_speed = Fw.Select(Fw.Select.PARAMS_SPEED)

        car =Fw.Car()
        car.set_stop_action('hold')
        car.setSpeed(select_speed.waitValue())

        volant_previous = None
        timer_previous  = 0
        Fw.MatrixLight.show_number(timer_previous)  

        while True:
            while bo.isOn() and timer_previous < 30 :
                volant = manette.getValue()
                if volant_previous == None : 
                    manette.setValue(0)
                    timer.start()

                if volant_previous != volant : 
                    car.start_motors(volant)
                    volant_previous = volant

                if timer_previous != timer.now() : 
                    timer_previous = timer.now()
                    Fw.MatrixLight.show_number(timer_previous)
                    #print("direction: {}   timer: {}".format(volant,timer_previous))
                yield

            if volant_previous != None :
                car.stop()
                bo.off()
                volant_previous = None
                timer_previous  = 0  
            yield

# Create the cooperative tasks instance with linked menu Item
func_dummy          = ProcessCtrl.dummy()
func_bouton_optique = ProcessCtrl.bouton_optique()
func_run            = ProcessCtrl.run()
func_manette_drive  =ProcessCtrl.manette_drive()

# ----Main Program----
TRACE = True # Enable or desable flag
Fw.Log.trace('Main:Thread() Welcome to Discovery Hub os:{} car version:{} fw:{}'. \
               format(sys.platform ,sys.version,Fw.LegoFw.__VERSION__))

# -- Sensors port---
PAIR_MOTORS_PORT    = ('A','B')
RADAR_MOTOR_PORT    = 'C'
COLOR_SENSOR_PORT   = 'E'
RADAR_SENSOR_PORT   = 'F'
MANETTE_MOTOR_PORT  = 'D'

# -- global instance ---
Fw.Speaker.beep3()

Fw.StatusLight.on('yellow')
bo = Fw.BoutonOptique()
manette = Fw.ManetteDrive()

Fw.Log.trace("Select un  'P'rogramme touche '>'  '<' - Valider '>' 2 secondes. ")
Fw.Log.trace("Select une 'V'itesse   touche '>'  '<' - Valider '>' 2 secondes. ")
Fw.Log.trace("Depart/ Arret du vehicule avec le doigt Capteur Lumière")

select_prog_num = Fw.Select(Fw.Select.PARAMS_PROG_NUM)
prog_num = select_prog_num.waitValue()

#--- Loop ---
Fw.StatusLight.on('green')
while True :
    next(func_run)
    next(func_bouton_optique)
    next(func_manette_drive)

#--- Loop ---



