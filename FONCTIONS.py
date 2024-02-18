#IMPORTS--------------------------------------------------------------------------------------------
from fltk import *
import math


#FONCTIONS, pre-made-------------------------------------------------------------------------------
def point_in_polygon(point, polygon):
    x, y = point
    nbPoints = len(polygon)
    inside = False

    # Prendre un point très éloigné pour le ray casting (ici, à droite du polygone)
    extreme_point = (max(p[0] for p in polygon) + 1, y)

    # Compter les intersections du rayon avec les côtés du polygone
    intersection_count = 0
    for i in range(nbPoints):
        p1 = polygon[i]
        p2 = polygon[(i + 1) % nbPoints]

        # Vérifier si le rayon intersecte le côté
        if do_lines_intersect((x, y), extreme_point, p1, p2):
            intersection_count += 1

    return intersection_count % 2 == 1


def do_lines_intersect(p1, p2, p3, p4):
    # Vérifie si les segments de ligne (p1, p2) et (p3, p4) s'intersectent
    # Utilise une formule déterminant
    def determinant(x1, y1, x2, y2):
        return x1 * y2 - x2 * y1

    det1 = determinant(p2[0] - p1[0], p2[1] - p1[1], p3[0] - p1[0], p3[1] - p1[1])
    det2 = determinant(p2[0] - p1[0], p2[1] - p1[1], p4[0] - p1[0], p4[1] - p1[1])
    det3 = determinant(p4[0] - p3[0], p4[1] - p3[1], p1[0] - p3[0], p1[1] - p3[1])
    det4 = determinant(p4[0] - p3[0], p4[1] - p3[1], p2[0] - p3[0], p2[1] - p3[1])

    return det1 * det2 < 0 and det3 * det4 < 0




#FONCTIONS------------------------------------------------------------------------------------------
def pause_logo(cx, cy, size, color, tag='pause'):
    efface('pause')
    square(cx, cy, size, color, '', 3, 'pause')



def generate_four_branches_star(cx, cy, size, size2):
    star = [(cx,cy-size),(cx+size2,cy-size2),
            (cx+size,cy), (cx+size2,cy+size2),
            (cx,cy+size), (cx-size2,cy+size2),
            (cx-size,cy), (cx-size2,cy-size2)]
    return star


def get_direction():
    '''Renvoie la direction selon la touche pressee'''
    direction = None
    if touche_pressee('Up'):
        direction = 'Up'
    elif touche_pressee('Right'):
        direction = 'Right'
    elif touche_pressee('Down'):
        direction = 'Down'
    elif touche_pressee('Left'):
        direction = 'Left'
    return direction


def distance(point1, point2):
    ax, ay = point1
    bx, by = point2
    return math.sqrt((bx-ax)**2 + (by-ay)**2)


def point_in_polygon0(point, polygon):
    '''Renvoie True si le point et dans le polygone, False sinon
    Ne prends pas en compte les cas particuliers'''
    x, y = point
    nbPoints = len(polygon)
    intersection = 0
    for i in range(nbPoints):
        p1 = polygon[i]
        p2 = polygon[(i+1)%nbPoints]
        if p1[0] == p2[0]: #ligne verticale
            if min(p1[1],p2[1]) < y < max(p1[1],p2[1]): #traverse la ligne verticale par une ligne horizontales passant par point
                intersection += 1
    return intersection % 2 == 1


def point_on_polygon(point, polygon):
    x, y = point
    nbPoints = len(polygon)
    for i in range(nbPoints):
        p1 = polygon[i]
        p2 = polygon[(i+1)%nbPoints]
        if point_on_line(point, (p1,p2)):
            return True
    return False


def point_on_line(point, line):
    x,y = point
    p1, p2 = line
    #ligne verticale
    if p1[0] == p2[0] == x:
        if min(p1[1],p2[1]) < y < max(p1[1],p2[1]):
            return True
    #ligne horizontale
    elif p1[1] == p2[1] == y:
        if min(p1[0],p2[0]) < x < max(p1[0],p2[0]):
            return True
    return False
    

def area_of_polygon(polygon):
    '''Renvoie l'aire du polygone'''
    aire = 0
    nbPoints = len(polygon)
    for i in range(nbPoints):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i+1)%nbPoints]
        aire += (x1*y2)-(x2*y1)
    return int(abs(aire)/2)


def split_polygon(polygon, separator):
    '''Renvoie deux polygones séparés par un separator'''
    first, last = separator[0], separator[-1]
    nbPoints = len(polygon)
    #chercher l'index sur le polygon
    for i in range(nbPoints):
        p1 = polygon[i]
        p2 = polygon[(i+1)%nbPoints]
        if point_on_line(last, [p1,p2]):
            stock_i = i
            break   
    #sens -> droite
    polygon_one = []
    polygon_one.extend(separator)
    for j in range(1,nbPoints):
        p1 = polygon[(stock_i+j)%nbPoints]
        p2 = polygon[(stock_i+j+1)%nbPoints]
        polygon_one.append(p1)
        if point_on_line(first, [p1,p2]):
            break
    #sens <- gauche
    polygon_two = []
    polygon_two.extend(separator)
    for k in range(nbPoints):
        p1 = polygon[(stock_i-k)%nbPoints]
        p2 = polygon[(stock_i-1-k)%nbPoints]
        polygon_two.append(p1)
        if point_on_line(first, [p1,p2]):
            break
    return simplify_polygon(polygon_one), simplify_polygon(polygon_two)


def move_on_polygon(point, polygon, direction=None):
    '''Renvoie True si le joueur se trouve sur le polygone et peut s'y déplacer dans la direction donnée
    False sinon'''
    nbPoints = len(polygon)
    for point_index in range(nbPoints):
        p1 = polygon[i]
        p2 = polygon[(i+1)%nbPoints]
        line = (p1,p2)
        if move_on_line(point,line,direction): #peut se déplacer sur ligne
            return True
    return False


def square(x,y,length,couleur='black',remplissage='black',epaisseur=1,tag=''):
    '''Dessine un carré'''
    rectangle(x,y,x+length,y+length,couleur,remplissage,epaisseur,tag)


def simplify_line(line):
    new_line = []
    new_line.append(line[0])
    nbPoints = len(line)
    for i in range(nbPoints-2):
        p1, p2, p3 = line[i], line[i+1], line[i+2]
        #les deux lignes n'ont pas la même direction ( verticale/horizontale )
        if not ( p1[0] == p2[0] == p3[0] or p1[1] == p2[1] == p3[1] ):
            new_line.append(p2)
    new_line.append(line[-1])
    return new_line
    
    
def simplify_polygon(polygon):
    '''Simplifie le polygon. nbPoints = nbAretes'''
    new_polygon = []
    new_polygon.append(polygon[0]) #ajout du tout premier point
    nbPoints = len(polygon)
    for i in range(nbPoints):
        p1, p2, p3 = polygon[i], polygon[(i+1)%nbPoints], polygon[(i+2)%nbPoints]
        #les deux lignes n'ont pas la même direction ( verticale/horizontale )
        if not ( p1[0] == p2[0] == p3[0] or p1[1] == p2[1] == p3[1] ):
            new_polygon.append(p2)
    new_polygon.pop() #dernier point == premier point
    return new_polygon
     
        
if __name__ == '__main__':
    polygon = [(1,1),(2,1),(3,1),(3,2),(2,2),(2,3),(1,3),(1,2)]
    #print(simplify_polygon(polygon))
    