# Colored print functions
from logging import *

def error(msg):
    print("\033[91m" + msg + "\033[0m") # red
    log(msg)

def warn(msg):
    print("\033[93m" + msg + "\033[0m") # yellow
    log(msg)

def success(msg):
    print("\033[94m" + msg + "\033[0m") # blue
    log(msg)

def wait(msg):
    print("\033[95m" + msg + "\033[0m") # purple
    log(msg)

def info(msg):
    print("\033[92m" + msg + "\033[0m") # green
    log(msg)

def bold(msg):
    print("\033[1m" + msg + "\033[0m") # bold
    log(msg)

def underline(msg):
    print("\033[4m" + msg + "\033[0m") # underline
    log(msg)
