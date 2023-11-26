import RPi.GPIO as GPIO
import time

trig=3
echo=2
servoPin=6
SERVO_MAX_DUTY = 12
SERVO_MIN_DUTY = 3
BUTTON=5
LED=7

GPIO.setmode(GPIO.BCM)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(servoPin, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)

servo=GPIO.PWM(servoPin, 50)
servo.start(0)

def servo_control(degree, delay) :
    if degree > 180 :
       degree = 180

    duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY - SERVO_MIN_DUTY)/180.0)
    servo.ChangeDutyCycle(duty)
    time.sleep(delay)

try : 
  while True:
    GPIO.output(trig, False)
    time.sleep(0.5)
    GPIO.output(trig, True)
    GPIO.output(trig, False)
    time.sleep(0.5)
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
    
    while GPIO.input(echo) == 0 :
        pulse_start = time.time( )
    while GPIO.input(echo) == 1 :
        pulse_end = time.time( )
    
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration*(340*100)/2
    distance = round(distance, 2)
    
    print("distance : ", distance, "cm", end="       ")
    print()

    if GPIO.input(BUTTON) == True :
        print("open plz")
        for i in range(21, -1,-10) : # open
            servo_control(i, 0.1)
        time.sleep(0.5) # time delay
        for i in range(0, 151, 10) :
            servo_range(i, 0.1) # close

     
     
    else :
        if distance <= 20 :
            print("open")
            for i in range (21,-1,-10) : # open
                servo_control(i, 0.1)
            time.sleep(0.5) # time delay
            for i in range(0, 151, 10) : # close
                servo_control(i, 0.1)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()


# have to revise 'range'