"""
    DECANUM - Robot Inventor MicroPython Software -
    Project    : Framework for LEGO Robot Inventor MSHub
                : Application Dummy sample
    Application : slot04_codeur.py
    Libraries: sloy15_baselib.py
    Auth        : remybeaudenon@yahoo.com
    Date        : 09/2023
"""
import hub, time, gc
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

# -- Libraries load--
LIBRARY_SLOT = const(15)
Fw = import_from_slot(LIBRARY_SLOT)
Fw.Speaker.play_sound('Hello')
Fw.MatrixLight.off()

# -- start Program --
mshub = MSHub()
mshub.motion_sensor.reset_yaw_angle()
cap = mshub.motion_sensor.get_yaw_angle()

matrix = Fw.MatrixLight()
matrix.off()

car = Fw.Car()
car.setSpeed(10)

MOTOR_AUX_PORT = 'C'

motorAux = Fw.MotorAux(MOTOR_AUX_PORT, Fw.MotorAux.REVERSE)

# ---------------------------------------------
# ---------- Process Tasks loop ---------------
# ---------------------------------------------

# Mission Meta data 
PARAM_DRIVE   = 0
PARAM_SPEED   = 1
PARAM_SECONDS = 2
PARAM_POINTS  = 2 
PARAM_ANGLE   = 0

ACTION_TEMPO   = 'T'   # PARAM ( DRIVE,SPEED,SECONDS )
ACTION_CODEUR  = 'C'   # PARAM ( DRIVE,SPEED,POINTS )
ACTION_ROTATE  = 'R'   # PARAM ( ANGLE)

### ------  Mission sequences  -----  
#missions = []
missions = [(ACTION_ROTATE,(-15)) ]

xmissions  = [ (ACTION_TEMPO,(30, 25 , 3 )), 
              (ACTION_TEMPO,(-30, 25, 6)) , \
              (ACTION_TEMPO,(30, 25, 3))  , \
              (ACTION_TEMPO,(0, 35, 3 ))  , \
              (ACTION_CODEUR,(0,50,3500))]

# -- init coder 
car.coder.set_degrees_counted(0)
car.coder.start_position()

Fw.Log.trace("-- Start position coder:{}  yaw:{}  moteur_aux:{} ".format(car.coder.get_position(), \
                                                    mshub.motion_sensor.get_yaw_angle(),motorAux.get_position() ))

timerCtrl = Fw.TimerCtrl() 
timerCtrl.start() 

for mission in missions :

    if mission[0] == ACTION_TEMPO : 

        params = mission[1] 
        car.start_motors(params[PARAM_DRIVE] , params[PARAM_SPEED] )
        Fw.Log.trace("mission:[{}] save time:{} coder:{} ".format( mission ,  timerCtrl.get_saveTime(), \
                                                              car.coder.get_position())) 
        while timerCtrl.lap() <  timerCtrl.get_saveTime() + params[PARAM_SECONDS] :
            pass
        timerCtrl.set_saveTime()

    elif mission[0] == ACTION_CODEUR :
        params = mission[1] 

        car.start_motors(params[PARAM_DRIVE] , params[PARAM_SPEED] )
        Fw.Log.trace("mission:[{}] save time:{} coder:{} ".format( mission ,  timerCtrl.get_saveTime(), \
                                                              car.coder.get_position())) 
        while car.coder.get_position() <  params[PARAM_POINTS] :

            points_restant = abs(car.coder.get_position() - params[PARAM_POINTS])    
            if points_restant  <=  250 :
                vitesse = min(params[PARAM_SPEED], max( 25 , round(points_restant / 5.0 )))
            else : 
                vitesse = params[PARAM_SPEED]
            car.start_motors(params[PARAM_DRIVE] , vitesse )
        timerCtrl.set_saveTime()

    elif mission[0] == ACTION_ROTATE :
        params = mission[1] 
        car.rotate(params[PARAM_ANGLE])


car.stop()
timerCtrl.reset()

Fw.Log.trace("--END position coder:{} total duration:{}  yaw:{}".format(car.coder.get_position(), \
                                                                        timerCtrl.get_saveTime(), \
                                                                        mshub.motion_sensor.get_yaw_angle()) ) 

motorAux.run_to_position(0)


# ---------------------------------------------

# -- Exit Program --
Fw.Speaker.play_sound('Mission Accomplished')
raise Exception("Exit")
