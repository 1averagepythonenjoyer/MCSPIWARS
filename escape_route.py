# Import necessary libraries
import time
import RPi.GPIO as GPIO
import practicemotors as motors
GPIO_TRIGGER = 18 #change
GPIO_ECHO = 24 #change

LM = 0
RM = 0

left_turn_time = 1 #adjust
right_turn_time = 1 #adjust

# Function to measure distance using HC-SR04 sensor
def measure_distance():
    # Code to measure distance using HC-SR04 sensor

    # set trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set trigger after 0.01 ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    startTime = time.time()
    arrivalTime = time.time()
 
    # store startTime
    while GPIO.input(GPIO_ECHO) == 0:
        startTime = time.time()
 
    # store arrivalTime
    while GPIO.input(GPIO_ECHO) == 1:
        arrivalTime = time.time()
 
    # Time difference between start and arrival
    timeElapsed = arrivalTime - startTime
    # multiply by the speed of sound (34300 cm/s)
    # and divide by 2, there and back again
    distanceToWall = (timeElapsed * 34300) / 2
 
    return distanceToWall

# Function to move the robot forward
def move_forward():
    # Code to move the robot forward
    RM = 100
    LM = 100
    motors.set(LM, RM)
# Function to turn the robot left
def turn_left():
    # Code to turn the robot left
    RM = 100
    LM = -100
    time.sleep(left_turn_time)
    motors.set(LM, RM)

# Function to turn the robot right
def turn_right():
    # Code to turn the robot right
    RM = -100
    LM = 100
    time.sleep(right_turn_time)
    motors.set(LM, RM)

# Turn 1/2/5
def RightTurn():
    while True:
        # Check the distance to the wall
        distance = measure_distance()
    
        # Print the current distance for demonstration
        print("Distance to wall:", distance, "cm")

        if distance < 30:
            turn_right()
            break  # Exit the loop since turning
        else:
            move_forward()

# Turn 3/4
def LeftTurn():
    while True:
        # Check the distance to the wall
        distance = measure_distance()
    
        # Print the current distance for demonstration
        print("Distance to wall:", distance, "cm")

        if distance < 30:
            turn_left()
            break  # Exit the loop since turning
        else:
            move_forward()

# Main function to run the maze program
def main():
    print("Starting maze program...")

    RightTurn()
    RightTurn()
    LeftTurn()
    LeftTurn()
    RightTurn()
    move_forward()

    print("End of maze program.")

# Run the main function
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
    finally:
        # Clean up GPIO
        GPIO.cleanup()
