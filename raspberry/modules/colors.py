# Colored print functions

def error(msg):
    print("\033[91m" + msg + "\033[0m") # red

def warn(msg):
    print("\033[93m" + msg + "\033[0m") # yellow

def success(msg):
    print("\033[94m" + msg + "\033[0m") # blue

def wait(msg):
    print("\033[95m" + msg + "\033[0m") # purple

def info(msg):
    print("\033[92m" + msg + "\033[0m") # green

def bold(msg):
    print("\033[1m" + msg + "\033[0m") # bold

def underline(msg):
    print("\033[4m" + msg + "\033[0m") # underline
