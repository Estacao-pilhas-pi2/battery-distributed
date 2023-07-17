import RPi.GPIO as gpio
import signal
import os

PIN = int(os.getenv("PIN_IR", "16"))

def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(PIN, gpio.IN)
    gpio.add_event_detect(PIN, gpio.RISING, callback=on_ir_change)

def on_ir_change(x):
    print(x, PIN, gpio.input(PIN))

if __name__ == "__main__":
    init()
    while True:
        signal.pause()
