#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#MIT Licence
#Copyright (c) 2015 Julien Poupeney

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

       

import serial,json,sys
from Util import lectureTrame,Json,serial_ports,DB_Record
from time import sleep, gmtime,localtime, strftime

DEVICE = '/dev/ttyACM0'
BAUD = 1200



print (strftime("%a, %d %b %Y %H:%M:%S: Starting\n", localtime()))
ports=serial_ports()

try:
	
	ser = serial.Serial(DEVICE,
BAUD,
bytesize=serial.SEVENBITS,
rtscts=True,
parity=serial.PARITY_ODD,
stopbits=serial.STOPBITS_ONE,
timeout=1)

except serial.SerialException:
	print "Erreur de ports:les ports disponible sont"
	for elt in ports:
		print(elt)
	sys.exit(0)

print ("Vidage buffer...")
sleep(1)
ser.flushInput()
while True:
    
   
    
   n=ser.inWaiting()
   if n!=0:
     trame=(lectureTrame(ser))
     print(trame)
     try:
      Json(trame)
     except AttributeError:
      print "Trame vide" 
    # DB_Record(trame)  

   
     
            
        

