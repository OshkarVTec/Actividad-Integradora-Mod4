import RPi.GPIO as GPIO
from time import sleep

btn1 = 25
btn2 = 26
btn3 = 27
btn4 = 28
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(btn1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def button1_callback(channel):
    print("Button was pushed!")

def button2_callback(channel):
    print("Button was pushed!")

def button3_callback(channel):
    print("Button was pushed!")

def button4_callback(channel):
    print("Button was pushed!")
    
def main():
    GPIO.add_event_detect(btn1,GPIO.FALLING,callback=button1_callback) #Button pressed event
    GPIO.add_event_detect(btn2,GPIO.FALLING,callback=button2_callback) #Button pressed event
    GPIO.add_event_detect(btn3,GPIO.FALLING,callback=button3_callback) #Button pressed event
    GPIO.add_event_detect(btn4,GPIO.FALLING,callback=button4_callback) #Button pressed event