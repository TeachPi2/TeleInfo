#fichier Util.py

#MIT licence
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




from time import sleep, gmtime,localtime, strftime
import json,serial,glob,sys,MySQLdb as mdb



def lectureTrame(ser):
    """reconstitution de la trame EDF"""
    msg=ser.read()
    print (hex(ord(msg)))
    if msg==chr(0x02) :
      print("\n"+strftime("%Y-%m-%d %H:%M:%S: Starting ", localtime())+"detection trame")
      trame=""
      concact=""
      while trame!=chr(0x03):
       
       concact+=trame
       trame=ser.read()
       
       
      return(concact[0:-1])



def Json (trame):
 
  """Ecriture dans le JSON pour teleinfo.html"""
  sub=trame.split(chr(0x0a))
  dict={}
  
  for i in range(1,len(sub)):
    item=sub[i].split(' ')
    dict[item[0]]=item[1]
  with open("/var/www/realTime.json","w") as file:
   json.dump(dict,file,indent=4)
  file.close()


def DB_Record(trame):
  ts=strftime("%Y-%m-%d %H:%M:%S", localtime())
  con=mdb.connect('localhost','Pi','juju','EDF')
  cur=con.cursor()
  cur.execute("CREATE TABLE IF NOT EXISTS EDF (id serial PRIMARY KEY, etiquette VARCHAR(25), data VARCHAR(25), ts timestamp);")
  sub=trame.split(chr(0x0a))
  for i in range(1,len(sub)):
    item=sub[i].split(' ')
    cur.execute("INSERT INTO EDF (etiquette , data , ts) VALUES (%s,%s,%s)",(item[0],item[1],ts))
    
  
  con.commit()
  cur.close()
  con.close()





def serial_ports():
    """Lists serial ports

    :raises EnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of available serial ports
    """
    if sys.platform.startswith('win'):
        ports = ['COM' + str(i + 1) for i in range(256)]

    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this is to exclude your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')

    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')

    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result



 

	

  
