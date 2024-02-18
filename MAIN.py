#IMPORTS---------------------------------------------------------------------------------------
from fltk import *
from QIX_ENEMY import *
from PLAYER import *
from INTERFACE import *
from INTERACTIONS import *
from OBSTACLES import *
from time import perf_counter
from random import randint, choice

#VARIABLES------------------------------------------------------------------------------------
largeurFenetre = 1200
hauteurFenetre = 700

directions = ['Up','Right','Down','Left']

blue = '#619ADF'

#FONCTIONS-------------------------------------------------------------------------------------


    
#FONCTIONS-------------------------------------------------------------------------------------
def main():
    cree_fenetre(largeurFenetre,hauteurFenetre)
    interface()
    
    #MENU
    options = menu()
    
    #initialisation
    contour = []
    contour.append([(300,100),(850,100),(850,650),(300,650)])
    
    #values
    zone = [(300,100),(850,100),(850,650),(300,650)] #zone non capturée
    draw_zone(zone)
    
    #quitter le jeu
    if options['leave'] is True:
        ferme_fenetre()
        return
    #création de joueur(s)
    all_players = []
    if options['two_players'] is True:
        all_players.append(generate_player(570, 650))
        all_players.append(generate_player(580, 650, blue, tag='player2'))
    else: #one player
        all_players.append(generate_player())
    #création des qix
    all_qix = qix_per_level(options['level'], zone)
    #création obstacles
    obstacles = generate_obstacles(options['obstacles'])
    for obstacle in obstacles:
        polygone(obstacle, 'white', 'black', 1, 'obstacle')
    #bonus
    bonus = dict()
    for i in range(options['bonus']):
        x, y = randint(300,650), randint(100,650)
        bonus['bonus'+str(i)] = generate_four_branches_star(x,y,15,5)
    draw_bonus(bonus)
    #collect
    collected = 0
    collection = dict()
    collection['radius'] = 6
    radius_check = all_players[0]['radius'] + collection['radius']
    for i in range(options['collect']):
        x, y = randint(300,650), randint(100,650)
        collection['coin'+str(i)] = (x,y)
    draw_coins(collection)
    if options['collect'] != 0:
        print(0)
        info_collect(collected, options['collect'])
    
    
    k = 0 #ralentir affichage
    
    #valeurs de capture
    quota = 75 #%
    captured = 0 #%
    score = 0 #points
    total = 550*550 #pixels
    
    start = True
    win = None #True -> Victoire, False -> Defaite
    pause = False
    
    info(all_players, captured, quota, score)
    
    mise_a_jour()
    
    #GAME-PLAY
    while start:
        
        if touche_pressee('p'):
            pass
        
        k += 1
        
        if k % 1000 == 0:
            
            for player_values in all_players:
            
                event = donne_ev()
                typeEvent = type_ev(event)
                
                #conditions d'arrêts
                if typeEvent == 'Quitte':
                    start = False
                elif player_values['hp'] == 0:
                    win = False
                    start = False
                elif captured >= quota and collected == options['collect']:
                    start = False
                    win = True
                
                #player_status(player_values)
                
                direction = get_direction()
                cx, cy = player_values['cx'], player_values['cy']
                
                #qix
                if k % 7 == 0:
                    for qix_values in all_qix:
                        qx, qy = qix_values['cx'], qix_values['cy']
                        move = qix_values['move']
                        if move[1] == 0:
                            move = [ choice(directions), randint(1,4) ]
                        qix_values = generate_qix(zone, move, qx, qy)
                        efface('qix')
                        draw_qix(qix_values)
                
                
                #intéraction qix-joueur
                if not player_values['onContour']:
                    if not player_values['invincible']:
                        for qix_values in all_qix:
                            if qix_touch_player(qix_values, player_values):
                                handle_hp_loss(player_values)
                                #mettre à jour info
                                info(all_players, captured, quota, score)
                                player_values['onContour'] = True
                
                #gestion OBSTACLES
                        for obs in obstacles:
                            if player_touch_obstacle(player_values, obs):
                                handle_hp_loss(player_values)
                                #mettre à jour info
                                info(all_players, captured, quota, score)
                                player_values['onContour'] = True
                        
                        
                
                #gestion BONUS
                if player_values['invincible'] == True:
                    inv_counter2 = perf_counter()
                    if inv_counter2 - inv_counter1 >= 3:
                        player_values['invincible'] = False
                to_remove = []
                for tag, value in bonus.items():
                    if tag != 'radius' and point_in_polygon((cx,cy), value):
                        efface(tag)
                        player_values['invincible'] = True
                        to_remove.append(tag)
                        inv_counter1 = perf_counter()
                for tag in to_remove:
                    bonus.pop(tag)
                
                
                # sur le contour
                if player_values['onContour']:
                    #sortir du contour, tracer stix
                    if touche_pressee('Return') and direction != None:
                        #peut sortir des contours
                        if move_out_zone(player_values, zone, direction):
                            player_values['stix'].append((player_values['cx'],player_values['cy']))
                            update_player_values(player_values,direction)
                            player_values['stix'].append((player_values['cx'],player_values['cy']))
                            draw_stix(player_values)
                            player_values['onContour'] = False
                    #se déplacer sur contour
                    else:
                        if direction != None and move_on_contour(player_values,contour,direction):
                            update_player_values(player_values,direction)
                # hors du contour:
                else:
                    #re-rentre dans le contour
                    if point_on_polygon((player_values['cx'],player_values['cy']),zone):
                        player_values['stix'].append((player_values['cx'],player_values['cy']))
                        player_values['stix'] = simplify_line(simplify_line(player_values['stix']))
                        #crée un nouveau polygone et met à jour la zone
                        zone, new_polygon = handle_capture(player_values, qix_values, zone)
                        #print(zone, '\n\n', new_polygon)
                        contour.append(new_polygon)
                        capture_polygon(player_values, new_polygon)
                        #plus
                        area = area_of_polygon(new_polygon)
                        score += area//2
                        captured += round(area_of_polygon(new_polygon) * 100 / total)
                        efface('stix'); player_values['stix'] = []
                        efface('zone'); draw_zone(zone)
                        info(all_players, captured, quota, score)
                        player_values['onContour'] = True
                        
                        #gestion COLLECT
                        to_remove = []
                        for tag, coin in collection.items():
                            if tag != 'radius' and point_in_polygon(coin, new_polygon):
                                efface(tag)
                                to_remove.append(tag)
                                collected += 1
                        for tag in to_remove:
                            collection.pop(tag)
                        if len(to_remove) != 0 and options['collect'] != 0:
                            efface('info_collect')
                            info_collect(collected, options['collect'])
                        
                        
                    #trace le stix
                    else:
                        if direction != None:
                            update_player_values(player_values,direction)
                            #if (player_values['cx'], player_values['cy']) not in player_values['stix']:
                            player_values['stix'].append((player_values['cx'], player_values['cy']))
                            draw_stix(player_values)

                
                #efface('obstacles'); draw_obstacles(obstacles_values)
                efface('player'); draw_player(player_values)
                
                mise_a_jour()
        
    game_over(win, score)
    mise_a_jour()
    
#MAIN------------------------------------------------------------------------------------------
if __name__ == '__main__' :
    main()
    attend_fermeture()
    
    