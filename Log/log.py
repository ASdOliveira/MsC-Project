# Create a log file

import time

class log:
    def __init__(self,filename):
        self.filename = filename
        
    def logger (self, text):
        file = open(str(self.filename), "a")
        time_string = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
        file.write(time_string + "  "+ text + "\n")
        file.close()

