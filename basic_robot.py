#!/usr/bin/env python
#############################################################################################################                                                                  
# Basic example for controlling the GoPiGo using the Keyboard
# Controls:
#       w:      Move forward
#       a:      Turn left
#       d:      Turn right
#       s:      Move back
#       x:      Stop
#       t:      Increase speed
#       g:      Decrease speed
#       z:      Exit
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author        Date                    Comments  
# Karan                 27 June 14              Code cleanup                                                    
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
##############################################################################################################

from gopigo import *    #Has the basic functions for controlling the GoPiGo Robot
import sys      #Used for closing the running program
print "This is a basic example for the GoPiGo Robot control"
print "Press:\n\tw: Move GoPiGo Robot forward\n\ta: Turn GoPiGo Robot left\n\td: Turn GoPiGo Robot right\n\ts: Move GoPiGo Robot backward\n\tt: Increase speed\n\tg: Decrease speed\n\tx: Stop GoPiGo Robot\n\tz: Exit\n"
while True:
        print "Enter the Command:",
        a=raw_input()   # Fetch the input from the terminal
        if a=='w':
                fwd()   # Move forward
        elif a=='a':
                left()  # Turn left
        elif a=='o':
                
                for i in range(0,4):
                        fwd()
                        time.sleep(2)
                        stop()
                        time.sleep(0.1)
                        left()  # Turn left
                        time.sleep(0.5)
                        stop()
			time.sleep(0.1)	
                        
                stop()
        elif a=='8':
                motor1(1, 100)
                motor2(1, 50)
                time.sleep(2)
                motor1(1, 50)
                motor2(1, 100)
                time.sleep(2)
                
                stop()
                
        elif a=='d':
                right() # Turn Right
        elif a=='s':
                bwd()   # Move back
        elif a=='x':
                stop()  # Stop
        elif a=='t':
                increase_speed()        # Increase speed
        elif a=='g':
                decrease_speed()        # Decrease speed
        elif a=='z':
                print "Exiting"         # Exit
                stop()
                time.sleep(0.5)
                break
                #sys.exit()
        else:
                print "Wrong Command, Please Enter Again"
        time.sleep(.1)
