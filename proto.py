#!/usr/bin/env python
# coding: utf-8

# # Determinacion de puntos para toma de muestras

# In[79]:


# python 3.7
#
# Parametros de entrada:
#    nombre del archivo formato csv
#    numero minimo de puntos a seleccionar o ... porcentaje minimo de puntos a seleccionar
#    distancia minima entre puntos
#


# In[104]:


import random
import math


# In[137]:


debug = True


# In[141]:


# universe_points se obtiene del archivo csv
universe_points = []
min_necesary_points = 15


# In[128]:


# Crea un arreglo de points_number puntos  
# Esto debe ser obtenido desde el archivo csv
total_points_number = 100
for x in range(total_points_number):
  universe_points.append( [random.randint(1,100),random.randint(1,100)] ) 


# In[129]:


def distance(p,q):
    '''
    Euclidian distance
    '''
    return math.sqrt( (p[0]-q[0])*(p[0]-q[0]) + (p[1]-q[1])*(p[1]-q[1]) )  


# In[130]:


def get_point():
    '''
    Get a new point from the points array
    '''
    i = random.randint(0,min_necesary_points-1)
    return universe_points[i]


# In[139]:


def verify(point, selected_points):
    '''
    Verify that the new point is useful (based on a minimall distance)
    '''
    min_distance_allowed = 7
    useful = False
    '''
    Compare the point with the rest of points selected
    '''
    i = 0
    while i < len(selected_points) :
        if debug: print('comparing ',point, selected_points[i], sep='')
        dist =  distance(point, selected_points[i])
        if  dist <= min_distance_allowed and dist > 0:
            if debug: print('not ok',int(dist), ' < ',  min_distance_allowed)
            useful = False
            return useful
        else:
            if debug: print('ok',int(dist), ' > ',  min_distance_allowed)
            useful = True
        i += 1
    return useful


# # Ejecucion de la seleccion de puntos

# In[140]:


k = 0
max_iter = 20
selected_points=[]
'''
First point added to selected_points
'''
p = get_point()
selected_points.append( p )
if debug: print('first point',selected_points)
while ( len(selected_points) < min_necesary_points and k < max_iter ):
    p = get_point()
    if debug: print('checking if new point:',p, 'is useful ...')
    res = False
    res = verify(p, selected_points)
    if res :
        if debug: print('yes, is useful')
        selected_points.append( p )
    else:
        if debug: print('no, not useful')
    k += 1
    if debug: print('number of selected points',len(selected_points))
    #print('points selected', selected_points)
    

print('\n*** end of selection.')
print('*** number of selected points:',len(selected_points) )


# In[135]:


print('selected points:')
selected_points


# In[ ]:




