import pygame 
from pygame.locals import *
from copy import deepcopy
import random 

pygame.init()

pygame.display.set_caption('Mastermind')

COLORS = {
    'RED':          (255, 0, 0),
    'ORANGE':       (255, 165, 0),
    'YELLOW':       (255,255,0),
    'GREEN':        (0, 255, 0),
    'BLUE':         (0, 0, 255),
    'PURPLE':       (160, 32, 240),
    'BLACK':        (0, 0, 0),
    'WHITE':        (255, 255, 255),
    'LIGHT_GREY':   (170,170,170),
    'DARK_GREY':    (100,100,100)
}

PEGS_IMAGES = [
    pygame.image.load('assets/red_circle.png'),
    pygame.image.load('assets/orange_circle.png'),
    pygame.image.load('assets/yellow_circle.png'),
    pygame.image.load('assets/green_circle.png'),
    pygame.image.load('assets/blue_circle.png'),
    pygame.image.load('assets/purple_circle.png')
]

HINT_PEGS_IMAGES = [
    pygame.image.load('assets/white_circle.png'),
    pygame.image.load('assets/dark_red_circle.png')
    
]

GREY_PEG = pygame.image.load('assets/grey_circle.png')

CHECK_MARK = pygame.image.load('assets/check.png')

ANS_RECTS = [Rect((125,15),(70,70)),Rect((220,15),(70,70)),Rect((315,15),(70,70)),Rect((410,15),(70,70))]
SEL_RECTS = [Rect((120,855),(50,50)),Rect((183,855),(50,50)),Rect((246,855),(50,50)),Rect((309,855),(50,50)),Rect((372,855),(50,50)),Rect((435,855),(50,50))]
GUESS_RECTS = [ [Rect((125,120),(70,70)),Rect((220,120),(70,70)),Rect((315,120),(70,70)),Rect((410,120),(70,70))],
                [Rect((125,210),(70,70)),Rect((220,210),(70,70)),Rect((315,210),(70,70)),Rect((410,210),(70,70))],
                [Rect((125,300),(70,70)),Rect((220,300),(70,70)),Rect((315,300),(70,70)),Rect((410,300),(70,70))],
                [Rect((125,390),(70,70)),Rect((220,390),(70,70)),Rect((315,390),(70,70)),Rect((410,390),(70,70))],
                [Rect((125,480),(70,70)),Rect((220,480),(70,70)),Rect((315,480),(70,70)),Rect((410,480),(70,70))],
                [Rect((125,570),(70,70)),Rect((220,570),(70,70)),Rect((315,570),(70,70)),Rect((410,570),(70,70))],
                [Rect((125,660),(70,70)),Rect((220,660),(70,70)),Rect((315,660),(70,70)),Rect((410,660),(70,70))],
                [Rect((125,750),(70,70)),Rect((220,750),(70,70)),Rect((315,750),(70,70)),Rect((410,750),(70,70))],
]
CHECK_RECT = Rect((10,10),(80,80))

HINT_RECTS = [  [Rect((20,127),(25,25)),Rect((50,127),(25,25)),Rect((20,158),(25,25)),Rect((50,158),(25,25))],
                [Rect((20,217),(25,25)),Rect((50,217),(25,25)),Rect((20,248),(25,25)),Rect((50,248),(25,25))],
                [Rect((20,307),(25,25)),Rect((50,307),(25,25)),Rect((20,338),(25,25)),Rect((50,338),(25,25))],
                [Rect((20,397),(25,25)),Rect((50,397),(25,25)),Rect((20,428),(25,25)),Rect((50,428),(25,25))],
                [Rect((20,487),(25,25)),Rect((50,487),(25,25)),Rect((20,518),(25,25)),Rect((50,518),(25,25))],
                [Rect((20,577),(25,25)),Rect((50,577),(25,25)),Rect((20,608),(25,25)),Rect((50,608),(25,25))],
                [Rect((20,667),(25,25)),Rect((50,667),(25,25)),Rect((20,698),(25,25)),Rect((50,698),(25,25))],
                [Rect((20,757),(25,25)),Rect((50,757),(25,25)),Rect((20,788),(25,25)),Rect((50,788),(25,25))],

]

width = 500
height = 920
res = (width,height) 
screen = pygame.display.set_mode(res)
state = 0
players = 0
pattern = (-1,-1,-1,-1)
patterns = [[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
hints = [[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
round = 0
pressed_tile = (-1,-1)
verify = False
won = False

def play():
    global pressed_tile
    global round
    global patterns
    global verify
    global won
                        
    screen.fill((COLORS['BLUE'][0]+10,COLORS['BLUE'][1]+75,COLORS['BLUE'][2]-100))
    pygame.draw.rect(screen,(COLORS['BLUE'][0],COLORS['BLUE'][1],COLORS['BLUE'][2]-150),Rect((0,100),(width,7)))
    pygame.draw.rect(screen,(COLORS['BLUE'][0],COLORS['BLUE'][1],COLORS['BLUE'][2]-150),Rect((100,0),(7,height)))
    pygame.draw.rect(screen,(COLORS['BLUE'][0],COLORS['BLUE'][1],COLORS['BLUE'][2]-150),Rect((0,835),(width,7)))
    screen.blit(pygame.transform.scale(CHECK_MARK,(80,80)),CHECK_RECT)

    for ev in pygame.event.get():
          
        if ev.type == pygame.QUIT:
            pygame.quit()
        
        if ev.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if CHECK_RECT.collidepoint(pos):
                if -1 not in patterns[round]:
                    print('verify')
                    verify = True
            
            for i in range(4):
                if GUESS_RECTS[round][i].collidepoint(pos):
                    pressed_tile = (round,i)
            
            for i in range(6):
                if SEL_RECTS[i].collidepoint(pos):
                    if pressed_tile != (-1,-1):
                        patterns[round][pressed_tile[1]] = i
                        pressed_tile = (-1,-1)

    for r in range(round+1):
        for i in range(len(GUESS_RECTS[r])):
            if (r,i) == pressed_tile:
                pygame.draw.rect(screen,COLORS['LIGHT_GREY'],GUESS_RECTS[r][i].inflate(10,10))
                pygame.draw.rect(screen,(COLORS['BLUE'][0]+10,COLORS['BLUE'][1]+75,COLORS['BLUE'][2]-100),GUESS_RECTS[r][i])
            if patterns[r][i] == -1:
                screen.blit(pygame.transform.scale(GREY_PEG,(70,70)), GUESS_RECTS[r][i])
            else:
                screen.blit(pygame.transform.scale(PEGS_IMAGES[patterns[r][i]],(70,70)), GUESS_RECTS[r][i])
            if hints[r][i] == -1:
                screen.blit(pygame.transform.scale(GREY_PEG,(25,25)), HINT_RECTS[r][i])
            else:
                screen.blit(pygame.transform.scale(HINT_PEGS_IMAGES[hints[r][i]],(25,25)), HINT_RECTS[r][i])
    
    for i in range(len(SEL_RECTS)):
        screen.blit(pygame.transform.scale(PEGS_IMAGES[i],(50,50)),SEL_RECTS[i])

    if verify:
        verify = False
        correct_place = 0
        correct_peg = 0
        counted = [-1,-1,-1,-1]
        for i in range(4):
            if patterns[round][i] == pattern[i]:
                if counted[i] == -1:
                    correct_place += 1
                    counted[i] = 1
        for i in range(4):
            for j in range(4):
                if patterns[round][i] == pattern[j]:
                    if counted[j] == -1:
                        correct_peg += 1
                        counted[j] = 0
                        break

        if correct_place == 4:
            won = True
        i = 0
        hints[round] = deepcopy(counted)
        hints[round].sort()
        hints[round].reverse()

        print(hints[round])
        round += 1
        

    if won or round == 8:
        for i in range(4):
            screen.blit(pygame.transform.scale(PEGS_IMAGES[pattern[i]],(70,70)), ANS_RECTS[i])
        won = True
    
    # show RECTS
    #for r in ANS_RECTS:
    #    pygame.draw.rect(screen,COLORS['LIGHT_GREY'],r)
    #for i in range(8):
    #    for r in GUESS_RECTS[i]:
    #        pygame.draw.rect(screen,COLORS['LIGHT_GREY'],r)
    #for r in SEL_RECTS:
    #    pygame.draw.rect(screen,COLORS['LIGHT_GREY'],r)
    #pygame.draw.rect(screen,COLORS['LIGHT_GREY'],CHECK_RECT)
    #for i in range(len(HINT_RECTS)):
    #    for r in HINT_RECTS[i]:
    #        pygame.draw.rect(screen,COLORS['LIGHT_GREY'],r)
                    
def choose_pattern():
    if players == 1:
        random.seed()
        return ((random.randint(0,5),random.randint(0,5),random.randint(0,5),random.randint(0,5)),2)
    else:
        for ev in pygame.event.get():

            if ev.type == pygame.QUIT: 
                pygame.quit()
            
            if ev.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

def menu():
    # defining a font 
    title_font = pygame.font.SysFont('Consolas',75) 
    button_font = pygame.font.SysFont('Consolas',50)
    
    # rendering a text written in 
    # this font 
    mastermind_title = [title_font.render('MASTERMIND' , True , COLORS['BLACK']), title_font.render('MASTERMIND' , True , COLORS['WHITE'])]
    one_player_text = button_font.render('One Player' , True , COLORS['BLACK'])
    two_player_text = button_font.render('Two Players' , True , COLORS['BLACK'])

    one_player_rect = Rect((10,100),(200,80))
    two_player_rect = Rect((10,200),(200,80))

    for ev in pygame.event.get():
          
        if ev.type == pygame.QUIT: 
            pygame.quit()
        
        if ev.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if one_player_rect.collidepoint(pos):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/button_press.wav"))
                return (1,1)
            elif two_player_rect.collidepoint(pos):
                pygame.mixer.Sound.play(pygame.mixer.Sound("assets/button_press.wav"))
                return (2,1)

    screen.fill(COLORS['DARK_GREY'])
    screen.blit(mastermind_title[0],(44,14))
    screen.blit(mastermind_title[1],(40,10))

    mouse = pygame.mouse.get_pos()

    if one_player_rect.collidepoint(mouse):
        pygame.draw.rect(screen,COLORS['LIGHT_GREY'],one_player_rect)
    else:
        pygame.draw.rect(screen,COLORS['WHITE'],one_player_rect)
    if two_player_rect.collidepoint(mouse):
        pygame.draw.rect(screen,COLORS['LIGHT_GREY'],two_player_rect)
    else:
        pygame.draw.rect(screen,COLORS['WHITE'],two_player_rect)

    return (0,0)

while True:  
    if state == 0:
        players,state = menu()
    elif state == 1:
        pattern,state = choose_pattern()
        print(pattern)
    elif state == 2:
        play()
      
    # updates the frames of the game 
    pygame.display.update()
    if won:
        input()
        pygame.quit()