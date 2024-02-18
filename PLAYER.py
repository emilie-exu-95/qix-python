#IMPORTS---------------------------------------------------------------------------------------
from fltk import *
from random import randint, choice, random
import time
from FONCTIONS import *
#from time import perf_counter
from MAIN import *

#VARIABLES-------------------------------------------------------------------------------------
directions = ['Up','Right','Down','Left']

colors = { 'red': '#C7A3A3',
           'blue': '#D5DFFF',
           'green': '#D5F0D9',
           'orange': '#FFE8D5' }

font = 'Dubai'
blue = '#619ADF'


#FONCTIONS--------------------------------------------------------------------------------

def handle_player():
    pass


#FONCTIONS-------------------------------------------------------------------------------------
def draw_stix(player_values):
    stix = player_values['stix']
    color = player_values['color']
    efface('stix')
    if player_values['invincible']:
        color = 'yellow'
    for i in range(len(stix)-1):
        p1 = stix[i]
        p2 = stix[i+1]
        ligne(p1[0], p1[1], p2[0], p2[1], couleur=color, epaisseur=2, tag='stix')
    

def capture_polygon(player_values, polygon):
    color = player_values['color']
    polygone(polygon,color,colors[color],3)


def handle_capture(player_values, qix_values, zone):
    print()
    stix = player_values['stix']
    qx, qy = qix_values['cx'], qix_values['cy']
    one, two = split_polygon(zone,stix)
    if point_in_polygon((qx,qy),one): #if qix dans polygone -> polygone = zone
        #print('ZONE : ', one)
        #print('CAPTURE : ', two)
        return one, two
    #print('ZONE : ', two)
    #print('CAPTURE : ', one)
    return two, one
    

def handle_hp_loss(player_values):
    player_values['hp'] -= 1
    #revient sur le contour, premier point du stix
    player_values['cx'] = player_values['stix'][0][0]
    player_values['cy'] = player_values['stix'][0][1]
    #vider et effacer le stix
    player_values['stix'] = []
    efface('stix')


def copy_player(new_cx, new_cy, step):
    player_values_copy = {
        'cx' : new_cx,
        'cy' : new_cy,
        'step' : step
        }
    return player_values_copy


def move_on_polygon(point, polygon, direction):
    '''Renvoie True si le joueur se trouve sur le polygone et peut s'y déplacer dans la direction donnée
    False sinon'''
    nbPoints = len(polygon)
    for i in range(nbPoints):
        if i == nbPoints-1 : #si c'est le dernier point, l'autre point de la ligne est le premier
            line = [polygon[i],polygon[0]]
        else: #le point consécutif pour créer une ligne
            p1 = polygon[i]
            p2 = polygon[(i+1)%nbPoints]
            line = [p1,p2]
        if move_on_line(point,line,direction): #peut se déplacer sur ligne
            return True
    return False


def move_on_line(point, line, direction):
    '''Renvoie True si le joueur peut se déplacer sur la ligne dans la direction donnée'''
    cx, cy = point[0], point[1]
    close, far = min(line[0],line[1]), max(line[0],line[1])
    close_x, close_y, far_x, far_y = close[0], close[1], far[0], far[1]
    #ligne verticale
    if close_x == far_x == cx:
        if (direction == 'Up') and (close_y < cy <= far_y):
            return True
        elif (direction == 'Down') and (close_y <= cy < far_y):
            return True
    #ligne horizontale
    elif close_y == far_y == cy:
        if (direction == 'Right') and (close_x <= cx < far_x):
            return True
        elif (direction == 'Left') and (close_x < cx <= far_x):
            return True
    return False
    
        
def update_player_values(player_values, direction):
    '''Met à jour les valeurs du joueur'''
    if direction == 'Up':
        player_values['cy'] -= player_values['step']
    elif direction == 'Right':
        player_values['cx'] += player_values['step']
    if direction == 'Down':
        player_values['cy'] += player_values['step']
    if direction == 'Left':
        player_values['cx'] -= player_values['step']

        
def generate_player(cx=575, cy=650, color='red', radius=7, step=5, hp=3, tag='player'):
    '''
    step = [ 5, 5.5, 6.25, 6.875, 11 ]
    '''
    player_values = dict()
    player_values['hp'] = hp
    player_values['cx'] = cx
    player_values['cy'] = cy
    player_values['radius'] = radius
    player_values['color'] = color
    player_values['step'] = step
    player_values['stix'] = []
    player_values['tag'] = tag
    player_values['onContour'] = True
    player_values['invincible'] = False
    return player_values

    
def draw_player(player_values):
    '''Dessine le joueur sous forme de cercle'''
    cx, cy, radius, color = player_values['cx'], player_values['cy'], player_values['radius'], player_values['color']
    tag = player_values['tag']
    if player_values['invincible']:
        color = 'yellow'
    cercle(cx, cy, radius, color, '', 3, tag)
    

def move_on_contour(player_values, contour, direction):
    '''Renvoie True et la direction si le joueur peut se déplacer sur le contour
    False sinon'''
    cx, cy = player_values['cx'], player_values['cy']
    if direction in ['Up','Right','Down','Left']:
        for polygon in contour:
            if move_on_polygon((cx,cy),polygon,direction):
                return True
    return False

def move_in_zone(player_values, zone, direction):
    '''Renvoie True si la direction permet de revenir sur le contour'''
    cx, cy, step = player_values['cx'], player_values['cy'], player_values['step']
    player_copy = copy_player(cx, cy, step)
    update_player_values(player_copy, direction)
    return move_on_contour(player_copy, [zone], direction)
    

def move_out_zone(player_values, zone, direction):
    '''Renvoie True si le joueur peut sortir des contours grâce à la direction'''
    #création d'une copie pour réaliser des tests
    cx, cy, step = player_values['cx'], player_values['cy'], player_values['step']
    player_values_copy = copy_player(cx,cy,step)
    update_player_values(player_values_copy, direction)
    point_copy = (player_values_copy['cx'], player_values_copy['cy'])
    return point_in_polygon(point_copy, zone)
    

def can_draw_stix(player_values, direction):
    '''Renvoie True si le joueur peut créer le stix'''
    cx, cy, step = player_values['cx'], player_values['cy'], player_values['step']
    stix = player_values['stix']
    player_copy = copy_player(cx, cy, step)
    update_player_values(player_copy, direction)
    cx_copy, cy_copy = player_copy['cx'], player_copy['cy']
    nbPoints = len(stix)
    for i in range(nbPoints-1):
        p1 = stix[i]
        p2 = stix[i+1]
        if point_on_line((cx_copy,cy_copy), [p1,p2]):
            return False
    return True


#MAIN------------------------------------------------------------------------------------------
if __name__ == '__main__' :
    pass
