# RPI-python-CNC
un script en pyhton que unicamente lee G00 y G01 para crear una interpolacion lineal y transformarlo a pasos.<br />
no esta diseñado para funcionar bien, solo es una prueba para entender un poco mejor el funcionamineto basico de una cnc<br />
si lo que quiere es un firmware funcional, por favor visite este video: https://www.youtube.com/watch?v=fFp9MaTRyE4
***
### desventajas
* Solo funciona con cordenadas absolutas, incrementales no funcionaran.
* El escript no trasforma milimetros a pasos, por lo que tendra que acerlo usted al hora de crear el codigo g;<br />
G00 X 0.00 Y 0.00
G00 X 5.00 Y 0.00<br />
el eje x se movera 5 pasos, no 5 milimetros
* unicamente acepta movimiento lineal G00 y G01 y no cambia la velocidad entre estos
***
### Ejecucion:
entre en el script y especifique la ruta y nombre del archivo codigo G en la linea 3:
```python
nombre="/ruta/nombreArchivo.extencion"
```

Especifique cuantos pasos dara cada eje por una unidad en el gcode.(Linea 85)<br /> Si el avance en cada eje es el mismo por paso, dejelo en 1
<br/>Subir este valor no es conveniente ya que perdera resolucion, en cambio escale el modelo antes de generar el codigo g
```python
if x>xa:
  girar(1,8,1)  
if x<xa:
  girar(1,8,0)
if y>ya:
  girar(1,11,1)
if y<ya:
  girar(1,11,0)
```
especifique los valores del servomotor para arriba y abajo el la linea 109
```python
if z != za:
  if z >0 :
      servo.ChangeDutyCycle(8)#pocicion de dibujo(abajo) 
      time.sleep(.5)
      servo.ChangeDutyCycle(0)                    
  if z<0:
      servo.ChangeDutyCycle(10)#pocicion de brinco(arriba)
      time.sleep(.5)
      servo.ChangeDutyCycle(0)
  ```
pocisione la "herramienta" en la pocicion 0,0 y ejecute el script
### Conecciones:
Todos los pines estan numerados en modo BOARD<br />
* se utilizan dos pines para la direccion,PIN 10 y PIN 13
* dos para los pasos, PI 11 y PIN 8
* uno para habilitar o deshabilitar los motores, PIN 15
* y uno para controlar el servomotor, PIN 33
```python
GPIO.setup(8, GPIO.OUT) # pasos X
GPIO.setup(10, GPIO.OUT) #direccion X
GPIO.setup(13, GPIO.OUT) #direccion Y 
GPIO.setup(11, GPIO.OUT) #pasos  Y 
GPIO.setup(15, GPIO.OUT) #enable 
GPIO.setup(33, GPIO.OUT) #servo motor 
```
### Funciones:
la funcion girar recibe 3 parametros, el primero es la cantidad de pasos a dar, el segundo es el pin de pasos y el tercero es la direccion de giro
```python
girar(pasos,pin,direccion)
```
la funcion bresenham recibe 4 parametros, las cordenadas del primer punto, y las cordenadas del segundo, y regresa una lista con las cordenadas de los puntos necesarios para formar la linea,
```python
def bresenham(x0,y0,x1,y1):
```
### Screenshot
![Image text](https://www.united-internet.de/fileadmin/user_upload/Brands/Downloads/Logo_IONOS_by.jpg)
