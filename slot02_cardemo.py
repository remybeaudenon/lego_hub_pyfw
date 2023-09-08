"""
    DECANUM - Robot Inventor MicroPython Software -
    Project    : Framework for LEGO Robot Inventor MSHub
    Application : slot02_cardemo.py
    Libraries   : slot15_baseline  '1.0.3-0822'
    Auth        : remybeaudenon@yahoo.com
    Date        : 08/2023
"""
import hub, time
from mindstorms.control import wait_for_seconds
from micropython import const
from mindstorms import MSHub
import sys,util


def import_from_slot(slot) :
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
hub.light_matrix.off()
# ---------------------------------------------
# ---------- Process Tasks loop ---------------
# ---------------------------------------------

class ProcessCtrl():

    @staticmethod
    def speaker(item_menu) :
        timer    = Fw.TimerCtrl()
        while True:
            while menuCtrl.isMenuItem(item_menu):
                Fw.Speaker.play_random()
                timer.reset()
                yield from timer.wait_y(30)
            yield

    @staticmethod
    def statusLight(item_menu) :
        light_button = Fw.StatusLight()
        timer        = Fw.TimerCtrl()
        while True:
            while menuCtrl.isMenuItem(item_menu):
                light_button.activated = True
                light_button.show_random()
                timer.reset()
                yield from timer.wait_y(3)
            if light_button.activated :
                light_button.off()
                light_button.activated = False
            yield

    @staticmethod
    def matrixLight(item_menu) :
        matrix= Fw.MatrixLight()
        timer= Fw.TimerCtrl()
        while True:
            while menuCtrl.isMenuItem(item_menu):
                matrix.activated = True
                matrix.show_img_random()
                timer.reset()
                yield from timer.wait_y(2)
            if matrix.activated :
                matrix.off_menu()
                matrix.activated = False
            yield

    @staticmethod
    def radar(item_menu) :
        radar= Fw.Radar(RADAR_SENSOR_PORT)
        timer= Fw.TimerCtrl()
        func_radar_scan = radar.scan_y()
        while True:
            while menuCtrl.isMenuItem(item_menu):
                radar.activated = True
                try :
                    next(func_radar_scan)
                except StopIteration:
                    func_radar_scan = radar.scan_y()
                timer.reset()
                yield from timer.wait_y(5)
            if radar.activated:
                radar.deactivate()
            yield

    @staticmethod
    def color_scanner(item_menu):
        sensor= Fw.ColorSensorCtrl(COLOR_SENSOR_PORT)
        timer= Fw.TimerCtrl()
        while True:
            while menuCtrl.isMenuItem(item_menu):
                sensor.activated = True
                sensor.scan_check()
                timer.reset()
                yield from timer.wait_y(1)
            if sensor.activated :
                sensor.off()
                sensor.activated = False
            yield

    @staticmethod
    def menu_control():
        while True :
            yield menuCtrl.update_y()

# Create the cooperative tasks instance with linked menu Item
func_matrix        = ProcessCtrl.matrixLight('A')
func_light_button= ProcessCtrl.statusLight('B')
func_color_scanner= ProcessCtrl.color_scanner('C')
func_radar        = ProcessCtrl.radar('D')
func_speaker        = ProcessCtrl.speaker('E')

func_menu_ihm    = ProcessCtrl.menu_control()

# ----Main Program----

TRACE = True # Enable or desable flag
Fw.Log.trace('Main:Thread() Welcome to Discovery Hub os:{} car version:{} fw:{}'. \
               format(sys.platform ,sys.version,Fw.LegoFw.__VERSION__))

# -- Sensors port---
PAIR_MOTORS_PORT    = ('A','B')
RADAR_MOTOR_PORT    = 'C'
COLOR_SENSOR_PORT   = 'E'
RADAR_SENSOR_PORT   = 'F'
CODER_MOTOR_PORT    = 'D'

# -- global instance ---
hub    = MSHub()
menuCtrl = Fw.MenuCtrl()

#car = Car(PAIR_MOTORS_PORT)

#--- Loop ---
Fw.Speaker.beep3()

while True :

    next(func_menu_ihm)

    next(func_light_button)
    next(func_color_scanner)
    next(func_matrix)

    next(func_radar)
    next(func_speaker)
# ---------------------------------------------
# ---------- Process Tasks loop ---------------
# ---------------------------------------------

class ProcessCtrl():

    @staticmethod
    def speaker(item_menu) :
        timer    = TimerCtrl()
        while True:
            while menuCtrl.isMenuItem(item_menu):
                Speaker.play_random()
                timer.reset()
                yield from timer.wait_y(30)
            yield

    @staticmethod
    def statusLight(item_menu) :
        light_button = StatusLight()
        timer        = TimerCtrl()
        while True:
            while menuCtrl.isMenuItem(item_menu):
                light_button.activated = True
                light_button.show_random()
                timer.reset()
                yield from timer.wait_y(3)
            if light_button.activated :
                light_button.off()
                light_button.activated = False
            yield

    @staticmethod
    def matrixLight(item_menu) :
        matrix= MatrixLight()
        timer= TimerCtrl()
        while True:
            while menuCtrl.isMenuItem(item_menu):
                matrix.activated = True
                matrix.show_img_random()
                timer.reset()
                yield from timer.wait_y(2)
            if matrix.activated :
                matrix.off_menu()
                matrix.activated = False
            yield

    @staticmethod
    def radar(item_menu) :
        radar= Radar(RADAR_SENSOR_PORT)
        timer= TimerCtrl()
        func_radar_scan = radar.scan_y()
        while True:
            while menuCtrl.isMenuItem(item_menu):
                radar.activated = True
                try :
                    next(func_radar_scan)
                except StopIteration:
                    func_radar_scan = radar.scan_y()
                timer.reset()
                yield from timer.wait_y(5)
            if radar.activated:
                radar.deactivate()
            yield

    @staticmethod
    def color_scanner(item_menu):
        sensor= ColorSensorCtrl(COLOR_SENSOR_PORT)
        timer= TimerCtrl()
        while True:
            while menuCtrl.isMenuItem(item_menu):
                sensor.activated = True
                sensor.scan_check()
                timer.reset()
                yield from timer.wait_y(1)
            if sensor.activated :
                sensor.off()
                sensor.activated = False
            yield

    @staticmethod
    def menu_control():
        while True :
            yield menuCtrl.update_y()

# Create the cooperative tasks instance with linked menu Item
func_matrix        = ProcessCtrl.matrixLight('A')
func_light_button= ProcessCtrl.statusLight('B')
func_color_scanner= ProcessCtrl.color_scanner('C')
func_radar        = ProcessCtrl.radar('D')
func_speaker        = ProcessCtrl.speaker('E')

func_menu_ihm    = ProcessCtrl.menu_control()

# ----Main Program----

TRACE = True # Enable or desable flag
Log.trace('Main:Thread() Welcome to Discovery Hub os:{} car version:{} fw:{}'. \
               format(sys.platform ,sys.version,LegoFw.__VERSION__))

# -- Sensors port---
PAIR_MOTORS_PORT    = ('A','B')
RADAR_MOTOR_PORT    = 'C'
COLOR_SENSOR_PORT   = 'E'
RADAR_SENSOR_PORT   = 'F'
CODER_MOTOR_PORT    = 'D'

# -- global instance ---
hub    = MSHub()
menuCtrl = MenuCtrl()

#car = Car(PAIR_MOTORS_PORT)

#--- Loop ---
Speaker.beep3()

while True :

    next(func_menu_ihm)

    next(func_light_button)
    next(func_color_scanner)
    next(func_matrix)

    next(func_radar)
    next(func_speaker)
#--- Loop ---

# -- Exit Program --
Fw.Speaker.play_sound('Mission Accomplished')
raise Exception("Exit")

