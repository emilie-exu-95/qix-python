#IMPORTS----------------------------------------------------------------------
from fltk import *
import FONCTIONS
from random import randint

#FONCTIONS-------------------------------------------------------------------
def generate_obstacles(nbObstacles=5):
    obstacles_values = []
    for i in range(nbObstacles):
        x = randint(300,850)
        y = randint(100,650)
        obstacles_values.append(FONCTIONS.generate_four_branches_star(x,y,8,17))
    return obstacles_values


def extract_obstacles(file):
    '''Chaque ligne du fichier est un polygone'''
    pass
    
    

def draw_obstacles(obstacles_values):
    for v in obstacles_values.values():
        polygone(v, 'grey', 'black', 1, 'obstacles')
    
    
    
