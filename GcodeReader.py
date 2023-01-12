import RPi.GPIO as GPIO
import time
nombre="pythonRaspberrt.ngc"
archivo= open(nombre,mode="r")

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(8, GPIO.OUT) # pasos X
GPIO.setup(10, GPIO.OUT) #direccion X
GPIO.setup(13, GPIO.OUT) #direccion Y 
GPIO.setup(11, GPIO.OUT) #pasos  Y 
GPIO.setup(15, GPIO.OUT) #enable 
GPIO.setup(33, GPIO.OUT) #servo motor 

servo=GPIO.PWM(33,50)
servo.start(0)

x0=0
y0=0
x1=13
y1=6
GPIO.output(15, 0)

def bresenham(x0,y0,x1,y1):
    puntos=[]
    c=0
    dx=x1-x0
    dy=y1-y0
    if dy<0:
        dy=-dy
        stepy=-1
    else:
        stepy=1
    if dx<0:
        dx=-dx
        stepx=-1
    else:
        stepx=1
    x=x0
    y=y0
    puntos.append([x,y])
    if dx>dy:
        p=dy-dx
        incE=2*dy
        incNE=2*(dy-dx)
        while x!= x1:
            x=x+stepx
            if p<0:
                p=p+incE
            else:
                y=y+stepy
                p=p+incNE
            puntos.append([x,y])

    else:
        p=2*(dx-dy)
        incE=2*dx
        incNE=2*(dx-dy)
        while y!=y1:
            y=y+stepy
            if p<0:
                p=p+incE
            else:
                x=x+stepx
                p=p+incNE
            puntos.append([x,y])
    return(puntos)

def girar(N,P,D):
    GPIO.output(10,D)
    GPIO.output(13,D)
    for i in range(N):
        time.sleep(0.003)
        GPIO.output(P, 1)
        time.sleep(0.003)
        GPIO.output(P, 0)
        
def linea(x1,y1,x2,y2):
    xa=0
    ya=0
    for i in bresenham(x1,y1,x2,y2):
        x=i[0]
        y=i[1]
        if x>xa:
            girar(1,8,1)
        if x<xa:
            girar(1,8,0)
        if y>ya:
            girar(1,11,1)
        if y<ya:
            girar(1,11,0)
        xa=i[0]
        ya=i[1]
        
x=0
y=0
ya=0
xa=0
def G01(linea):
    c=0
    global x
    global y
    for i in linea:
        c+=1
        if i =="Z":
            z=float(linea[c+1:c+4])
            global za
            if z != za:
                if z >0 :
                    servo.ChangeDutyCycle(8)
                    time.sleep(.5)
                    servo.ChangeDutyCycle(0)                    
                if z<0:
                    servo.ChangeDutyCycle(10)
                    time.sleep(.5)
                    servo.ChangeDutyCycle(0)

            za=z
        if i =="Y":
            y=float(linea[c:c+5])
        
        if i =="X":
            x=float(linea[c:c+5])
        
    global ya,xa
    retX=int(x-xa)
    retY=int(y-ya)
    x=int(x)
    y=int(y)   
    return x,y

za=0
def G00(linea):
    c=0
    global x
    global y
    for i in linea:
        c+=1
        if i =="Z":
            z=float(linea[c+1:c+4])
            global za
            if z != za:
                if z >0 :
                    servo.ChangeDutyCycle(8)
                    time.sleep(.5)
                    servo.ChangeDutyCycle(0)
                if z<0:
                    servo.ChangeDutyCycle(10)
                    time.sleep(.5)
                    servo.ChangeDutyCycle(0)
            za=z
        if i =="Y":
            y=float(linea[c+1:c+5])
        if i =="X":
            x=float(linea[c+1:c+5])
    global ya,xa
    retX=x-xa
    retY=y-ya        
    x=int(x)
    y=int(y)
    return x,y

for line in archivo:
    l=line[0:3]
    if l == "G01":
        print(line)
        par=G01(line)
        x=par[0]
        y=par[1]
        linea(0,0,xa-x,ya-y)
    if l == "G00":
        print(line)
        par=G00(line)
        x=par[0]
        y=par[1]
        linea(0,0,xa-x,ya-y)
    xa=x
    ya=y
    
time.sleep(.1)
GPIO.output(15, 1)
GPIO.output(13, 0)
GPIO.output(11, 0)

GPIO.cleanup()
