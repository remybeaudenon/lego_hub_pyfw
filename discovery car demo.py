from mindstorms.control import wait_for_seconds,Timer
from mindstorms import MSHub, Motor, MotorPair, DistanceSensor,ColorSensor
from micropython import const

import math,sys,urandom

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

        if name in Speaker.BRUITAGES or name in Speaker.VOIX  :
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

class Radar(DistanceSensor) :

    def __init__(self, port) :
        super().__init__(port)
        self.motor = Motor(RADAR_MOTOR_PORT)
        #self.data = { 45:0,315:0,90:0,270:0,0:0} # [angle:dist.]
        #self.order =[0,45,315,90,270 ] # choice
        self.data = { 80:0,280:0,0:0} # [angle:dist.]
        self.order =[0,80,280 ] # choice
        self.motor.set_stall_detection(True)
        self.motor.run_to_position(0,direction="shortest path",speed=20)
        self.activated = False

    def get_distance(self):
        numsamples = 3 # How many samples to avarage
        sumsamples = 0.0
        for i in range(numsamples):
            sample= self.get_distance_cm()
            if sample==None: sample=999 # Convert out-of-range to big number
            sumsamples += sample
        result = sumsamples / numsamples
        if TRACE : print("Radar:get_distance() lg {} mm".format(result))
        return result

    def set_angle(self,angle):
        correction = 0 # My motor has a 0-position that is 10 degrees off; correct yours here
        self.motor.run_to_position( angle+correction, direction="shortest path",speed=20)

    def spot(self,angle) :
        self.set_angle(angle)
        self.light_up_all(100)
        wait_for_seconds(0.5)
        distance = self.get_distance()
        self.data[angle] = distance
        self.show_distance(distance)
        self.light_up_all(0)
        if TRACE :print( "Radar.spot() angle: {} cm --> {} ".format(angle, self.data.get(angle)) )
        Speaker.play_sound('Hit')
        self.light_up_all(0)

    def spot_random(self,min,max) :
        angle  = urandom.randint(min,max)
        if angle < 0 : angle = 360 + angle 
        self.spot(angle)

    def scan(self):
        for angle in self.data.keys() :
            self.spot(angle)
        return

    def scan_y(self):
        for angle in self.data.keys() :
            self.spot(angle)
            yield
        yield

    def deactivate(self) :
        self.motor.run_to_position(0,direction="shortest path",speed=20)
        self.activated = False

    def show_distance(self,distance=0): 
        MatrixLight.off_menu()
        if distance <= 4 : 
            y_idx = 0  
        else: 
            y_idx   = int (distance/4) 
            if y_idx > 4 :  y_idx = 4 
        
        for y in range(0,5):
            hub.light_matrix.set_pixel(2,y,60)
        hub.light_matrix.set_pixel(2,y_idx,100)
        if TRACE :print( "Radar.show_distance() y_idx: {} cm --> {} ".format(y_idx, distance) )

    def show(self) :
        for angle in self.data.keys() :
            if TRACE : print( "Radar.show() angle: {} cm --> {} ".format(angle,self.data.get(angle)) )

    def get_bestFarWay(self) :
        max_distance = int(max(self.data.values()))
        for angle in self.order :
            distance = int(self.data.get(angle))
            if distance == max_distance :
                if angle > 180 : angle = -360 + angle
                return (angle,distance)
        return(None,None)

class Car(MotorPair):

    AVANT   = const(1)
    ARRIERE = const(-1)

    PERIMETRE_ROUE = const(17.5) # cm

    class Coder :

        GAUCHE  = const(0)
        DROIT   = const(1)

        def __init__(self, motorG, motorD) :
            self.motorG = Motor(motorG)
            self.motorD = Motor(motorD)
            self.init = self.start = self.get_positions()

        def get_positions(self) : # Incremented en sens Horaire, Decremente anti horaire
            wait_for_seconds(0.25)
            return (self.motorG.get_degrees_counted(), self.motorD.get_degrees_counted() )

        def start_positions(self) : # Incremented en sens Horaire, Decremente anti horaire
            self.start = self.get_positions()
            return self.start

        def get_diff_positions(self) : # Incremented en sens Horaire, Decremente anti horaire
            self.positions = self.get_positions()
            self.diff= (abs(self.start[self.GAUCHE] - self.positions[self.GAUCHE] ) ,\
                        abs(self.start[self.DROIT] - self.positions[self.DROIT] ) )
            return self.diff

    def __init__(self, motorG, motorD) :
        super().__init__(motorG,motorD)
        self.coder = Car.Coder(motorG,motorD)

    def move_tank_cm(self, cm , sens):
        self.move_tank(self, round( cm * 360 / Car.PERIMETRE_ROUE ) , sens )

    def move_tank(self, offset , sens):

        if sens < 0 :
            sens = -1
        else :sens = 1

        cap = hub.motion_sensor.get_yaw_angle()
        self.coder.start_positions()

        if TRACE : print("Car:drive() START| cap:{} | pos.start:{} --> offset: {}".format \
                        (cap, self.coder.start[Car.Coder.DROIT] ,offset))

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
            eccart =self.coder.get_diff_positions()[Car.Coder.DROIT]
            error = abs(offset) - eccart
            control_vit = int(kp_vit * (error/100 ) )
            if power0 + control_vit > 75 : control_vit = 75 - power0# Maxi 75%

            leftpower= int( (power0 * sens) + (control_vit * sens ) ) #+control_cap)
            rightpower= int( (power0 * sens) + (control_vit * sens) )#-control_cap)
            cont =abs(offset) - self.coder.get_diff_positions()[Car.Coder.DROIT] > 4
            if TRACE : print(" error: {} leftpower: {}rightpower:{} ".format(error, leftpower,rightpower) )

            self.start_tank_at_power(leftpower,rightpower)
        self.stop()

        if TRACE : print("Car:drive() STOP| cap:{} | pos.start: {} +offset:{} = {} ".format \
                        (hub.motion_sensor.get_yaw_angle(), self.coder.start[Car.Coder.DROIT] , \
                        offset, self.coder.get_positions()[Car.Coder.DROIT] ))


    # Rotates the car on its place so that its yaw() becomes `target` (using P-control).
    def rotate(self,target):
        ntarget = (180+target) % 360 - 180 # normalize target to be in -180..+180 range
        if TRACE : print("Car:rotate() target=", target,"(", hub.motion_sensor.get_yaw_angle()," --> ",ntarget,")")
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
        return self.coder.get_positions()

class TimerCtrl(Timer) :

    def __init__(self) :
        super()
        self.start_time = 0
        self.stop_time  = 0 
        self.activated = False

    def start(self): 
        self.start_time = self.now()
        self.activated  = True

    def lap(self): 
        if self.activated :
            return self.now() - self.start()
        else : 
            return 0 

    def stop(self): 
        self.stop = self.now()
        self.activated = False 

    def wait_y(self,sec):
        while self.now() < sec :
            yield
 
class ColorSensorCtrl(ColorSensor) :

    def __init__(self, port) :
        super().__init__(port)
        #self.light_up_all(10) si utilisé plus de detection de couleur
        self.light_up(0, 0, 0)
        self.previous_color = None
        self.activated = False 

    def scan_check(self) :
        self.light_up(100, 100, 100)
        color = self.get_color()
        if color != self.previous_color :
            if color == None :
                StatusLight.on('white')
            else :
                StatusLight.on(color)
                Speaker.play_sound('Scanning')
            self.previous_color = color

    def off(self):
        StatusLight.off()
        self.light_up(0, 0, 0)
        
class BoutonsCtrl():
    def __init__(self) :
        self.left   = hub.left_button.was_pressed() 
        self.right  = hub.right_button.was_pressed() 
        self.activated = False 

    def checks(self) :         
        self.left = hub.left_button.was_pressed()
        self.right = hub.right_button.was_pressed()
        return (self.left,self.right)

class MenuCtrl() : 

    A = const(65) #Ascii code 
    B = const(66) #Ascii code
    C = const(67) #Ascii code 
    D = const(68) #Ascii code  
    E = const(69) #Ascii code 
    F = const(70) #Ascii code  
    X = const(88) #Ascii code 'No choice'    

    DOT_LIST = {'A':(0,0),'B':(4,0),'C':(0,2),'D':(4,2),'E':(0,4),'F':(4,4)}
    CHECK_LIST = {'A':False,'B':False,'C':False,'D':False,'E':False,'F':False}

    def __init__(self) :
        self.left   = hub.left_button.was_pressed() 
        self.right  = hub.right_button.was_pressed() 
        
        self.menu_item =  MenuCtrl.X
        self.menu_item_selected =  MenuCtrl.A 
        self.timer = Timer()

        self.item_list = []
        self.activated = True 

    def update_y(self) :         

        self.left = hub.left_button.was_pressed()
        self.right = hub.right_button.was_pressed()

        # --- Buttons action -- 
        if self.left : 
            if self.menu_item != MenuCtrl.X :
                self.menu_item = MenuCtrl.X
            else:    
                self.menu_item_selected += 1
                if self.menu_item_selected  > MenuCtrl.F : self.menu_item_selected = MenuCtrl.A 

        if self.right : 
            if self.menu_item == self.menu_item_selected :
                check = MenuCtrl.CHECK_LIST.get(chr(self.menu_item))
                MenuCtrl.CHECK_LIST[chr(self.menu_item)] = not check
            else :
                self.menu_item = self.menu_item_selected

        # -- Matrix update ---
        for item in MenuCtrl.DOT_LIST.keys() : 
            dot = MenuCtrl.DOT_LIST.get(item)
            check = MenuCtrl.CHECK_LIST.get(item)

            if ord(item) == self.menu_item_selected :
                if self.menu_item == MenuCtrl.X : # mode edition 
                    if (self.timer.now() % 2 == 0 ) :
                        if check : 
                            hub.light_matrix.set_pixel(dot[0], dot[1], 100)
                        else : 
                            hub.light_matrix.set_pixel(dot[0], dot[1], 65)
                    else :
                        hub.light_matrix.set_pixel(dot[0], dot[1], 0)
                else : 
                    if check : 
                        hub.light_matrix.set_pixel(dot[0], dot[1], 100)
                    else : 
                        hub.light_matrix.set_pixel(dot[0], dot[1], 80)
            elif check :
                hub.light_matrix.set_pixel(dot[0], dot[1], 100)
            else :
                hub.light_matrix.set_pixel(dot[0], dot[1], 0)

        # --- Update Selection active item list 
        self.item_list = [] 
        for item in MenuCtrl.CHECK_LIST : 
            check = MenuCtrl.CHECK_LIST.get(item)
            if check: 
                self.item_list.append(item)
        self.item_list.append(chr(self.menu_item))
           
    def getAllSelection(self) : 
        return self.item_list
    
    def getMenuItem(self) :
        return chr(self.menu_item) 
    
    def isMenuItem(self,menu_item):
        return menu_item in self.item_list 

# ---------------------------------------------
# ---------- Process  loop --------------------
#
class ProcessCtrl():

    @staticmethod
    def speaker(item_menu) :
        timer       = TimerCtrl()
        while True:
            while menuCtrl.isMenuItem(item_menu):
                Speaker.play_random()
                timer.reset()
                yield from timer.wait_y(30)
            yield

    @staticmethod
    def statusLight(item_menu) :
        light_button = StatusLight()
        timer       = TimerCtrl()
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
        matrix  = MatrixLight()
        timer   = TimerCtrl()
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
        radar   = Radar(RADAR_SENSOR_PORT)
        timer   = TimerCtrl()
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
        sensor  = ColorSensorCtrl(COLOR_SENSOR_PORT)
        timer   = TimerCtrl()
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

# Create the cooperative tasks instance with Menu Item 
func_matrix         = ProcessCtrl.matrixLight('A')
func_light_button   = ProcessCtrl.statusLight('B')
func_color_scanner  = ProcessCtrl.color_scanner('C')
func_radar          = ProcessCtrl.radar('D')
func_speaker        = ProcessCtrl.speaker('E')

func_menu_ihm       = ProcessCtrl.menu_control()

# ----Main Program----
TRACE = False
if TRACE : print('Main:Thread() Welcome to Discovery Hub os:{} car version:{}'.format(sys.platform ,sys.version))


# -- Port des capteurs ---

PAIR_MOTOR_PORTS   =('A','B')
RADAR_MOTOR_PORT   ='C'  
COLOR_SENSOR_PORT  ='E'
RADAR_SENSOR_PORT  ='F'

hub    = MSHub()
Speaker.beep3()

# -- global instance 
menuCtrl = MenuCtrl()

#--- Loop
while True :

    next(func_menu_ihm)

    next(func_light_button)
    next(func_color_scanner)
    next(func_matrix)

    next(func_radar)
    next(func_speaker)

    #car     = Car("A","B")
    # car.coder.start_positions()
    #pos = car.rotate(target)
    #diff = car.coder.get_diff_positions()
    #print("yaw car {} --> position G {} D {}".format(target, diff[0],diff[1]))
    #car.move_tank_cm(20.0,Car.AVANT)
    #if TRACE : wait_for_seconds(2)
    #car.move_tank_cm(20.0,Car.ARRIERE)
    #if TRACE : print('item menu: {}'.format(menu_item))
    #if TRACE : wait_for_seconds(1)

