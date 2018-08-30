# Colored print functions

from logging import *

def error(msg):
    print("\033[91m" + "[ERROR]\t" + msg + "\033[0m") # red
    log("[ERROR]\t" + msg)

def warn(msg):
    print("\033[93m" + "[WARN]\t" + msg + "\033[0m") # yellow
    log("[WARN]\t" + msg)

def success(msg):
    print("\033[94m" + "[SUCCESS]\t" + msg + "\033[0m") # blue
    log("[SUCCESS]\t" + msg)

def wait(msg):
    print("\033[95m" + "[WAIT]\t" + msg + "\033[0m") # purple
    log("[WAIT]\t" + msg)

def info(msg):
    print("\033[92m" + "[INFO]\t" +  msg + "\033[0m") # green
    log("[INFO]\t" + msg)

def bold(msg):
    return "\033[1m" + msg + "\033[0m" # bold
    log(msg)

def underline(msg):
    return "\033[4m" + msg + "\033[0m" # underline
    log(msg)

def reset_terminal():
    print("\x1b[2J")
