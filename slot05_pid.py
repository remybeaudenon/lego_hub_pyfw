"""
    DECANUM - Robot Inventor MicroPython Software -
    Project    : Framework for LEGO Robot Inventor MSHub
                : Application Dummy sample
    Application : slot05_pid.py
    Auth        : remybeaudenon@yahoo.com
    Date        : 09/2023
"""
import hub,time
from mindstorms import MSHub,ColorSensor
#from mindstorms.control import wait_for_seconds
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

# -- Load Librarie --
LIBRARY_SLOT = const(15)
Fw = import_from_slot(LIBRARY_SLOT)
Fw.Speaker.play_sound('Hello')

# -- Instances--
mshub = MSHub()
colorSensor = ColorSensor('E')

matrix = Fw.MatrixLight()
matrix.off()

car = Fw.Car()
car.setSpeed(40)

pid = Fw.PID(P=1.1, I=0.35, D=0.003)
pid.setSampleTime(0)

REFLECT_NOIR = 40
REFLECT_BLANC = 98
pid.SetPoint= REFLECT_BLANC - REFLECT_NOIR

# -- Loop Program --
NBRE_TOURS = 3

counter = NBRE_TOURS
counter_step = 0
mshub.motion_sensor.reset_yaw_angle()

while counter >= 0 :

    feedback = colorSensor.get_reflected_light()
    pid.update(feedback)
    car.start_motors(-int(pid.output))

    cap = mshub.motion_sensor.get_yaw_angle()
    if counter_step == 0 and  cap < 5 and cap > -5  :
        counter -=1 
        counter_step = 1 
    elif counter_step == 1 and cap > 170 or cap < -170 :
        counter_step = 0

    matrix.show_number(counter)
    #Fw.Log.trace("setPoint:{} feedback:{} last_error:{} output:{} cap:{}   tours:{}"\
    #        .format(pid.SetPoint ,feedback , pid.last_error , pid.output ,cap , counter ))
    #time.sleep_ms(100)
car.stop()

# -- Exit Program --
Fw.Speaker.play_sound('Mission Accomplished')
raise Exception("Exit")