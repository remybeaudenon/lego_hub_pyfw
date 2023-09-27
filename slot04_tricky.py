"""
    DECANUM - Robot Inventor MicroPython Software -
    Project     : Framework for LEGO Robot Inventor MSHub
                : Application Tricky déplacements  
    Application : slot04_tricky.py
    Libraries   : sloy15_baselib.py
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

COLOR_SENSOR_PORT= 'E'
colorSensorCtrl = Fw.ColorSensor(COLOR_SENSOR_PORT)

# -- Tricky instance -- 
tricky = Fw.Tricky()


MOTOR_AUX_PORT = 'C'
motorAux = Fw.MotorAux(MOTOR_AUX_PORT, Fw.MotorAux.REVERSE)

# ---------------------------------------------
# ---------- Process Tasks loop ---------------
# ---------------------------------------------

# Mission Meta data
PARAM_DRIVE= PARAM_ANGLE = 0
PARAM_SPEED= 1
PARAM_POINTS = PARAM_SECONDS = PARAM_COLOR = 2

ACTION_TANK     = 'K'# PARAM ( DRIVE,SPEED,SECONDS )
ACTION_CODER    = 'C'# PARAM ( DRIVE,SPEED,POINTS )
ACTION_GYRO     = 'G'# PARAM ( ANGLE GYROSCOPIQUE) - 0 --> 359 
ACTION_FOURCHE  = 'F'# PARAM ( ANGLE MOTOR AUX.)
ACTION_INDEX    = 'I'# PARAM ( DRIVE,SPEED,COLOR)


### ------Mission sequences-----
missions = [(ACTION_CODER,(0,45,1000)), \
            (ACTION_GYRO,(180,)), \
            (ACTION_CODER,(0,45,000)),\
            (ACTION_GYRO,(0,)), \
            ]
            
qmissions = [(ACTION_TANK,(0,30, 3)) , \
            (ACTION_CODER,(0,50,-1000)) ,\
            (ACTION_CODER,(0,35,0)) ]

# Mission tests rectiligne6000 points_codeur3 metres parcourus 5 arrets codeur.
_missions = [(ACTION_CODER,(0,35,500)),\
            (ACTION_CODER,(0,35,-500)) ,\
            (ACTION_CODER,(0,50,1000)) ,\
            (ACTION_CODER,(0,50,-1000)) ,\
            (ACTION_CODER,(0,35,0)) ]


__missions= [ (ACTION_TANK,(30, 25 , 2 )),\
            (ACTION_TANK,(-30, 25, 2)) , \
            (ACTION_TANK,(-30, 25, 1)), \
            (ACTION_TANK,(30, 35, 1)), \
            (ACTION_CODER,(0,50,2000)),\
            (ACTION_FOURCHE,(65,))]

# -- init coder
tricky.coder.set_degrees_counted(0)
tricky.coder.start_position()

Fw.Log.trace("--- Start position moteur_aux:{} ".format(motorAux.get_position() ))

timerCtrl = Fw.TimerCtrl()
timerCtrl.start()

for mission in missions :

    params = mission[1]
    Fw.Log.trace("Thread:main() Start mission:{:25} save time:{:03d} gyro:{:03d} coder:{:05d} ".format( str(mission) ,timerCtrl.now(), \
                                                            mshub.motion_sensor.get_yaw_angle(), tricky.coder.get_position()))

    if mission[0] == ACTION_TANK :
        tricky.mv_to_tempo(params)

    elif mission[0] == ACTION_CODER :
        tricky.mv_to_point(params)
            
    elif mission[0] == ACTION_INDEX :

        grafcet = 1
        pos_start = pos_end = pos_index = 0
        vitesse =params[PARAM_SPEED]

        while True :
            tricky.start_motors(params[PARAM_DRIVE] , vitesse )
            color = colorSensorCtrl.wait_for_new_color()
            if grafcet == 1 and color == params[PARAM_COLOR] :
                pos_start = tricky.coder.get_position()
                print("pos_start:{}".format(pos_start))
                grafcet = 2
                vitesse = 10
            elif grafcet == 2 and color == 'white' :
                pos_end = tricky.coder.get_position()
                print("pos_end:{}".format(pos_end))                
                grafcet = 3
                vitesse =vitesse * -1
            elif grafcet == 3 and color == params[PARAM_COLOR] :
                grafcet= 4
            elif grafcet == 4 and color == 'white' :
                pos_start = tricky.coder.get_position()
                vitesse =vitesse * -1
                pos_index = round(( pos_end - pos_start ) /2 ) + pos_start
                print("pos_index:{}".format(pos_index))
                grafcet= 5

            elif grafcet == 5 and round(( pos_end - pos_start ) /2 ) + pos_start  :
                pos_index = round(( pos_end - pos_start ) /2 ) + pos_start
                print("pos_index:{}".format(pos_index))

                while abs(tricky.coder.get_position() - pos_index ) > 20 :
                      pass
                grafcet= 0
                tricky.stop()
                break

            Fw.Log.trace("grafcet:{} vitesse:{} color:{} coder:{} ".format(grafcet,vitesse , color, tricky.coder.get_position()))

        tricky.stop()

    elif mission[0] == ACTION_GYRO :
        tricky.stop()
        tricky.gyro_to_angle(params)

    elif mission[0] == ACTION_FOURCHE :
        tricky.stop()
        motorAux.angle(params[PARAM_ANGLE])

tricky.stop()
motorAux.run_to_position(0)

Fw.Log.trace("Thread:main() End mission:{:25} save time:{:03d} gyro:{:03d} coder:{:05d} ".format( "    " ,timerCtrl.now(), \
                                                            mshub.motion_sensor.get_yaw_angle(), tricky.coder.get_position()))

timerCtrl.reset()

# ---------------------------------------------

# -- Exit Program --
Fw.Speaker.play_sound('Mission Accomplished')
raise Exception("Exit")

