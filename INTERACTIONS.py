#IMPORTS--------------------------------
from FONCTIONS import *

#FONCTIONS------------------------------------------

def qix_touch_player(qix_values, player_values):
    if qix_values['type'] == 'cloud':
        return cloud_touch_player(qix_values, player_values)


# def cloud_touch_player(qix_values, player_values):
#     #player_values
#     cx, cy, stix = player_values['cx'], player_values['cy'], player_values['stix']
#     stix_points = len(stix)
#     #qix_values
#     nbParticles
    
def cloud_touch_player(qix_values, player_values):
    #player_values
    cx, cy, radius = player_values['cx'], player_values['cy'], player_values['radius']
    stix = player_values['stix']
    stix_points = len(stix)
    #qix_values
    nbParticles = qix_values['nbParticles']
    particles = qix_values['particles']
    for particle in particles:
        for point in particle:
            #touche le joueur ( distance inférieur au rayon )
            if distance(point, (cx,cy)) <= radius:
                print('touche joueur')
                return True
            #touche le stix
            for i in range(stix_points-1):
                p1 = stix[i]
                p2 = stix[(i+1)%stix_points]
                if point_on_line(point, [p1,p2]):
                    print('touche stix')
                    return True
                
                
def player_touch_obstacle(player_values, obstacle):
    cx, cy, radius = player_values['cx'], player_values['cy'], player_values['radius']
    for point in obstacle:
        if distance((cx,cy), point) <= radius:
            return True
    return False