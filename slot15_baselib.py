"""
    DECANUM - Robot Inventor MicroPython Software -
    Project    : Framework for LEGO Robot Inventor 51515
    Application: slot15_baselib.py
    Auth        : remybeaudenon@yahoo.com
    Date        : 06/2023
"""
from mindstorms.control import wait_for_seconds,Timer
from mindstorms import MSHub, Motor, MotorPair, DistanceSensor,ColorSensor
from micropython import const
import math,sys,urandom,time,gc

class LegoFw :
    __VERSION__ ='2.0.0-0927'

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

        header_record = '{}|{} > '.format( nowDay,nowTime)
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
    def exit() :
        hub.speaker.play_sound('Mission Accomplished')
        raise Exception("Exit")

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
            dizaine= MatrixLight.FONT_NUMBER[int(number/10)] + ':00000:'
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
        angle= urandom.randint(min,max)
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
            y_idx= int (distance/4)
            if y_idx > 4 :y_idx = 4

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

    def start_position(self) : # Incremented en sens Horaire, Decremente anti horaire
        self.start = self.get_position()
        return self.start

    def get_diff_position(self) : # Incremented en sens Horaire, Decremente anti horaire
        self.position = self.get_position()
        self.diff= self.start - self.position
        return self.diff

class Manette(Coder):

    POURCENT_MINI= const(-50)
    POURCENT_MAXI= const(50)
    RESOLUTION    = const(1)        # [1 to 5 ]1 reactive --> 5 souple
    SENS            = const(-1)    # [-1,+1]
    POINTS        = ( POURCENT_MAXI - POURCENT_MINI) * RESOLUTION
    STEP            = 5            # Ouput increment Step

    def __init__(self) :
        super().__init__(MANETTE_MOTOR_PORT)
        self.value = 0
        self.start_position()

    def setValue(self,value):
        if type(value) == int :
            self.value = self.scale(value)

    def getValue(self):
        diff_degrees = self.get_diff_position()
        self.start_position()

        points = int( diff_degrees / Manette.RESOLUTION ) * Manette.SENS
        points = int(points/Manette.STEP) * Manette.STEP
        points += self.value
        self.value= self.scale(points)
        return self.value

    def scale(self,value) :
        return min(Manette.POURCENT_MAXI, max(Manette.POURCENT_MINI, value))

class ManetteDrive(Coder) :

    POURCENT_MIN= const(-50)
    POURCENT_MAX= const(50)

    def __init__(self) :
        super().__init__(MANETTE_MOTOR_PORT)
        self.value = 0
        self.start_position()
        #self.run_to_position(0, 'shortest path', 30)

    def scale(self,value) :
        return min(ManetteDrive.POURCENT_MAX, max(ManetteDrive.POURCENT_MIN, value))

    def update_y(self) :
        yield self.getValue()

    def getValue(self):
        self.value = self.scale(self.get_position())
        return self.value

    def setValue(self,value):
        if type(value) == int :
            self.value = self.scale(value)
            self.run_to_position(self.value, 'shortest path', 30)


class PID:
    """PID Controller
    """
    def __init__(self, P=0.2, I=0.0, D=0.0, current_time=None):

        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 0.00
        self.current_time = current_time if current_time is not None else time.time()
        self.last_time = self.current_time

        self.clear()

    def clear(self):
        """Clears PID computations and coefficients"""
        self.SetPoint = 0.0

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.int_error = 0.0
        self.windup_guard = 20.0

        self.output = 0.0

    def update(self, feedback_value, current_time=None):
        """Calculates PID value for given reference feedback

        .. math::
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}

        .. figure:: images/pid_1.png
        :align:center

        Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)

        """
        error = self.SetPoint - feedback_value

        ####Ticky add
        if feedback_value == 0 :
            error = 0
        elif feedback_value > self.setPoint :
            error = 10
        else:
            error = - 10
        ################################"
        # "
        self.current_time = current_time if current_time is not None else time.time()
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error

        if (delta_time >= self.sample_time):
            self.PTerm = self.Kp * error
            self.ITerm += error * delta_time

            if (self.ITerm < -self.windup_guard):
                self.ITerm = -self.windup_guard
            elif (self.ITerm > self.windup_guard):
                self.ITerm = self.windup_guard

            self.DTerm = 0.0
            if delta_time > 0:
                self.DTerm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = error

            self.output = self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)

    def setKp(self, proportional_gain):
        """Determines how aggressively the PID reacts to the current error with setting Proportional Gain"""
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        """Determines how aggressively the PID reacts to the current error with setting Integral Gain"""
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        """Determines how aggressively the PID reacts to the current error with setting Derivative Gain"""
        self.Kd = derivative_gain

    def setWindup(self, windup):
        """Integral windup, also known as integrator windup or reset windup,
        refers to the situation in a PID feedback controller where
        a large change in setpoint occurs (say a positive change)
        and the integral terms accumulates a significant error
        during the rise (windup), thus overshooting and continuing
        to increase as this accumulated error is unwound
        (offset by errors in the other direction).
        The specific problem is the excess overshooting.
        """
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        """PID that should be updated at a regular interval.
        Based on a pre-determined sampe time, the PID decides if it should compute or return immediately.
        """
        self.sample_time = sample_time


class Car(MotorPair):

    AVANT= DROIT=1
    ARRIERE = GAUCHE = -1
    PERIMETRE_ROUE = 175 # mm
    PUISSANCE_MINI = 25
    PUISSANCE_MAXI = 75
    RAMPE        = 200# 10 cm

    def __init__(self, pair_motors_port) :
        MotorPair.__init__(self,pair_motors_port[0],pair_motors_port[1])
        self.coder = Coder(pair_motors_port[1])

    def start_motors(self,volant, speed = None):
        self.start(self.scale(-100,100,volant), self.PUISSANCE_MINI if speed == None else speed)

    def move_cm(self, cm , sens):
        self.move_tank(cm * sens, "cm", 25, 25)

    def rotate_to_cap(self, offset , sens):

        if sens < 0 :
            sens = -1
        else :sens = 1

        cap = hub.motion_sensor.get_yaw_angle()
        self.coder.start_position()

        Log.trace("Car:rotate_to_cap() START| cap:{} | pos.start:{} --> offset: {}".format \
                        (cap, self.coder.start ,offset))

        power0 = 27 # Mini

        kp_cap= 0.7
        kp_vit = 2

        cont = True

        #accelerations =[ power0 , power0 + 10 , power0 + 15 , power0 + 30 , power0+50 ]
        while cont :

            # P Regulation CAP
            yaw = hub.motion_sensor.get_yaw_angle()
            error = cap - yaw
            if error > +180: error = -(error - 180)
            if error < -180: error = -(error + 180)
            control_cap = kp_cap * error

            # P Regulation vitesse
            eccart =self.coder.get_diff_position()
            error = abs(offset) - eccart
            control_vit = int(kp_vit * (error/100 ) )
            if power0 + control_vit > 75 : control_vit = 75 - power0# Maxi 75%

            leftpower= int( (power0 * sens) + (control_vit * sens ) ) #+control_cap)
            rightpower= int( (power0 * sens) + (control_vit * sens) )#-control_cap)
            cont =abs(offset) - self.coder.get_diff_position() > 4
            Log.trace("Car:rotate_to_cap() error: {} leftpower: {}rightpower:{} ".format(error, leftpower,rightpower) )

            self.start_tank_at_power(leftpower,rightpower)
        self.stop()

        Log.trace("Car:rotate_to_cap() STOP| cap:{} | pos.start: {} +offset:{} = {} ".format \
                    (hub.motion_sensor.get_yaw_angle(), self.start , \
                    offset, self.coder.get_position() ))


    # Rotates the car on its place so that its yaw() becomes `target` (using P-control).
    def old_rotate(self,target):
        ntarget = (180+target) % 360 - 180 # normalize target to be in -180..+180 range
        Log.trace("Car:rotate() target= {} ntarget= {} ".format(target ,ntarget))
        kp = 0.1
        power0 = 35
        cont = True
        while cont:
            yaw = hub.motion_sensor.get_yaw_angle()
            error = ntarget - yaw
            #if error > +180: error = -(error - 180)
            #if error <= -180: error = -(error + 180)
            control = kp * error
            power = int(math.copysign(power0,control)+control)
            #print("error: {} control:{} power {} ".format(error , control,power))
            cont = math.fabs(error) > 2
            self.start_tank_at_power(power,-power)
        self.set_stop_action('brake')
        self.stop()
    # Rotates the car on its place so that its yaw() becomes `target` (using P-control).

    def rotate(self,target):
        ntarget = (180+target) % 360 - 180 # normalize target to be in -180..+180 range
        Log.trace("Car:rotate() target= {} ntarget= {} ".format(target ,ntarget))
        power = self.PUISSANCE_MINI
        cont = True
        self.start_tank_at_power(power,-power)
        while cont:
            error = ntarget - hub.motion_sensor.get_yaw_angle()
            cont = math.fabs(error) > 2
        #self.set_stop_action('brake')
        self.stop()

    def scale(self,mini,maxi,value) :
        return min(maxi , max(mini, value))

class Tricky(Car) :

    AVANT= DROIT= const(1)
    ARRIERE = GAUCHE = const(-1)
    PERIMETRE_ROUE = const(175) # mm
    PAIR_MOTORS_PORT    = ('A','B')


    PUISSANCE_MINI = const(25)
    PUISSANCE_MAXI = const(75)
    RAMPE        = const(200) # 10 cm
    BREAK_ADVANCE=const(3)# coder Points

    def __init__(self) :
        Car.__init__(self,Tricky.PAIR_MOTORS_PORT)


    def mv_to_tempo (self,params) :#Warning !!! No stop after elapsted time

        p_drive= self.scale(-100,100,params[0])
        p_speed= abs(params[1])
        p_seconds = params[2]
        self.start_motors(p_drive , p_speed )
        time.sleep(p_seconds)

    def gyro_to_angle(self,params) :    # PARAM ( ANGLE 'Yaw'  GYROSCOPIQUE,)
    
        p_angle= self.scale(0,359,params[0])
        start_pos = self.coder.get_position()
        self.rotate(p_angle)
        self.coder.set_degrees_counted(start_pos)


    def mv_to_point(self, params) :# PARAM ( DRIVE,SPEED,POINTS )
        p_drive= self.scale(-100,100,params[0])
        p_speed= abs(params[1])
        p_points = params[2]
        start_pos = self.coder.get_position()
        distance_points = p_points - start_pos

        while ( distance_points >= 0 and self.coder.get_position() < ( p_points - self.BREAK_ADVANCE) ) or \
            ( distance_points< 0 and self.coder.get_position() > ( p_points + self.BREAK_ADVANCE) ) :

            position = self.coder.get_position()
            points_restant = abs(p_points - position)                                # 1cm --> 20 points
            if points_restant <= self.RAMPE :                                    # speed deceleration ramp activation.
                speed = max( self.PUISSANCE_MINI , round(points_restant / 5 ))

            elif abs(position - start_pos) < self.RAMPE :                        # speed acceleration ramp activation.
                speed = max( self.PUISSANCE_MINI, round(abs(position - start_pos ) / 5) )
            else :
                speed = p_speed                                                    # speed default param

            if speed > p_speed : speed = p_speed                            # check keep limitation
            if distance_points < 0 : speed = - speed                        # Foward/Reverse motor setter

            #Log.trace("Tricky:mv_to_point() DEBUG start_pos:{:7d} points_distance:{:04d} points_restant:{:04d} speed:{:03d} "\
            #                .format( start_pos,distance_points,points_restant,speed))

            self.start_motors( p_drive , speed )
        self.stop()


class MotorAux(Coder) :

    REVERSE = True

    def __init__(self, motor_port , reverse = False ) :
        super().__init__(motor_port)
        self.motor_port = motor_port
        self.reverse = reverse
        self.set_default_speed(20)

    def init(self) :
        self.run_to_position(0, 'shortest path')

    def angle(self, angle) :

        angle = self.scale(0,150,angle)
        if self.reverse :
            angle = 360 - angle

        self.run_to_position( angle , 'shortest path')

    def scale(self,mini,maxi,value) :
        return min(maxi , max(mini, value))


class TimerCtrl(Timer) :

    def __init__(self) :
        super()
        self.start_time = 0
        self.stop_time= 0
        self.activated = False
        self.save_time = 0

    def start(self):
        self.reset()
        self.start_time = self.save_time = self.now()
        self.activated= True

    def lap(self):
        if self.activated :
            return self.now() - self.start_time
        else :
            return 0

    def set_saveTime(self):
        if self.activated :
            self.save_time = self.now()

    def get_saveTime(self):
        return self.save_time

    def stop(self):
        self.stop = self.now()
        self.activated = False

    def wait_sec(self, seconds):
        self.set_saveTime()
        while self.lap() <= self.get_saveTime() + seconds:
            pass

    def wait_y(self,sec):
        while self.now() < sec :
            yield

class ColorSensorCtrl(ColorSensor) :

    def __init__(self, port) :
        super().__init__(port)
        #self.light_up_all(10) si utilisé plus de detection de couleur
        #self.light_up(0, 0, 0)
        self.previous_color = None
        self.activated = False
        self.color= None

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
        self.top= False

    def isOn(self) :
        return self.etat

class BoutonOptique(Bouton,ColorSensorCtrl) :

    RED= 'red'

    def __init__(self,sound = False) :
        Bouton.__init__(self)
        ColorSensorCtrl.__init__(self,COLOR_SENSOR_PORT)
        self.sound = sound

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

class MenuCtrl() :

    A = const(65) #Ascii code
    B = const(66) #Ascii code
    C = const(67) #Ascii code
    D = const(68) #Ascii code
    E = const(69) #Ascii code
    F = const(70) #Ascii code
    X = const(88) #Ascii code 'Edit Mode'

    DISPLAY_DOT_LIST = {'A':(0,0),'B':(4,0),'C':(0,2),'D':(4,2),'E':(0,4),'F':(4,4)}
    CHECK_LIST = {'A':False,'B':False,'C':False,'D':False,'E':False,'F':False}

    def __init__(self) :
        self.left= hub.left_button.was_pressed()
        self.right= hub.right_button.was_pressed()

        self.menu_item =MenuCtrl.X
        self.menu_item_selected =MenuCtrl.A
        self.timer = Timer()

        self.item_list = []
        self.activated = True

    def update_y(self) :

        self.left    = hub.left_button.was_pressed()
        self.right    = hub.right_button.was_pressed()
        self.right_r    = hub.right_button.is_released()

        # --- Buttons action --
        if self.left :
            if self.menu_item != MenuCtrl.X :
                self.menu_item = MenuCtrl.X
            else:
                self.menu_item_selected += 1
                if self.menu_item_selected> MenuCtrl.F : self.menu_item_selected = MenuCtrl.A

        if self.right :
            if self.menu_item == self.menu_item_selected :
                check = MenuCtrl.CHECK_LIST.get(chr(self.menu_item))
                MenuCtrl.CHECK_LIST[chr(self.menu_item)] = not check
            else :
                self.menu_item = self.menu_item_selected


        # -- Matrix update ---

        for item in MenuCtrl.DISPLAY_DOT_LIST.keys() :
            dot = MenuCtrl.DISPLAY_DOT_LIST.get(item)
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

class Select() :

    _PARAMS_SPEED = {'mini':25 ,'maxi':95 ,'increment':5 ,'init' : 50 ,'matrix_code':'55599:55995:99555:55995:55599'}
    _PARAMS_PROG_NUM = {'mini':1 ,'maxi':20 ,'increment':1 ,'init' : 0, 'matrix_code':'55555:99999:55959:55999:55555'}

    def __init__(self, params) :
        self.left    = hub.left_button.was_pressed()
        self.right    = hub.right_button.was_pressed()
        self.right_r    = hub.right_button.is_released()

        self.value    = 0
        self.timer    = Timer()
        self.edit    = True
        self.right_set= False
        self.params    = params
        self.value    = self.scale(self.params.get('init'))

    def isEditMode(self):
        return self.edit

    def setEditMode(self,flag) :
        if type(flag) == bool :
            self.edit = flag

    def waitValue(self):
        while self.isEditMode() :
            self.update()
        return self.getValue()

    def update(self):

        if self.edit :
            self.left    = hub.left_button.was_pressed()
            self.right    = hub.right_button.was_pressed()
            self.right_r    = hub.right_button.is_released()

            # --- Buttons action --
            increment = self.params.get('increment')
            if self.left :
                if self.value - increment >= self.params.get('mini') :
                    self.value -= increment

            if self.right and not self.right_set: # wait time for validation
                self.timer.reset()
                self.right_set = True

            if self.right_set and self.right_r :
                if self.value + increment <= self.params.get('maxi'):
                    self.value += increment
                self.right_set = False

            # --- Matrix Light action --
            if self.right_set and self.timer.now() > 2 : #2 secondes
                self.edit = False
                MatrixLight.show_number(self.value)
                Speaker.beep()
                MatrixLight.off()
            else :
                if (self.timer.now() % 2 == 0 ) :
                    MatrixLight.show_number(self.value)
                else:
                    MatrixLight.show_pixels(self.params.get('matrix_code'))

    def getValue(self):
            return self.value

    def scale(self,value) :
        return min(self.params.get('maxi') , max(self.params.get('mini'), value))

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
LIBRARY_SLOT = const(15)


# -- LIBRARY MAIN ---
Speaker.beep3()
print("library loaded into robot slot:{}".format(LIBRARY_SLOT))
#hub.speaker.play_sound('charging')
