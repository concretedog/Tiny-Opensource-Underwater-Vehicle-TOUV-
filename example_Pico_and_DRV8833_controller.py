'''
This script has been used with a StoRPer motor driver board but would equally work with a Pi Pico connected to 3 DRV8833 motor driver modules.

You can fine-tune each motor's speed with the SPEED_Mx variables.
You can toggle the motor direction by either swaping the GPIO pair or the PWM X/Y values

As written it's set up for one motor to run a little slower as in the first TOUV prototype we found the Z axis thruster was too powerful'

M1	GPIO 8, 9 Button attached to GPIO 26 and GND

M2	GPIO 10, 11 Button attached to GPIO 22 and GND

M3	GPIO 12, 13 Button attached to GPIO 21 and GND
'''

from machine import Pin, PWM
import time

# PWM frequency for all motors
FREQ = 1000

# Motor speed settings (0 to 65535)
SPEED_M1 = 60000 # right hand thruster from rear view on touv1
SPEED_M2 = 40000 # z axis touv1
SPEED_M3 = 60000  # left hand thruster from rear on touv1

# Motor pin setup
motors = [
    (PWM(Pin(8)), PWM(Pin(9))),   # Motor 1
    (PWM(Pin(11)), PWM(Pin(10))), # Motor 2
    (PWM(Pin(13)), PWM(Pin(12)))  # Motor 3
]

# Button pin setup with pull-ups
buttons = [
    Pin(26, Pin.IN, Pin.PULL_UP),  # Button 1
    Pin(22, Pin.IN, Pin.PULL_UP),  # Button 2
    Pin(21, Pin.IN, Pin.PULL_UP)   # Button 3
]

# Set PWM frequency
for pwm1, pwm2 in motors:
    pwm1.freq(FREQ)
    pwm2.freq(FREQ)

# Motor control functions
def stop_motor(pwm1, pwm2):
    pwm1.duty_u16(0)
    pwm2.duty_u16(0)

def run_motor(pwm1, pwm2, speed):
    pwm1.duty_u16(speed)
    pwm2.duty_u16(0)

# Stop all motors at start
for pwm1, pwm2 in motors:
    stop_motor(pwm1, pwm2)

print("Ready! Press buttons to run respective motors.")

while True:
    for i in range(3):
        pwm1, pwm2 = motors[i]
        button = buttons[i]
        
        if not button.value():  # Button is pressed (LOW)
            if i == 0:
                run_motor(pwm1, pwm2, SPEED_M1)
            elif i == 1:
                run_motor(pwm1, pwm2, SPEED_M2)
            elif i == 2:
                run_motor(pwm1, pwm2, SPEED_M3)
        else:
            stop_motor(pwm1, pwm2)
    
    time.sleep(0.05)  # Simple debounce delay
