#IMPORTS---------------------------------------------------------------------------------------
from fltk import cree_fenetre, rectangle, efface, mise_a_jour
from random import randint, choice
from PLAYER import *
from FONCTIONS import *
from time import sleep


#VARIABLES--------------------------------------------------------------------------------------
zone = [(300,100),(850,100),(850,650),(300,650)]

move_step = { 'Up': -5, 'Right': 5, 'Down': 5, 'Left': -5 }

#FONCTIONS-------------------------------------------------------------------------------------
def generate_particles(cx, cy, nbParticles, radius):
    '''
    Génère des valeurs pour chaque particule sous la forme d'une liste
    et la retourne
    '''
    particles = []
    for _ in range(nbParticles):
        ax = randint(cx-radius,cx+radius)
        ay = randint(cy-radius,cy+radius)
        bx = ax + randint(15,35)
        by = ay + randint(15,35)
        particles.append([(ax,ay), (bx,ay), (bx,by), (ax,by)])
    return particles


def generate_qix(zone,
                move = ['Up', 3],
                cx = 500,
                cy = 400,
                nbParticles = 4,
                speed = 1,
                color = '#8756E1'):
    '''
    Renvoie un dictionnaire des valeurs du qix
    nbParticles et speed sont indicatifs du niveau de jeu
    '''
    qix_values = dict()
    cxV, cyV = 0, 0
    
    if move[0] in ['Left', 'Right']:
        cxV += move_step[move[0]]*speed
    else:
        cyV += move_step[move[0]]*speed
        
    if point_in_polygon((cx+cxV,cy+cyV),zone):
        cx += cxV; cy += cyV
    move[1] -= 1    
    qix_values['cx'], qix_values['cy'] = cx, cy
    qix_values['radius'], qix_values['speed'] = nbParticles*10, speed
    qix_values['nbParticles'] = nbParticles
    qix_values['particles'] = generate_particles(qix_values['cx'],qix_values['cy'],nbParticles,qix_values['radius'])
    qix_values['color'] = color
    qix_values['type'] = 'cloud'
    qix_values['move'] = move
    return qix_values


def draw_qix(qix_values):
    '''
    Dessine une instance du qix
    '''
    particles = qix_values['particles']
    color = qix_values['color']
    for particle in particles:
        polygone(particle, color, '', 3, 'qix')
        

def qix_per_level(level, zone):
    level_speed = { 2 : 2, 3 : 3, 4 : 3 } 
    all_qix = []
    if level == 1:
        all_qix.append(generate_qix(zone))
    else:
        if level in [2, 3, 4]:
            all_qix.append(generate_qix(zone, speed=level_speed[level]))
            all_qix.append(generate_qix(zone, speed=level_speed[level]))
    if level == 5:
        for _ in range(3):
            all_qix.append(generate_qix(zone, speed=3))
    return all_qix
            
    
#MAIN------------------------------------------------------------------------------------------
if __name__ == '__main__' :
    lst = []
    largeurFenetre = 1000
    hauteurFenetre = 700
    cree_fenetre(largeurFenetre,hauteurFenetre)
    rectangle(0,0,largeurFenetre,hauteurFenetre,'black','black')
    draw_zone(zone)
    #rectangle(0,0,200,200,couleur='red')
    qix_values = generate_qix()
    mise_a_jour()
    while True :
        sleep(0.09)
        cx = qix_values['cx']
        cy = qix_values['cy']
        qix_values = generate_qix(cx,cy)
        draw_qix(qix_values)
        mise_a_jour()
        efface('qix')


    
