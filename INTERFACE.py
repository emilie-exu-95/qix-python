#IMPORTS---------------------------------------------------------------------------------------------
from fltk import *
from FONCTIONS import *

#VARIABLES-------------------------------------------------------------------------------------------
directions = ['Up','Right','Down','Left']

colors = { 'red': '#C7A3A3',
           'blue': '#D5DFFF',
           'green': '#D5F0D9',
           'orange': '#FFE8D5' }

font = 'Dubai'
white = '#AAAAAA'; gris = '#2B2B2B'; blue = '#619ADF'

#FONCTIONS-------------------------------------------------------------------------------------------
def draw_bonus(bonus):
    for tag, value in bonus.items():
        polygone(value, 'yellow', 'yellow', 1, tag)


def game_over(win, score):
    font = 'Broadway'
    if win:
        texte(372, 298, 'VICTOIRE !', 'black', police=font, taille=51)
        texte(375, 300, 'VICTOIRE !', 'white', police=font, taille=50)
    else:
        texte(397, 298, 'Défaite...', 'white', police=font, taille=51)
        texte(400, 300, 'Défaite...', 'white', police=font, taille=50)


def interface(niveau=1,bgcolor='black',color='white',largeurFenetre=1200,hauteurFenetre=700):
    '''Dessine l'interface du jeu'''
    rectangle(0,0,largeurFenetre,hauteurFenetre,remplissage=bgcolor) #fond noir
    square(300,100,550,color) #aire de jeu
    texte(300,0,'QIX',color,police='Broadway',taille=70)


def info(all_players, captured, quota, score):
    #gestion vie
    efface('info')
    k = 0
    for player_values in all_players:
        hp, color = player_values['hp'], player_values['color']
        for _ in range(hp):
            cercle(870,180+k,7,color,'',3,'info')
            k += 30
    #gestion capture
    rectangle(45,108,270,200,'white','',tag='info')
    texte(50,110,'Capture','white',police=font,taille=20)
    texte(150,140,str(captured)+' / 100  %','white',police=font,taille=15,tag='info')
    texte(150,165,str(quota)+'  %','green',police=font,taille=15,tag='info')


def player_status(player_values):
    efface('player_status')
    onContour = player_values['onContour']
    color = player_values['color']
    fill = ''
    if not onContour:
        fill = colors[color]
    cercle(500,53,10,couleur=color,remplissage=fill,epaisseur=3,tag='player_status')
    

def draw_zone(zone):
    '''Efface et dessine la zone de déplacement du qix'''
    efface('zone')
    polygone(zone, 'green', epaisseur=3, tag='zone')
    
    
def menu():
    start = False
    all_tags = ['menu', 'p2', 'o', 'c', 's', '-', '+', 'l', 'b']
    #options
    options = dict()
    options['two_players'] = False
    options['obstacles'] = 0
    options['internal_sparx'] = False
    options['collect'] = 0
    options['bonus'] = 0 #invincibilté pour une courte période
    options['level'] = 1 #influe difficulté
    options['leave'] = False #quitter la fenêtre
    #graphique
    menu_visuals()
    while not start:
        event = donne_ev()
        typeEvent = type_ev(event)
        click = attend_clic_gauche()
        #quitte le jeu
        if typeEvent == 'Quitte':
            options['leave'] = True
            return options
        #two_players
#         if 500 <= click[0] <= 620 and 150 <= click[1] <= 270:
#             if options['two_players'] == True:
#                 efface('p2')
#                 options['two_players'] = False
#                 square(500, 150, 120, gris, '', 3, 'p2')
#                 texte(515, 170, 'PLAYER', gris, police=font, taille=20, tag='p2')
#                 texte(515, 210, 'TWO', gris, police=font, taille=20, tag='p2')
#             else:
#                 efface('p2')
#                 options['two_players'] = True
#                 square(500, 150, 120, blue, '', 3, 'p2')
#                 texte(515, 170, 'PLAYER', blue, police=font, taille=20, tag='p2')
#                 texte(515, 210, 'TWO', blue, police=font, taille=20, tag='p2')
        #obstacles
        if 350 <= click[0] <= 600 and 300 <= click[1] <= 340:
            if options['obstacles'] == 0:
                efface('o')
                options['obstacles'] = 5
                rectangle(350, 300, 600, 340, white, '', 3, 'o')
                texte(365, 305, 'OBSTACLES (5)', white, police=font, taille=16, tag='o')
            else: 
                efface('o')
                options['obstacles'] = 0
                rectangle(350, 300, 600, 340, gris, '', 3, 'o')
                texte(365, 305, 'OBSTACLES', gris, police=font, taille=16, tag='o')
        #collect
        if 350 <= click[0] <= 600 and 360 <= click[1] <= 400:
            if options['collect'] == 0:
                efface('c')
                options['collect'] = 10
                rectangle(350, 360, 600, 400, white, '', 3, 'c')
                texte(365, 365, 'Mode COLLECT (10)', white, police=font, taille=16, tag='c')
            else:
                efface('c')
                options['collect'] = 0
                rectangle(350, 360, 600, 400, gris, '', 3, 'c')
                texte(365, 365, 'Mode COLLECT', gris, police=font, taille=16, tag='c')
        #sparx internes
#         if 350 <= click[0] <= 600 and 420 <= click[1] <= 460:
#             if options['internal_sparx'] == True:
#                 efface('s')
#                 options['internal_sparx'] = False
#                 rectangle(350, 420, 600, 460, gris, '', 3, 's')
#                 texte(365, 425, 'SPARX INTERNES', gris, police=font, taille=16, tag='s')
#             else:
#                 efface('s')
#                 options['internal_sparx'] = True
#                 rectangle(350, 420, 600, 460, white, '', 3, 's')
#                 texte(365, 425, 'SPARX INTERNES', white, police=font, taille=16, tag='s')
        #level
#         if point_in_polygon(click, [(535,590),(535,610),(545,600)]):
#             if options['level'] != 5: 
#                 options['level'] += 1
#                 efface('l')
#                 texte(500, 575, options['level'], white, police=font, taille=22, tag='l')
#             if 1 < options['level'] < 5:
#                 polygone([(535,590),(535,610),(545,600)], white, white, 1, '+')
#                 polygone([(480,590),(480,610),(470,600)], white, white, 1, '-')
#             elif options['level'] == 1:
#                 efface('-')
#             elif options['level'] == 5:
#                 efface('+')
#         elif point_in_polygon(click, [(480,590),(480,610),(470,600)]):
#             if options['level'] != 1:
#                 options['level'] -= 1
#                 efface('l')
#                 texte(500, 575, options['level'], white, police=font, taille=22, tag='l')
#             if 1 < options['level'] < 5:
#                 polygone([(535,590),(535,610),(545,600)], white, white, 1, '+')
#                 polygone([(480,590),(480,610),(470,600)], white, white, 1, '-')
#             elif options['level'] == 1:
#                 efface('-')
#             elif options['level'] == 5:
#                 efface('+')
        #bonus
        if point_in_polygon(click, [(650, 575), (657, 588), (670, 595), (657, 602), (650, 615), (643, 602), (630, 595), (643, 588)]):
            if options['bonus'] != 0:
                options['bonus'] = 2
                efface('b')
                polygone([(650, 575), (657, 588), (670, 595), (657, 602), (650, 615), (643, 602), (630, 595), (643, 588)], gris, '', 2, 'b')
            else:
                options['bonus'] = 2
                efface('b')
                polygone([(650, 575), (657, 588), (670, 595), (657, 602), (650, 615), (643, 602), (630, 595), (643, 588)], 'yellow', 'yellow', 1, 'b')
        #start
        if point_in_polygon(click, [(730,550),(730,620),(790,585)]):
            for tag in all_tags:
                efface(tag)
            return options

    

def menu_visuals():
    rectangle(300,100,850,650,white,'',4,tag='menu') #frame
    #joueur1
    square(350, 150, 120, 'red', '', 3, 'menu')
    texte(365, 170, 'PLAYER', 'red', police=font, taille=20, tag='menu')
    texte(365, 210, 'ONE', 'red', police=font, taille=20, tag='menu')
    #joueur2
    square(500, 150, 120, gris, '', 3, 'p2')
    texte(515, 170, 'PLAYER', gris, police=font, taille=20, tag='p2')
    texte(515, 210, 'TWO', gris, police=font, taille=20, tag='p2')
    #obstacles
    rectangle(350, 300, 600, 340, gris, '', 3, 'o')
    texte(365, 305, 'OBSTACLES', gris, police=font, taille=16, tag='o')
    #mode collect
    rectangle(350, 360, 600, 400, gris, '', 3, 'c')
    texte(365, 365, 'Mode COLLECT', gris, police=font, taille=16, tag='c')
    #sparx internes
    rectangle(350, 420, 600, 460, gris, '', 3, 's')
    texte(365, 425, 'SPARX INTERNES', gris, police=font, taille=16, tag='s')
    #level
    texte(350, 575, 'Niveau', white, police=font, taille=22, tag='menu')
    texte(500, 575, '1', white, police=font, taille=22, tag='l')
    polygone([(535,590),(535,610),(545,600)], white, white, 1, '+')
    #bonus
    polygone([(650, 575), (657, 588), (670, 595), (657, 602), (650, 615), (643, 602), (630, 595), (643, 588)], gris, '', 2, 'b')
    #start
    polygone([(730,550),(730,620),(790,585)], 'white', 'white', 1, 'menu')
    

def draw_coins(collection):
    radius = collection['radius']
    for tag, coin in collection.items():
        if tag != 'radius':
            cercle(coin[0], coin[1], radius, 'yellow', 'yellow', 1, tag)
            
            
def info_collect(collected, total):
    value = str(collected) + ' / ' + str(total)
    rectangle(890,108,1095,200,'yellow','',tag='info_collect')
    texte(900,110,'Collect','yellow',police=font,taille=20)
    texte(950,140,value,'yellow',police=font,taille=15,tag='info')