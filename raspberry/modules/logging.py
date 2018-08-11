import time

logpad = open("log.txt", "w") # Open a document

def log(msg):
    print(str(time.strftime("%H:%M:%S", time.localtime(time.time()))) + ": " + msg, file = logpad)

def timestamp():
    return time.strftime("%H:%M:%S", time.localtime(time.time()))
