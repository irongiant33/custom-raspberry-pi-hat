import RPi.GPIO as GPIO
from time import sleep
import subprocess

OUTPUT_PIN = 17 # gpio.board for Raspberry Pi 4 Model B is 11, GPIO port for Broadcom SOC is 17
LED_PINS = {"G": [23, 0, "Green"], "B": [22, 0, "Blue"], "R": [25, 0, "Red"], "Y": [24, 0, "Yellow"], "W": [27, 0, "White"]}
ON_TIME = 3
OFF_TIME = 3
PIN_INDEX = 0 # index of the list to find LED_PINS pin assignment
VALUE_INDEX = 1 # index of the list to find LED_PINS output value
NAME_INDEX = 2 # index of the name of the led

def zeroize_gpio():
    GPIO.output(OUTPUT_PIN, 0)
    for _, state in LED_PINS.items():
        GPIO.output(state[PIN_INDEX], 0)

if __name__ == "__main__":
    # setup GPIO
    GPIO.setwarnings(False) # see README for why this is set to False
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(OUTPUT_PIN, GPIO.OUT)
    for _, state in LED_PINS.items():
        GPIO.setup(state[PIN_INDEX], GPIO.OUT)

    zeroize_gpio()

    try:
        while True:
            user_input = input("press space key to charge the capacitor, type R, G, B, Y, or W to toggle that LED\n> ")
            unique_user_input = list(set(user_input.upper()))
            for char in unique_user_input:
                if (char == " "):
                    GPIO.output(OUTPUT_PIN, 1)
                    print("sleeping 3s to charge the capacitor")
                    sleep(ON_TIME)
                    input("press any key to trigger the solenoid!")
                    GPIO.output(OUTPUT_PIN, 0)
                elif (char in LED_PINS.keys()):
                    led = char
                    LED_PINS[led][VALUE_INDEX] = (LED_PINS[led][VALUE_INDEX] + 1) % 2
                    GPIO.output(LED_PINS[led][PIN_INDEX], LED_PINS[led][VALUE_INDEX])
                    print(f"setting {LED_PINS[led][NAME_INDEX]} to {LED_PINS[led][VALUE_INDEX]}")
                else:
                    print(f"input {char} not recognized")
    except KeyboardInterrupt:
        zeroize_gpio()
        print()

    # drive all pins to low. See README for explanation of subprocess use.
    zeroize_gpio()
    GPIO.cleanup()
    subprocess.run(['raspi-gpio', 'set', f'{OUTPUT_PIN}', 'op', 'dl'])
    for _, state in LED_PINS.items():
        subprocess.run(['raspi-gpio', 'set', f'{state[PIN_INDEX]}', 'op', 'dl'])
