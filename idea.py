import random
import math

# funcion para calcular la distancia "euclidiana" entre dos puntos p1 y p2:
# Es la raiz cuadrada de la suma de los cuadrados de las coordenadas (Pitagoras)
# p1[0] es x1 p2[0] es x2, p1[1] es y1 y p2[1] es y2.
def distancia(p1,p2):
    dist = math.sqrt( (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 )
    return dist

# Para seleccionar el rango de los puntos random (son los limites x,y del cuadrado que representa un poligono basico)
min=0
max=666
# generare 20 puntos aleatorios se supone que tu ya los tienes  ...
max_puntos = 20
puntos=[]
for k in range(0,max_puntos):
    puntos.append ([ random.randint(min,max), random.randint(min,max) ])

# Solo para mostrar los puntos disponibles:
i = 0
for x,y in puntos:
    print('coordenadas:',x,y, ' = ', puntos[i])
    i = i + 1

numero_puntos_requeridos=5
distancia_minima_entre_puntos = 111
max_numero_iteraciones = 10

puntos_me_sirve=[]
for i in range(0,max_numero_iteraciones):
      print('selecione el punto:',i,'de la lista dentro de TODOS puntos disponibles, coordenadas:',puntos[i])
      
      # Al ppio el unico punto que sirve es el primero
      puntos_me_sirve.append( puntos[i] )
      
      # Obtiene el numero_puntos_requeridos y despues revisa si le "sirven"
      puntos_sel = []
      for j in range(0,numero_puntos_requeridos):
          puntos_sel.append( puntos[ j ] )
          
      k = 0
      while k < (numero_puntos_requeridos-1 ):
        for m in range(k+1,numero_puntos_requeridos):
            #print( puntos_sel[k], puntos_sel[m])
            d = distancia( puntos_sel[k], puntos_sel[m])
            #print("distancia entre ", puntos_sel[k], puntos_sel[m], ' es:', d, sep='')
            if d > distancia_minima_entre_puntos:
                #print('si me sirve el punto ', puntos[m])
                puntos_me_sirve.append(puntos[k])
                k = k + 1
            else:
                print(puntos[m],' no me sirve, buscare otro ...')

      print('ya encontre ',numero_puntos_requeridos,' puntos utiles. cercanos a ', puntos[i])
      print('los puntos son:')
      for p in puntos_me_sirve:
          print(p, end='\t')


      


