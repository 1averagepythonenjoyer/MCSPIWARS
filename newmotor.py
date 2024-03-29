from time import sleep
import RPi.GPIO as GPIO # remember to install
from approxeng.input.selectbinder import ControllerResource # remember to install

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

PWMaenable = 13 #what a lucky number 
GPIO.setup(PWMaenable, GPIO.OUT)
PWMa= GPIO.PWM(PWMaenable, 100)
PWMa.start(0)

PWMbenable = 15
GPIO.setup(PWMbenable, GPIO.OUT)
PWMb= GPIO.PWM(PWMbenable, 100)
PWMb.start(0)

input1 = 19
GPIO.setup(input1, GPIO.OUT)
GPIO.output(input1, GPIO.HIGH)

input2 = 21
GPIO.setup(input2, GPIO.OUT)
GPIO.output(input2, GPIO.LOW)

input3 = 16
GPIO.setup(input3, GPIO.OUT)
GPIO.output(input3, GPIO.HIGH)

input4 = 18
GPIO.setup(input4, GPIO.OUT)
GPIO.output(input4, GPIO.LOW)

def set_speed(power_left, power_right):
    if y >= 0:
        #forward
        GPIO.output(input1, GPIO.HIGH)
        GPIO.output(input2, GPIO.LOW)
        GPIO.output(input3, GPIO.HIGH)
        GPIO.output(input4, GPIO.LOW)
        r_motor= map_range(power_right,0,100,0,100) # add gpio out analog with duty cycle 0-100
        l_motor= map_range(power_left,0,100,0,80)
    elif y < 0:
        GPIO.output(input1, GPIO.LOW)
        GPIO.output(input2, GPIO.HIGH)
        GPIO.output(input3, GPIO.HIGH)
        GPIO.output(input4, GPIO.LOW)
        r_motor= map_range(power_right,0,100,0,100)
        l_motor= map_range(power_left, 0, 100, 0, 100)
    print('Left: {}, Right: {}'.format(power_left, power_right))
    print('Left duty percent: {}, Right duty percent: {}'.format(l_motor, r_motor))
    PWMa.ChangeDutyCycle(l_motor) 
    PWMb.ChangeDutyCycle(r_motor)
    sleep(0.1)

def mix(yaw, throttle, max_power=100):
    left = (0.9 * throttle) - yaw
    right = throttle + yaw
    scale = float(max_power) / max(1, abs(left), abs(right))
    return int(left * scale), int(right * scale)

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
    try:
        with ControllerResource() as joystick:
            while joystick.connected:
                x, y = joystick['l']
                power_left, power_right = mix(yaw=x, throttle=y)
                print("x =", x)
                print("y =", y)
                set_speed(power_left, power_right)
    except IOError:
        print('Unable to find any joysticks')
        sleep(1.0)


