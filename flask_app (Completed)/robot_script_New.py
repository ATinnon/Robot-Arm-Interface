import sys
import RPi.GPIO as GPIO
from time import sleep

wrist_step=50
pins=[7,22,18,16,15,13,12,11]
#msteps=[1,2,4,8]
msteps=[3,6,12,9]

GPIO.setmode(GPIO.BOARD)

def select_motor( motor ):
   GPIO.output(pins[0],motor&1)
   GPIO.output(pins[1],motor&2)
   GPIO.output(pins[2],motor&4)

def step(motor,steps,dir):
   select_motor(motor)
   if dir==1:
      x=0
      y=steps
      z=1
   elif dir==-1:
      x=steps
      y=0
      z=-1

   for c in range(x,y,z):
      GPIO.output(pins[3],~msteps[c%4]&1)
      GPIO.output(pins[4],~msteps[c%4]&2)
      GPIO.output(pins[5],~msteps[c%4]&4)
      GPIO.output(pins[6],~msteps[c%4]&8)
      GPIO.output(pins[7],True)
      GPIO.output(pins[7],False)
      sleep(0.01)
   stop(motor)

def stop(motor):
      GPIO.output(pins[3],True)
      GPIO.output(pins[4],True)
      GPIO.output(pins[5],True)
      GPIO.output(pins[6],True)
      GPIO.output(pins[7],True)
      GPIO.output(pins[7],False)
      sleep(0.01)
   

def wrist(steps,dir):
   for t in range(0,steps):
      if dir==1:               #turn
         step(1,wrist_step,1)
         step(3,wrist_step,1)
      elif dir==2:             #turn  
         step(1,wrist_step,-1)
         step(3,wrist_step,-1)
      elif dir==3:             #up
         step(1,wrist_step,-1)
         step(3,wrist_step,1)
      elif dir==4:             #down
         step(1,wrist_step,1)
         step(3,wrist_step,-1)

def initialize():
   for c in pins:
      print ("pin ",c) 
      GPIO.setup(c,GPIO.OUT)

print ("number of arguments", len(sys.argv)," arguments.")
print ("argument list: ",str(sys.argv))

initialize()
motor=int(sys.argv[1])
steps=int(sys.argv[2])
dir=int(sys.argv[3])

if motor<=7:
   step(motor,steps,dir)
if motor>7:
   dir=motor-7
   wrist(steps,dir)

sleep(0.5)

#wrist(20,1)
