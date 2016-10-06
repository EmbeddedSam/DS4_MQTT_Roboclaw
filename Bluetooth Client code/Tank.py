#Runs ds4drv and sense hat for init 
#Author <joseph.adams-3@student.manchester.ac.uk>
#Data 13/07/16

from sense_hat import SenseHat
import os
import time

sense = SenseHat()

os.system("ds4drv &")

time.sleep(1)

sense.show_message("Pair Now")

os.system("python /home/pi/ds4.py")