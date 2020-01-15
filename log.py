# Create a log file

import time

def Action (text):
    file = open("Log.txt", "a")
    time_string = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
    file.write(time_string + "  "+ text + "\n")
    file.close()
