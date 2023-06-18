
"""
    DECANUM - Robot Inventor MicroPython Software -
    Project    : Framework for LEGO Robot Inventor MSHub
    Application: Tools
    Auth        : remybeaudenon@yahoo.com
    Date        : 06/2023
"""
from mindstorms.control import wait_for_seconds,Timer
from mindstorms import MSHub, Motor, MotorPair, DistanceSensor,ColorSensor
from micropython import const
import math,sys,urandom,time

class LegoFw : 
    __VERSION__ ='1.0.1-0611'

class Log():

    @staticmethod
    def trace(data) :

        if not TRACE :
            return

        data_string =''
        if (type(data) == str ) :
            data_string = data
        elif (type(data) == list or type(data) == dict ) :
            data_string = ' ' + repr(data)
        elif (type(data) == int or type(data) == float ):
            data_string = ' ' + '{} value:{}'.format(type(data),data)
        else :
            data_string = 'Log:_writedata can\'t be converted.. {}'.format(type(data))
        header_record = ''
        lt= time.localtime()
        nowDay= '{:03d}'.format(lt[7])
        nowTime = '{:02d}:{:02d}:{:02d}'.format(lt[3],lt[4],lt[5])

        header_record = '{}\t{}'.format( nowDay,nowTime)
        line = header_record + data_string
        print(line)

class Speaker() :

    BRUITAGES = ['Activate','Affirmative','Bing','Bowling','Brick Eating','Bumper','Celebrate','Charging','Chuckle',\
            'countdown','Countdown Tick','Damage','Deactivate','Dial Down','Dial Up','Error','Explosion',\
            'Failure Chime','Fire','Flutter','Glitch','Goal','Grab','Growl',\
            'Hammer','Hit','Horn','Hydraulics Down','Hydraulics Up','Initialize','Kick','Laser',\
            'Ping','play','Power Down','Power Up','Punch','Reverse',\
            'Revving','Scanning','Shake','Shooting','Shut Down ','Slam Dunk','Slow down',\
            'Sonic Explosion','Static','Stomp','Strike','Success Chime','Theremin',\
            'Tweet','Void','Warp Speed','Whirl','Zap'
            ]
    VOIX = ['1234','Delivery','Dizzy','Exterminate','Goodbye','Ha','Ha Ha','Ha Ha Ha','Hello','Hi','HI 5','Hit','Humming','Laugh',\
            'Like','Mission Accomplished','No','Oh','Oh No','Oh Oh','Ouch','Sad','Seek and Destroy','Scared','Tadaa','Target Acquired','Target Destroyed',\
            'Void','Wow','Yes','Yipee','Yuck'
            ]

    @staticmethod
    def beep3():
        hub.speaker.beep(60, 0.1)
        hub.speaker.beep(70, 0.1)
        hub.speaker.beep(62, 0.1)

    @staticmethod
    def beep():
        hub.speaker.beep(60, 0.2)

    def play_sound(name = 'Bing') :

        if name in Speaker.BRUITAGES or name in Speaker.VOIX:
            hub.speaker.play_sound(name)
        else :
            hub.speaker.play_sound('Void')

    @staticmethod
    def play_all():

        for son in Speaker.VOIX :
            print(son)
            hub.speaker.play_sound(son)
            wait_for_seconds(2)

        for son in Speaker.BRUITAGES :
            print(son)
            hub.speaker.play_sound(son)
            wait_for_seconds(2)

    @staticmethod
    def play_random():

        select = urandom.randint(0,10)
        if select < 8 :
            index = urandom.randint(0,len(Speaker.VOIX) -1 )
            hub.speaker.play_sound(Speaker.VOIX[index])
        else :
            index = urandom.randint(0,len(Speaker.BRUITAGES) -1 )
            hub.speaker.play_sound(Speaker.BRUITAGES[index])

class StatusLight() :

    COLORS = ['azure','black','cyan','green','orange','pink','red','white','yellow']

    def __init__(self) :
        self.activated = False

    @staticmethod
    def on(color = 'white'):
        if color in StatusLight.COLORS :
            hub.status_light.on(color)
            return
        hub.status_light.on('white')

    @staticmethod
    def show_all():

        for color in StatusLight.COLORS :
            print(color)
            hub.status_light.on(color)
            wait_for_seconds(1)

    @staticmethod
    def show_random():
        index = urandom.randint(0,len(StatusLight.COLORS) -1 )
        hub.status_light.on(StatusLight.COLORS[index])

    @staticmethod
    def off():
        hub.status_light.off()

class MatrixLight() :

    PICTURES = ['ANGRY','ARROW_E','ARROW_N','ARROW_NE','ARROW_NW','ARROW_S','ARROW_SE','ARROW_SW','ARROW_W',\
                'ASLEEP','BUTTERFLY','CHESSBOARD','CLOCK1','CLOCK10','CLOCK11','CLOCK12','CLOCK2','CLOCK3','CLOCK4',\
                'CLOCK5','CLOCK6','CLOCK7','CLOCK8','CLOCK9','CONFUSED','COW','DIAMOND','DIAMOND_SMALL','DUCK','FABULOUS',\
                'GHOST','GIRAFFE','GO_RIGHT','GO_LEFT','GO_UP','GO_DOWN','HAPPY','HEART','HEART_SMALL','HOUSE','MEH',\
                'MUSIC_CROTCHET','MUSIC_QUAVERS','NO','PACMAN','PITCHFORK','RABBIT','ROLLERSKATE','SAD','SILLY','SKULL', \
                'SMILE','SNAKE','SQUARE','SQUARE_SMALL','STICKFIGURE','SURPRISED','SWORD','TARGET','TORTOISE','TRIANGLE',\
                'TRIANGLE_LEFT','TSHIRT','UMBRELLA','XMAS','YES' ]
    
    FONT_NUMBER = ['99999:99999','90090:99999','99909:90999','90909:99999','00990:99999','90999:99909',\
                   '99999:99909','99909:00099','99099:99099','90999:99999' ] 
    
    def __init__(self) :
        self.activated = False

    @staticmethod
    def show_pixels(pixels = '99999:77777:55555:33333:11111'):
        hub.light_matrix.show(pixels)

    def set_bin_image(bits) : # =0b_00000_00000_00100_00000_00000):
        hub.light_matrix.off()
        cur=1<<24
        for y in range(5):
            for x in range(5):
                if bits & cur : hub.light_matrix.set_pixel(x,y,100)
                cur >>= 1

    @staticmethod
    def show_number(number):
        if type(number) == int and number >=0 and number < 100 : 
            dizaine  = MatrixLight.FONT_NUMBER[int(number/10)] + ':00000:'
            unité    = MatrixLight.FONT_NUMBER[(number % 10)]  
            hub.light_matrix.show(dizaine+unité)


    @staticmethod
    def on(picture):
        if picture in MatrixLight.PICTURES :
            hub.light_matrix.show_image(picture)

    @staticmethod
    def show_img_random():
        index = urandom.randint(0,len(MatrixLight.PICTURES) -1 )
        hub.light_matrix.show_image(MatrixLight.PICTURES[index])

    @staticmethod
    def show_all():
        for picture in MatrixLight.PICTURES :
            if TRACE : print(picture)
            hub.light_matrix.show_image(picture)
            wait_for_seconds(1)

    @staticmethod
    def off():
        hub.light_matrix.off()

    @staticmethod
    def off_menu() :
        for y in [0,2,4]:
            for x in range(1,4):
                hub.light_matrix.set_pixel(x,y,0)
        for y in [1,3]:
            for x in range(0,5) :
                hub.light_matrix.set_pixel(x,y,0)

class ColorSensorCtrl(ColorSensor) :

    def __init__(self, port) :
        super().__init__(port)
        #self.light_up_all(10) si utilisé plus de detection de couleur
        #self.light_up(0, 0, 0)
        self.previous_color = None
        self.activated = False
        self.color  = None

    def scan_check(self) :
        self.light_up(100, 100, 100)
        self.color = self.get_color()
        if self.color != self.previous_color :
            if self.color == None :
                StatusLight.on('white')
            else :
                StatusLight.on(self.color)
                Speaker.play_sound('Scanning')
            self.previous_color = self.color

    def off(self):
        StatusLight.off()
        self.light_up(0, 0, 0)

class Coder(Motor) :

    def __init__(self, motor_port) :
        super().__init__(motor_port)
        self.motor_port = motor_port
        self.init = self.start = self.diff = 0
        self.position = self.get_degrees_counted()
        
        #self.run_to_position(0, 'shortest path', 30)

    def get_position(self) : # Incremented en sens Horaire, Decremente anti horaire
        try :
            self.position = self.get_degrees_counted()
            return self.position
        except RuntimeError as re : 
            Log.trace("Coder.get_position() Error:{}".format(re) )
        return self.position
    
    def start_position(self) : # Incremented en sens Horaire, Decremente anti horaire
        self.start = self.get_position()
        return self.start

    def get_diff_position(self) : # Incremented en sens Horaire, Decremente anti horaire
        self.position = self.get_position()
        self.diff= self.start - self.position
        return self.diff

class ManetteDrive(Coder) : 

    POURCENT_MINI   = const(-50)
    POURCENT_MAXI   = const(50)

    def __init__(self) :
        super().__init__(MANETTE_MOTOR_PORT)
        self.value = 0
        self.start_position()
        #self.run_to_position(0, 'shortest path', 30)
 
    def scale(self,value) : 
        return min(ManetteDrive.POURCENT_MAXI, max(ManetteDrive.POURCENT_MINI, value))

    def update_y(self) :
        yield self.getValue()

    def getValue(self):
        self.value = self.scale(self.get_position())
        return self.value

    def setValue(self,value):
        if type(value) == int :
            self.value = self.scale(value)
            self.run_to_position(self.value, 'shortest path', 30)




class Car(MotorPair,Coder):

    AVANT= const(1)
    ARRIERE = const(-1)

    PERIMETRE_ROUE = const(175) # mm

    def __init__(self) :
        MotorPair.__init__(self,PAIR_MOTORS_PORT[0],PAIR_MOTORS_PORT[1]) 
        Coder.__init__(self,PAIR_MOTORS_PORT[1])


    def move_cm(self, cm , sens):
        self.move_tank(cm * sens  , "cm", 25, 25)

    def rotate_to_cap(self, offset , sens):

        if sens < 0 :
            sens = -1
        else :sens = 1

        cap = hub.motion_sensor.get_yaw_angle()
        self.start_positions()

        Log.trace("Car:drive() START| cap:{} | pos.start:{} --> offset: {}".format \
                        (cap, self.start ,offset))

        power0 = 27 # Mini

        kp_cap= 0.7
        kp_vit = 2

        cont = True

        #accelerations =[ power0 , power0 + 10 , power0 + 15 , power0 + 30 , power0+50 ]
        while cont :

            # P Reguration CAP
            yaw = hub.motion_sensor.get_yaw_angle()
            error = cap - yaw
            if error > +180: error = -(error - 180)
            if error < -180: error = -(error + 180)
            control_cap = kp_cap * error

            # P Reguration vitesse
            eccart =self.get_diff_positions()
            error = abs(offset) - eccart
            control_vit = int(kp_vit * (error/100 ) )
            if power0 + control_vit > 75 : control_vit = 75 - power0# Maxi 75%

            leftpower= int( (power0 * sens) + (control_vit * sens ) ) #+control_cap)
            rightpower= int( (power0 * sens) + (control_vit * sens) )#-control_cap)
            cont =abs(offset) - self.get_diff_positions() > 4
            Log.trace(" error: {} leftpower: {}rightpower:{} ".format(error, leftpower,rightpower) )

            self.start_tank_at_power(leftpower,rightpower)
        self.stop()

        Log.trace("Car:drive() STOP| cap:{} | pos.start: {} +offset:{} = {} ".format \
                    (hub.motion_sensor.get_yaw_angle(), self.start , \
                    offset, self.get_positions() ))


    # Rotates the car on its place so that its yaw() becomes `target` (using P-control).
    def rotate(self,target):
        ntarget = (180+target) % 360 - 180 # normalize target to be in -180..+180 range
        Log.trace("Car:rotate() target=", target,"(", hub.motion_sensor.get_yaw_angle()," --> ",ntarget,")")
        kp = 0.1
        power0 = 20
        cont = True
        while cont:
            yaw = hub.motion_sensor.get_yaw_angle()
            error = ntarget - yaw
            if error > +180: error = -(error - 180)
            if error < -180: error = -(error + 180)
            control = kp * error
            power = int(math.copysign(power0,control)+control)
            cont = math.fabs(error) > 4
            self.start_tank_at_power(power,-power)
        self.stop()
        return self.get_positions()

class TimerCtrl(Timer) :

    def __init__(self) :
        super()
        self.start_time = 0
        self.stop_time  = 0
        self.activated  = False

    def start(self):
        self.start_time = self.now()
        self.activated  = True

    def lap(self):
        if self.activated :
            return self.now() - self.start()
        else :
            return 0

    def stop(self):
        self.stop       = self.now()
        self.activated  = False

    def wait_y(self,sec):
        while self.now() < sec :
            yield

class BoutonsCtrl():
    def __init__(self) :
        self.left= hub.left_button.was_pressed()
        self.right= hub.right_button.was_pressed()
        self.activated = False

    def checks(self) :
        self.left = hub.left_button.was_pressed()
        self.right = hub.right_button.was_pressed()
        return (self.left,self.right)

class Bouton() : 
    def __init__(self) :
        self.etat = False 
        self.top  = False

    def isOn(self) :
        return self.etat

class BoutonOptique(Bouton,ColorSensorCtrl) : 

    RED= 'red'

    def __init__(self) :
        Bouton.__init__(self) 
        ColorSensorCtrl.__init__(self,COLOR_SENSOR_PORT)
        StatusLight.on('green')  
        self.sound = False  

    def update_y(self) : 
        color_value = self.get_color()

        if color_value != self.previous_color :
            if color_value == BoutonOptique.RED :
                if not self.etat :
                    self.on()
                else :
                    self.off()

            self.previous_color = color_value
    
    def off(self) : 
        self.etat = False
        StatusLight.on('green')    
        if self.sound : Speaker.play_sound("Power Down")

    def on(self) : 
        self.etat = True
        StatusLight.on('pink')    
        if self.sound : Speaker.play_sound("Power Up")



class ColorSensorCtrl(ColorSensor) :

    def __init__(self, port) :
        super().__init__(port)
        #self.light_up_all(10) si utilisé plus de detection de couleur
        #self.light_up(0, 0, 0)
        self.previous_color = None
        self.activated = False
        self.color  = None

    def scan_check(self) :
        self.light_up(100, 100, 100)
        self.color = self.get_color()
        if self.color != self.previous_color :
            if self.color == None :
                StatusLight.on('white')
            else :
                StatusLight.on(self.color)
                Speaker.play_sound('Scanning')
            self.previous_color = self.color

    def off(self):
        StatusLight.off()
        self.light_up(0, 0, 0)

# ---------------------------------------------
# ---------- Process Tasks loop ---------------
# ---------------------------------------------

class ProcessCtrl():

    @staticmethod
    def dummy() :
        timer    = TimerCtrl()
        while True:
            while True:
                Speaker.play_random()
                timer.reset()
                yield from timer.wait_y(30)
            yield
    @staticmethod
    def bouton_optique() :
        #bo = BoutonOptique()
        while True:
            yield bo.update_y()

    @staticmethod
    def manette_drive() :
        while True:
            yield manette.update_y()


    @staticmethod
    def run() :
        car =Car()
        timer = TimerCtrl()

        car.set_stop_action('hold')
        car_puissance  = 35
        car.set_default_speed(car_puissance)
        volant_previous = None
        timer_previous  = 0
        MatrixLight.show_number(timer_previous)  

        while True:
            while bo.isOn() and timer_previous < 30 :
                volant = manette.getValue()
                if volant_previous == None : 
                    manette.setValue(0)
                    timer.start()

                if volant_previous != volant : 
                    car.start_at_power(car_puissance, volant)
                    volant_previous = volant
                if timer_previous != timer.now() : 
                    timer_previous = timer.now()
                    MatrixLight.show_number(timer_previous)
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
Log.trace('Main:Thread() Welcome to Discovery Hub os:{} car version:{} fw:{}'. \
               format(sys.platform ,sys.version,LegoFw.__VERSION__))

# -- Sensors port---
PAIR_MOTORS_PORT    = ('A','B')
RADAR_MOTOR_PORT    = 'C'
COLOR_SENSOR_PORT   = 'E'
RADAR_SENSOR_PORT   = 'F'
MANETTE_MOTOR_PORT  = 'D'

# -- global instance ---
hub    = MSHub()
Speaker.beep3()

bo = BoutonOptique()
manette = ManetteDrive()

#--- Loop ---
while True :
    next(func_bouton_optique)
    next(func_run)
    next(func_manette_drive)


#--- Loop ---



