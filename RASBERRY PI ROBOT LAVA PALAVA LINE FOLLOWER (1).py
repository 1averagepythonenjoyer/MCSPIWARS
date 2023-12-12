
import RPi.GPIO as GPIO
import time


Left_sensor_pin =  29    #modify for use!
middle_sensor_pin = 31#We can just glue three jumper wires together.
right_sensor_pin = 33
right_motor_input_1 = 21  #same as the ones for the remote control: this makes it less confusing. It also allows us to manually override the robot 
right_motor_input_2 = 22 # if something doesnt work
left_motor_input_3 = 23
left_motor_input_4 = 24


GPIO.setmode(GPIO.BOARD)
GPIO.setup(left_sensor_pin, GPIO.IN)
GPIO.setup(middle_sensor_pin, GPIO.IN)
GPIO.setup(right_sensor_pin, GPIO.IN)
GPIO.setup(left_motor_pin, GPIO.OUT)
GPIO.setup(right_motor_pin, GPIO.OUT)

left_motor = GPIO.PWM(left_motor_pin, 100)
right_motor = GPIO.PWM(right_motor_pin, 100)
left_motor.start(0)
right_motor.start(0)

def forward(left_speed, right_speed):
    left_motor.ChangeDutyCycle(left_speed)
    right_motor.ChangeDutyCycle(right_speed)
    GPIO.output(left_motor_pin, GPIO.HIGH)
    GPIO.output(right_motor_pin, GPIO.HIGH)
def left():
    forward(70,100) #ADJUST!!!
def right():
    forwards(100,70) #ADJUST!!!
def left_a_bit():
    forward(90,100) #ADJUST!!!
def right_a_bit():
    forward(100,90) #ADJUST!!!
def Lava_Palava():
    while True:
        left_sensor = GPIO.input(left_sensor_pin)
        middle_sensor = GPIO.input(middle_sensor_pin)
        right_sensor = GPIO.input(right_sensor_pin)
        
        if left_sensor and middle_sensor == 1:
            left_a_bit()
        elif right_sensor and middle_sensor == 1:
            right_a_bit()
        else:
            if middle_sensor == 0:
                if left_sensor == 1:
                    left()
                elif right_sensor == 1:
                    right()
            
            else:
                forward(100,100)
            time.sleep(0.1) #CUSTOMISE BUT I THINK 0.1 SECONDS PER CHECK IS GOOD ENOUGH
Lava_Palava()