#!/usr/bin/env python
# coding: utf-8
#
# Determinacion de puntos para toma de muestras
# python 3.7
#
# Parametros de entrada:
#    nombre del archivo formato csv
#    numero minimo de puntos a seleccionar o ... porcentaje minimo de puntos a seleccionar
#    distancia minima entre puntos <--- en mts
#
#   C:\Users\Julio\Dropbox\current\ATY\sel_points>python sel_point.py -m 141 -i ../data/Puntos_Point.csv -p 20
#   C:\dir\sel_points>python sel_point.py -m 141 -i ../data/Puntos_Point.csv -p 20
#

import random
import math

import sys, getopt, os

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

import pandas as pd

# Print helpful messages, set to False in Production
debug = False
plot  = False

def regulariza(t):
    nc  = t.replace('(','')
    nc2 = nc.replace(')','')
    return nc2 
    

def read_csv(filename):
    if debug: print('reading '+filename)
    df = pd.read_csv(filename)
#    name = 'A3-c'
#name = 'A4-b'
# Filtra solo las filas con Name = ...
#    df = df[(df['Name'] == name )]
    total_points =  len(df)

    if debug: df.head(3)

# Transform wkt_geom to X, Y coord.
    df[['sinuso','X','Y']] = df['wkt_geom'].str.split(" ",expand=True, )
    df.drop(columns=['sinuso'],inplace=True)
    df['X']=df['X'].apply(regulariza)
    df['Y']=df['Y'].apply(regulariza)
    if debug: df.head(3)
 
    # To numeric
    df['X'] = pd.to_numeric(df['X'], errors='raise', downcast='float')
    df['Y'] = pd.to_numeric(df['Y'], errors='raise', downcast='float')

    X = df['X'].values
    Y = df['Y'].values

    # Minimos
    xmin = int(df['X'].min())
    ymin = int(df['Y'].min())

    # Maximos
    xmax = int(df['X'].max())
    ymax = int(df['Y'].max())

    if debug: 
        print('Min. coord.:',df['X'].min(), df['Y'].min(),' | Integer:',xmin,ymin)
        print('Max. coord.:',df['X'].max(), df['Y'].max(),' | Integer:',xmax,ymax)

    # ### Puntos recibidos

    if plot:
        plt.title('Grid Points (loaded)')
        plt.scatter(X,Y, marker='.', s = 5);

    # universe_points se obtiene del archivo csv
    universe_points = []
    for i in range(0,len(X)):
        x = X[i] 
        y = Y[i] 
        universe_points.append([x,y])

    if debug: universe_points[0:5]
    
    return X, Y, total_points, universe_points
 
    
def distance(p,q):
    '''
    Euclidian distance
    '''
    return math.sqrt( (p[0]-q[0])*(p[0]-q[0]) + (p[1]-q[1])*(p[1]-q[1]) )  


def get_point(universe_points):
    '''
    Get a new point from the points array
    '''
    i = random.randint(0, len(universe_points)-1)
    return universe_points[i]


def get_first_point(universe_points):
    '''
    Get the first point from the points array
    The nearest point to the centroid of all points
    '''
    totx = 0
    toty = 0
    #xmin = 9999999999999999
    #xmax = -999999999999999
    #ymin = 9999999999999999
    #ymax = -999999999999999
    first_point = []
    n = len(universe_points)
    for i in range(0,n):
        x = universe_points[i][0]
        y = universe_points[i][1]
        #if x < xmin: xmin = x
        #if x > xmax: xmax = x
        #if y < ymin: ymin = y
        #if y > ymax: ymax = y
        totx = totx + x
        toty = toty + y
                
    #centroid = [ xmin + (xmax-xmin)/2 ,ymin + (ymax-ymin)/2 ]
    centroid = [ totx/n, toty/n ]

    if debug: print('*** Centroid:',centroid)
    
    d = 9999999999999999
    for i in range(0,len(universe_points)):
        if distance(universe_points[i], centroid) < d:
            d = distance(universe_points[i], centroid)
            first_point = universe_points[i]
    
    return first_point


def verify(point, selected_points, min_distance_allowed):
    '''
    Verify that the new point is useful (based on a minimall distance)
    '''
    useful = False
    '''
    Compare the point with the rest of points selected
    '''
    i = 0
    while i < len(selected_points) :
        if debug: print('comparing ',point, selected_points[i], sep='')
        dist =  distance(point, selected_points[i])
        if  dist <= min_distance_allowed:
            if debug: print('not ok',int(dist), ' < ',  min_distance_allowed)
            useful = False
            return useful
        else:
            if debug: print('ok',int(dist), ' > ',  min_distance_allowed)
            useful = True
        i += 1
    return useful


# Ejecucion de la seleccion de puntos
def select_first_point(universe_points, selected_points,  X, Y):
    '''
    First point added to selected_points
    '''
    p = get_first_point(universe_points)
    selected_points.append( p )
    
    if debug: print('first point',selected_points)
    if plot:
        plt.title('Centroid')
        plt.scatter(X,Y, c='b', marker='.', label='grid', s=10)
        plt.scatter(selected_points[0][0], selected_points[0][1], c='r', marker='X', label='centroid', s=40)
        plt.legend(loc='lower center')
        plt.show()
        
    return selected_points


def exec_select_points(universe_points, selected_points, min_necesary_points, min_distance_allowed):
    k = 0
    max_iter = 1000
    while ( len(selected_points) < min_necesary_points and k < max_iter ):
        p = get_point(universe_points)
        if debug: print('checking if new point:',p, 'is useful ...')
        res = False
        res = verify(p, selected_points, min_distance_allowed)
        if res:
            if debug: print('yes, is useful')
            selected_points.append( p )
        else:
            if debug: print('no, not useful')
        k += 1
        if debug: print('number of selected points',len(selected_points))
        #print('points selected', selected_points)


    print('\n*** end of selection.\t',k, 'iterations')
    print('*** number of selected points:',len(selected_points))
    return selected_points
    
def chart_selected_points(selected_points, X, Y):
# ### Grafico con puntos seleccionados
    if plot:
        XX=[]
        YY=[]
        for p in selected_points:
            XX.append(p[0]) 
            YY.append(p[1]) 
        plt.title('Selected Points')
        plt.scatter(XX,YY, c='r', marker='+' );

    if plot:
        plt.title('Selected Points in Grid')
        plt.scatter(X,Y, c='b', marker='.', label='grid', s=10)
        plt.scatter(XX, YY, c='r', marker='s', label='selected', s=10)
        plt.legend(loc='lower left')
        plt.show() 


# ### Graba el csv con los puntos generados
def save_csv(filename, selected_points):
    data_dir = '../data/'
    x = filename.split('/')
    name = x[-1].replace('.csv','')
    XX=[]
    YY=[]
    for p in selected_points:
        XX.append(p[0]) 
        YY.append(p[1]) 
    
    index = []
    for i in range(0,len(XX)):
        index.append(i)

    data = {
        'x': XX,
        'y': YY
    }
    dfsel = pd.DataFrame(data=data, columns=['x','y'], index=index)
    filename_selected = data_dir + 'sel_'+name+'.csv'
    print ('*** saving in ',filename_selected )
    dfsel.to_csv(filename_selected, index_label='line')


# ---
def main(argv):
    filename = ''
    min_distance_allowed = 0
    prop = 0

    try:
        opts, args = getopt.getopt(argv,"hi:p:d:m:",["filename=","percent=","min_diatance"])
    except getopt.GetoptError:
        print ('sel_point.py -d <min_distance_in_meters> -i <filename_csv> -n <percent_points>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('sel_point.py -m <min_distance_in_meters> -i <filename_csv> -p <percent_points>')
            sys.exit()
        elif opt in ("-i", "--filename"):
            filename = arg
            # Validar que filename existe y es legibe ...
            if os.path.exists(filename):
                pass
            else:
                print ('Error: can\'t read the file: '+filename)
                print ('sel_point.py -m <min_distance_in_meters> -i <filename_csv> -p <percent_points>')
                sys.exit()
        elif opt in ("-p", "--percent"):
            prop = int(arg)
            if prop < 0 or prop > 100:
                print ('Error: percent must be between 1 and 99')
                print ('sel_point.py -m <min_distance_in_meters> -i <filename_csv> -p <percent_points>')
                sys.exit()
        elif opt in ("-m", "--min_distance"):
            min_distance_allowed = int(arg)
            if min_distance_allowed < 1 or min_distance_allowed > 100000:
                print ('Error: min_distance must be positive in meters')
                print ('sel_point.py -m <min_distance_in_meters> -i <filename_csv> -p <percent_points>')
                sys.exit()
                
    print ('CSV Filename         :', filename )
    print ('Percent of points [%]:', prop )
    print ('Min. Distance [m]    :', min_distance_allowed )
    
    universe_points = []
    selected_points = []
    
    # Lee el csv    
    X, Y, total_points, universe_points = read_csv(filename)
    
    min_necesary_points = int((total_points)*prop/100)
    print('\n')
    print('Total Points in csv       :',total_points)
    print('Number of points to select:', min_necesary_points)
   
    selected_points = select_first_point(universe_points, selected_points,  X, Y)
    selected_points = exec_select_points(universe_points, selected_points, min_necesary_points, min_distance_allowed)
    
    if debug: print('selected points:', selected_points)
        
    save_csv(filename, selected_points)
    
    if plot: chart_selected_points(selected_points, X, Y)

if __name__ == "__main__":
   main(sys.argv[1:])


