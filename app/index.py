import RPi.GPIO as GPIO
import threading
import time

from flask import Flask, render_template


class BlinkingThread(threading.Thread):
    should_blink: bool
    speed: float

    def __init__(self, should_blink, speed):
        threading.Thread.__init__(self)
        self.should_blink = should_blink
        self.speed = speed

    def run(self):
        while True:
            time.sleep(1)

            if self.should_blink:
              GPIO.output(18, True)
              time.sleep(self.speed)
              
              GPIO.output(18, False)
              time.sleep(self.speed)
            


app = Flask(__name__)

blinking_thread = BlinkingThread(True, 0.5)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

@app.route("/")
def success():
    return render_template('index.html')

@app.route("/blink")
def blink():
    blinking_thread.should_blink = True
    return success()

@app.route("/off")     
def off():
    blinking_thread.should_blink = False
    GPIO.output(18, False)
    return success()

@app.route("/on")     
def on():
    blinking_thread.should_blink = False
    GPIO.output(18, True)
    return success()


if __name__ == "__main__":
    blinking_thread.start()
    app.run()
    
