import cv2
import numpy as np
import tflite_runtime.interpreter as tf
import RPi.GPIO as GPIO
import time


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

interpreter_model = None

# Put camera reolution and servo to camera ratio I think it is 15 degrees gun = 90 degrees servo

camera_resolution = [,]
servo_to_camera_ratio = 90 / 15 #Ratio of gun and servo. Can be changed depending on design

prev_positions = [] # Please do not change this must be empty list

def load_model(model_path):
    interpreter_model = tf.Interpreter(model_path=model_path)
    interpreter_model.allocate_tensors()
    return interpreter_model

def preprocess_image(image):
    tensor_input = image.astype(np.float32)
    input_tensor = np.expand_dims(tensor_input, axis=0)
    return input_tensor

def run_inference(interpreter_model, image):
    input_data = preprocess_image(image)
    interpreter_model.set_tensor(interpreter_model.get_input_details()[0]['index'], input_data)
    interpreter_model.invoke()
    return interpreter_model.get_tensor(interpreter_model.get_output_details()[0]['index'])

def calculate_motor_output(target_position_x, target_position_y, camera_resolution):
    speed = 1.0
    center_x = camera_resolution[0] // 2

    if target_position_x > center_x:  # Program assumes the robot is facing right
        left_motor_speed = speed
        right_motor_speed = speed  # Move forward
    elif target_position_x < center_x:
        left_motor_speed = -speed  # Move backward
        right_motor_speed = -speed
    else:
        left_motor_speed = 0  # Stay still
        right_motor_speed = 0

    return left_motor_speed, right_motor_speed

def move_servo(servo_pin, target_position_y):
    GPIO.setup(servo_pin, GPIO.OUT)
    servo = GPIO.PWM(servo_pin, 100)  # I don't know if 100 is good. customizes, I guess?
    servo.start(0)

    servo_movement = target_position_y / servo_to_camera_ratio

    duty_cycle = 7.5 + (0.05 * servo_movement) #This line check servo registartion and documentry see what value PWM it wants
    servo.ChangeDutyCycle(duty_cycle)
    time.sleep(0.1)

def move_motor(left_motor_speed, right_motor_speed, left_motor_pin_1, right_motor_pin_1):
    GPIO.setup(left_motor_pin_1, GPIO.OUT)
    GPIO.setup(left_motor_pin_2, GPIO.OUT)
    GPIO.setup(right_motor_pin_1, GPIO.OUT)
    GPIO.setup(right_motor_pin_2, GPIO.OUT)

    GPIO.output(left_motor_pin_1, GPIO.HIGH)
    GPIO.output(left_motor_pin_2, GPIO.LOW)
    GPIO.output(right_motor_pin_1, GPIO.HIGH)
    GPIO.output(right_motor_pin_2, GPIO.LOW)

    left_pwm = GPIO.PWM(left_motor_pin_1, 100)
    left_pwm.start(left_motor_speed * 100)

    right_pwm = GPIO.PWM(right_motor_pin_1, 100)
    right_pwm.start(right_motor_speed * 100)

def operation_kill_undead(interpreter_model, servo_pin):
    cap = cv2.VideoCapture(0)  # Enter in camera index
    
    interpreter_model = load_model(model_path)

    try:
        while True:
            ret, frame = cap.read()
            
            output_data = run_inference(interpreter_model, frame)

            if output_data:
                x, y, w, h = output_data[0]
                target_position_x = x + w // 2
                target_position_y = y + h // 2

                offset = 2
                target_position_y += offset

                left_motor_speed, right_motor_speed = calculate_motor_output(target_position_x, target_position_y, camera_resolution)

                move_motor(left_motor_speed, right_motor_speed, left_motor_pin_1, right_motor_pin_1)
                move_servo(servo_pin, target_position_y)

    finally:
        cap.release()

operation_kill_undead(interpreter_model, servo_pin)
