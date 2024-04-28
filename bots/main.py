from sys import argv
import os.path
from threading import Timer
from random import randint, uniform
from requests import post as rq_post
import configparser

config = configparser.ConfigParser()
path = os.path.dirname(os.path.abspath(argv[0]))
config.read(path + r'\bot.ini')

TOKEN = argv[1]
MIN_INTERVAL = int(config['TIMER']['MIN_INTERVAL'])
MAX_INTERVAL = int(config['TIMER']['MAX_INTERVAL'])
INTERVAL = randint(MIN_INTERVAL, MAX_INTERVAL)
MIN_VALUE = float(config['TELEMETRY']['MIN_VALUE'])
MAX_VALUE = float(config['TELEMETRY']['MAX_VALUE'])
URL = config["WEB"]["URL"]

TIMER = -1

def post():
    value = round(uniform(MIN_VALUE, MAX_VALUE), 2)
    try:
        respose = rq_post(URL, params={'token' : TOKEN}, json={'telemetry' : value})
        print(f"POST /?token={TOKEN} [telemetry: {value}] responce code: {respose.status_code}")
    except Exception as e:
        print(e)
        print("\nAn error occurred while sending POST. The program has been stopped")
        global TIMER
        TIMER.cancel()

def repeater(interval, function):
    global TIMER
    TIMER = Timer(interval, repeater, [interval, function])
    TIMER.start()
    function()

def main():
    repeater(INTERVAL, post)

if __name__  == '__main__':
    main()