import RPi.GPIO as GPIO
from time import sleep
import subprocess

CAPACITOR_CHARGE_TIME = 3 # in seconds, should be sufficient to charge the capacitor - you could probably get away with as few as 1s

"""
@brief function to trigger the solenoid. Requires charging the capacitor prior to activation
@param pin (int): BCM pin that controls the solenoid
@param value (int): current output value on the pin
@param name (str): name of the output device
@return new_value (int): the same input value
"""
def solenoid_driver(pin, value, name):
    new_value = value
    GPIO.output(pin, 1)
    print("sleeping 3s to charge the capacitor")
    sleep(CAPACITOR_CHARGE_TIME)
    input(f"press any key to trigger the {name}!")
    GPIO.output(pin, 0)
    return new_value

"""
@brief function to toggle a led.
@param pin (int): BCM pin that controls the led
@param value (int): current output value on the pin
@param name (str): name of the output device
@return new_value (int): the new state of the output pin
"""
def led_driver(pin, value, name):
    led = char
    new_value = (value + 1) % 2
    GPIO.output(pin, new_value)
    print(f"setting {name} from {value} to {new_value}")
    return new_value

# gpio.board for Raspberry Pi 4 Model B is 11, GPIO port for Broadcom SOC (BCM) is 17
OUTPUT_BCM_PINS   = {  
                  "S": [17, 0, "Solenoid", solenoid_driver],
                  "G": [23, 0, "Green", led_driver],
                  "B": [22, 0, "Blue", led_driver],
                  "R": [25, 0, "Red", led_driver],
                  "Y": [24, 0, "Yellow", led_driver],
                  "W": [27, 0, "White", led_driver]
                 }
PIN_INDEX      = 0 # index of the list to find LED_BCM_PINS pin assignment
VALUE_INDEX    = 1 # index of the list to find LED_BCM_PINS output value
NAME_INDEX     = 2 # index of the name of the led
FUNC_INDEX     = 3 # index of the driver function for that output

"""
@brief function to drive all GPIO outputs to 0
@return None
"""
def zeroize_gpio():
    for _, state in OUTPUT_BCM_PINS.items():
        GPIO.output(state[PIN_INDEX], 0)

if __name__ == "__main__":
    # setup GPIO
    GPIO.setwarnings(False) # see README for why this is set to False
    GPIO.setmode(GPIO.BCM)
    for _, state in OUTPUT_BCM_PINS.items():
        GPIO.setup(state[PIN_INDEX], GPIO.OUT)
    zeroize_gpio()

    # enter endless user input loop
    try:
        while True:
            user_input = input("press S key to charge the capacitor, type R, G, B, Y, or W to toggle that LED\n> ")
            unique_user_input = list(set(user_input.upper()))
            for char in unique_user_input:
                if (char in OUTPUT_BCM_PINS.keys()):
                    OUTPUT_BCM_PINS[char][VALUE_INDEX] = OUTPUT_BCM_PINS[char][FUNC_INDEX](OUTPUT_BCM_PINS[char][PIN_INDEX],
                                                                                           OUTPUT_BCM_PINS[char][VALUE_INDEX],
                                                                                           OUTPUT_BCM_PINS[char][NAME_INDEX])
                else:
                    print(f"input {char} not recognized")
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected, exiting...")

    # drive all pins to low. See README for explanation of subprocess use.
    zeroize_gpio()
    GPIO.cleanup()
    for _, state in OUTPUT_BCM_PINS.items():
        subprocess.run(['raspi-gpio', 'set', f'{state[PIN_INDEX]}', 'op', 'dl'])
