"""
    DECANUM - Robot Inventor MicroPython Software -
    Project    : Framework for LEGO Robot Inventor MSHub
                : Application Dummy sample
    Application : slot04_codeur.py
    Libraries: sloy15_baselib.py
    Auth        : remybeaudenon@yahoo.com
    Date        : 09/2023
"""
import hub
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
PARAM_DRIVE= PARAM_ANGLE = 0
PARAM_SPEED= 1
PARAM_POINTS= PARAM_SECONDS =2

ACTION_TANK    = 'K'# PARAM ( DRIVE,SPEED,SECONDS )
ACTION_CODER= 'C'# PARAM ( DRIVE,SPEED,POINTS )
ACTION_GYRO    = 'G'# PARAM ( ANGLE GYROSCOPIQUE)
ACTION_FOURCHE = 'F'# PARAM ( ANGLE MOTOR AUX.)

### ------Mission sequences-----
#missions = []
missions = [(ACTION_CODER,(0,70,2500)) ]

xmissions= [ (ACTION_TANK,(30, 25 , 2 )),\
            (ACTION_TANK,(-30, 25, 2)) , \
            (ACTION_TANK,(-30, 25, 1)), \
            (ACTION_TANK,(30, 35, 1)), \
            (ACTION_CODER,(0,50,2000)),\
            (ACTION_FOURCHE,(65,))]

# -- init coder
car.coder.set_degrees_counted(0)
car.coder.start_position()

Fw.Log.trace("-- Start position coder:{}yaw:{}moteur_aux:{} ".format(car.coder.get_position(), \
                                                    mshub.motion_sensor.get_yaw_angle(),motorAux.get_position() ))

timerCtrl = Fw.TimerCtrl()
timerCtrl.start()

for mission in missions :

    params = mission[1]

    if mission[0] == ACTION_TANK :
        Fw.Log.trace("Thead:main() mission:[{}] save time:{} coder:{} ".format( mission ,timerCtrl.get_saveTime(), \
                                                            car.coder.get_position()))
        car.start_motors(params[PARAM_DRIVE] , params[PARAM_SPEED] )
        while timerCtrl.lap() <timerCtrl.get_saveTime() + params[PARAM_SECONDS] :
            pass
        timerCtrl.set_saveTime()

    elif mission[0] == ACTION_CODER :
        Fw.Log.trace("Thead:main() mission:[{}] save time:{} coder:{} ".format( mission ,timerCtrl.get_saveTime(),\
                                                                                car.coder.get_position()))
        start_pos = car.coder.get_position()
        while car.coder.get_position() < params[PARAM_POINTS] :

            points_restant = abs(car.coder.get_position() - params[PARAM_POINTS])   #  1cm --> 20 points 
            if points_restant <= 200 :                                              #  deceleration ramp started 10cm from end point.  
                vitesse = max( 15 , round(points_restant / 5.0 ))                   #  drop -10% Power each 2.5 cm 
                if vitesse > params[PARAM_SPEED] : vitesse   = params[PARAM_SPEED]  #  keep limitation 
            
            elif abs(car.coder.get_position() - start_pos)  < 250 :
                vitesse = max( 15, round(abs(car.coder.get_position() - start_pos ) /5.0) )    #  increase 10% each --> 50 points 
                if vitesse > params[PARAM_SPEED] : vitesse   = params[PARAM_SPEED]             #  keep limitation 
                #Fw.Log.trace("Thead:main() start:{} pos:{}   vit:{} ".format(start_pos , car.coder.get_position(),vitesse) )  
            else : 

                vitesse = params[PARAM_SPEED]
                #Fw.Log.trace("Thead:main() points_restant:{} vitesse:{} ".format( points_restant, vitesse))
            car.start_motors(params[PARAM_DRIVE] , vitesse )

        timerCtrl.set_saveTime()

    elif mission[0] == ACTION_GYRO :
        Fw.Log.trace("mission:[{}]yaw:{}save time:{} coder:{} ".format( mission ,mshub.motion_sensor.get_yaw_angle(), \
                                                        timerCtrl.get_saveTime(), car.coder.get_position()))
        car.rotate(params[PARAM_ANGLE])

    elif mission[0] == ACTION_FOURCHE :
        Fw.Log.trace("mission:[{}]angle:{} ".format( mission , params[PARAM_ANGLE]))
        motorAux.angle(params[PARAM_ANGLE])

car.stop()
timerCtrl.reset()
motorAux.run_to_position(0)

Fw.Log.trace("--END position coder:{} total duration:{}yaw:{}".format(car.coder.get_position(), \
                                                                        timerCtrl.get_saveTime(), \
                                                                        mshub.motion_sensor.get_yaw_angle()) )

# ---------------------------------------------

# -- Exit Program --
Fw.Speaker.play_sound('Mission Accomplished')
raise Exception("Exit")
