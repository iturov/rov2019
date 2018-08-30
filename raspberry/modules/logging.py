import time

logpad = open("log.txt", "a") # Open a document

def datetime():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))

def timestamp():
    return time.time()

def log(msg):
    print(str(datetime()) + ": " + msg, file = logpad)
