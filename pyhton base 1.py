#from mindstorms import MSHub, Motor, MotorPair, ColorSensor, DistanceSensor, App
#from mindstorms.control import wait_for_seconds, wait_until, Timer
#from mindstorms.operator import greater_than, greater_than_or_equal_to, less_than, less_than_or_equal_to, equal_to, not_equal_to
#import math

# Crée tes objets ici.

#movement_moteurs = MotorPair('A','B') 

# Écris ton programme ici.
#hub.speaker.beep()

# movement_moteurs.move(10,'cm',steering = 0)
#distance_sensor = distanceSensor('D')

#movement_moteurs.start()
#distance_sensor.wait_for_distance_closer_than('5','cm')
#movement_moteurs.stop()

# Importer la classe MSHub.
#from mindstorms import MSHub
#from mindstorms.control import wait_for_seconds
# Initialiser le Hub.
#hub = MSHub()
# Montrer un visage souriant pendant cinq secondes.

#
#hub.light_matrix.show_image('HAPPY')
#wait_for_seconds(5)
#hub.light_matrix.off()
#from mindstorms import App

#app = App()
from mindstorms import MSHub
from mindstorms.control import wait_for_seconds
from mindstorms import MotorPair
import math
import time
from micropython import const
import machine
import pkg_resources


class Gyro() :
    POINTS = [(2,0),(1,0),(0,0),(0,1),(0,2),(0,3),(0,4),(1,4),(2,4),(3,4),(4,4),(4,3),(4,2),(4,1),(4,0),(3,0),(2,0)]
    def __init__(self) :
        self.hub = MSHub()
        self.lacet = None
        self.idx = -1
    def reset(self):
        hub.motion_sensor.reset_yaw_angle()
        self.idx = -1 
    def position(self):
        self.lacet = hub.motion_sensor.get_yaw_angle()
        return self.lacet
    def plotPixel(self):
        angle = self.position()
        if angle < 0 :
            angle = 180 + (angle + 180)
        new_idx = int(angle/23)
        if self.idx != new_idx :
            if self.idx != -1:
                self.hub.light_matrix.set_pixel(Gyro.POINTS[self.idx][0],Gyro.POINTS[self.idx][1], 0)
            self.idx = new_idx
            self.hub.light_matrix.set_pixel(Gyro.POINTS[self.idx][0],Gyro.POINTS[self.idx][1], 100)

class Moteurs() :

    def __init__(self) :
        self.motors = MotorPair('A', 'B')  
        self.motors.set_default_speed(50)
        self.gyro = Gyro()
        # Les roues MINDSTORMS ont un diamètre de 5,6 cm. Multiplier par « π » pour obtenir la circonférence.
        #self.motors.set_motor_rotation(5,6 * math.pi, 'cm')

    def start(self,vitG,vitD) : 
        self.motors.start_tank(vitG, vitD)  # vitX -100 , +100 

    def avance(self,volant,vitesse = None) :  #   -100 <- 0 -> 100 
        if vitesse == None: 
            vitesse = self.vitesse() 
        self.motors.start(steering=volant,speed=vitesse)# vitX -100 , +100

    def stop (self):
        self.motors.stop()

    def set_vitesse(self,vitesse) :  #° ->  100 
        self.motors.set_default_speed(vitesse)

    def vitesse(self) :#° ->100
        return self.motors.get_default_speed()

    def demiTour_droit(self,vitesse=None) :
        
        if vitesse == None :
            vitesse = self.vitesse()
        self.motors.move_tank(262, "degrees", vitesse * -1 , vitesse )
        self.gyro.plotPixel()

    # Gyro- 1 T ==> 525 
    def demiTour_gauche(self, vitesse= None) :
        if vitesse == None :
            vitesse = self.vitesse()
        self.motors.move_tank(262, "degrees", vitesse, vitesse * -1 )
        self.gyro.plotPixel()

    def avance_degrés(self,degrés) :
        self.motors.move_tank(degrés, "degrees", 25, 25)

    def recul_degrés(self,degrés) :
        self.motors.move_tank(degrés * -1 , "degrees", 25, 25)


# Changer la séquence des ports des moteurs pour changer le sens du moteur
#motors = MotorPair('B', 'A')


hub = MSHub()
gyro = Gyro()
moteurs = Moteurs()

hub.speaker.beep()


#pixels = '99999:88888:77777:66666:55555'
#hub.light_matrix.show(pixels)
#wait_for_seconds(2)

#moteurs.start(25, -25)
#moteurs.avance_degrés(360)
#moteurs.recul_degrés(360)

gyro.reset()
gyro.plotPixel()

while True:
    #gyro.plotPixel()
    #moteurs.avance_degrés(360)
    #wait_for_seconds(1)
    #moteurs.recul_degrés(360)
    #moteurs.demiTour_droit(20)
    wait_for_seconds(1)
    #moteurs.avance_degrés(360)
    #moteurs.demiTour_gauche(20)
    wait_for_seconds(1)
    
    #moteurs.demiTour_gauche(20)
    #wait_for_seconds(2)

    #moteurs.avance(0,25)
    #wait_for_seconds(5)
    #moteurs.stop()

