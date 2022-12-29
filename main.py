import pygame 
from pygame.locals import *
from copy import deepcopy
import random 
from assets import *

pygame.init()
pygame.mixer.init()

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

LOGO_RECT = Rect((43,10),(410,60))

PICK_RECTS = [Rect((20,125),(100,100)),Rect((140,125),(100,100)),Rect((260,125),(100,100)),Rect((380,125),(100,100))]

SEL_PICK_RECTS = [Rect((20,255),(65,65)),Rect((99,255),(65,65)),Rect((178,255),(65,65)),Rect((257,255),(65,65)),Rect((338,255),(65,65)),Rect((415,255),(65,65))]

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
pattern = [-1,-1,-1,-1]
patterns = [[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
hints = [[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
round = 0
pressed_tile = (-1,-1)
picked_tile = -1
verify = False
won = False
done = False
button_press_sound = pygame.mixer.Sound('assets/button_press.wav') 
peg_select_sound = pygame.mixer.Sound('assets/button_pop.wav') 
check_press = pygame.mixer.Sound('assets/check_press.wav')
won_sound = pygame.mixer.Sound('assets/won_game.wav')
lost_sound = pygame.mixer.Sound('assets/lost_game.wav')
menu_sound = pygame.mixer.Sound('assets/main_menu.wav')
playing_sound = pygame.mixer.Sound('assets/playing.wav')

menu_music = pygame.mixer.Channel(1)
menu_music.set_volume(0.75)
fx = pygame.mixer.Channel(2)
fx.set_volume(0.9)
play_music = pygame.mixer.Channel(3)
play_music.set_volume(0.25)

def play():

    menu_music.stop()
    if not play_music.get_busy():
        play_music.play(playing_sound)

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
                fx.play(check_press)
                if -1 not in patterns[round]:
                    verify = True
            
            for i in range(4):
                if GUESS_RECTS[round][i].collidepoint(pos):
                    fx.play(peg_select_sound)
                    pressed_tile = (round,i)
            
            for i in range(6):
                if SEL_RECTS[i].collidepoint(pos):
                    fx.play(peg_select_sound)
                    if pressed_tile != (-1,-1):
                        patterns[round][pressed_tile[1]] = i

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
        counted = [-1,-1,-1,-1]
        guess_counted = [-1,-1,-1,-1]
        for i in range(4):
            if patterns[round][i] == pattern[i]:
                counted[i] = 1
                guess_counted[i] = 1
        for i in range(4):
            if guess_counted[i] != -1:
                continue
            for j in range(4):
                if patterns[round][i] == pattern[j]:
                    if counted[j] != -1:
                        continue
                    counted[j] = 0
                    guess_counted[i] = 0
                    break

        if sum(counted) == 4:
            won = True
        hints[round] = deepcopy(counted)
        hints[round].sort()
        hints[round].reverse()
        round += 1
        

    if won or round == 8:
        for i in range(4):
            screen.blit(pygame.transform.scale(PEGS_IMAGES[pattern[i]],(70,70)), ANS_RECTS[i])
        if won:
            fx.play(won_sound)
        else:
            fx.play(lost_sound)
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

    pygame.display.update()
       
def choose_pattern():
    global picked_tile
    global pattern
    global state
    
    if players == 1:
        random.seed()
        state = 2
        pattern = (random.randint(0,5),random.randint(0,5),random.randint(0,5),random.randint(0,5))
        return
    else:
        title_font = pygame.font.SysFont('Consolas',40)
        screen.fill(COLORS['DARK_GREY'])
        back_rect = Rect((150,800),(200,80))
        pygame.draw.rect(screen,COLORS['LIGHT_GREY'],Rect((0,100),(width,7)))
        pygame.draw.rect(screen,COLORS['LIGHT_GREY'],Rect((100,0),(7,101)))
        pygame.draw.rect(screen,COLORS['WHITE'],back_rect)
        screen.blit(pygame.transform.scale(CHECK_MARK,(80,80)),CHECK_RECT)
        screen.blit(title_font.render('Choose a Pattern' , True , COLORS['BLACK']),(122,27))
        screen.blit(title_font.render('Choose a Pattern' , True , COLORS['WHITE']),(120,25))
        button_font = pygame.font.SysFont('Consolas',30)
        button_font_larger = pygame.font.SysFont('Consolas',35)
        back_text = button_font.render('Back' , True , COLORS['BLACK'])
        back_text_larger = button_font_larger.render('Back' , True , COLORS['BLACK'])

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT: 
                pygame.quit()
            
            if ev.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if CHECK_RECT.collidepoint(pos):
                    fx.play(check_press)
                    if -1 not in pattern:
                        state = 2
                        return
                    continue
                if back_rect.collidepoint(pos):
                    fx.play(button_press_sound)
                    state = 0
                    return
                for i in range(4):
                    if PICK_RECTS[i].collidepoint(pos):
                        fx.play(peg_select_sound)
                        picked_tile = i
                for i in range(6):
                    if SEL_PICK_RECTS[i].collidepoint(pos):
                        fx.play(peg_select_sound)
                        if picked_tile != -1:
                            pattern[picked_tile] = i
        
        for i in range(len(SEL_PICK_RECTS)):
            screen.blit(pygame.transform.scale(PEGS_IMAGES[i],(65,65)),SEL_PICK_RECTS[i])
        for i in range(len(PICK_RECTS)):
            if i == picked_tile:
                pygame.draw.rect(screen,COLORS['LIGHT_GREY'],PICK_RECTS[i].inflate(10,10))
                pygame.draw.rect(screen,COLORS['DARK_GREY'],PICK_RECTS[i])
            if pattern[i] == -1:
                screen.blit(pygame.transform.scale(GREY_PEG,(100,100)), PICK_RECTS[i])
            else:
                screen.blit(pygame.transform.scale(PEGS_IMAGES[pattern[i]],(100,100)), PICK_RECTS[i])

        mouse = pygame.mouse.get_pos()
        if back_rect.collidepoint(mouse):
            pygame.draw.rect(screen,COLORS['LIGHT_GREY'],back_rect.inflate(10,10))
            screen.blit(back_text_larger,(210,825))
        else:
            pygame.draw.rect(screen,COLORS['WHITE'],back_rect)
            screen.blit(back_text,(210,825))

    pygame.display.update()

def menu():

    mouse = pygame.mouse.get_pos()

    play_music.stop()
    if not menu_music.get_busy():
        menu_music.play(menu_sound)

    # defining a font 
    title_font = pygame.font.SysFont('Consolas',75) 
    button_font = pygame.font.SysFont('Consolas',30)
    button_font_larger = pygame.font.SysFont('Consolas',35)
    
    # rendering a text written in 
    # this font 
    mastermind_title = [title_font.render('MASTERMIND' , True , COLORS['BLACK']), title_font.render('MASTERMIND' , True , COLORS['WHITE'])]
    one_player_text = button_font.render('One Player' , True , COLORS['BLACK'])
    one_player_text_larger = button_font_larger.render('One Player' , True , COLORS['BLACK'])
    two_player_text = button_font.render('Two Players' , True , COLORS['BLACK'])
    two_player_text_larger = button_font_larger.render('Two Players' , True , COLORS['BLACK'])
    quit_text = button_font.render('Quit' , True , COLORS['BLACK'])
    quit_text_larger = button_font_larger.render('Quit' , True , COLORS['BLACK'])

    one_player_rect = Rect((150,125),(200,100))
    two_player_rect = Rect((150,275),(200,100))
    quit_rect = Rect((150,800),(200,80))

    for ev in pygame.event.get():
          
        if ev.type == pygame.QUIT: 
            pygame.quit()
        
        if ev.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if one_player_rect.collidepoint(pos):
                fx.play(button_press_sound)
                pygame.display.update()
                return (1,1)
            elif two_player_rect.collidepoint(pos):
                fx.play(button_press_sound)
                pygame.display.update()
                return (2,1)
            elif quit_rect.collidepoint(pos):
                fx.play(button_press_sound)
                pygame.quit()

    if LOGO_RECT.collidepoint(mouse):
        screen.fill((random.randint(0,255),random.randint(0,255),random.randint(0,255)))
        screen.blit(mastermind_title[0],(44,14))
        screen.blit(title_font.render('MASTERMIND' , True , (random.randint(0,255),random.randint(0,255),random.randint(0,255))),(40,10))
    else:
        screen.fill(COLORS['DARK_GREY'])
        screen.blit(mastermind_title[0],(44,14))
        screen.blit(mastermind_title[1],(40,10))

    if one_player_rect.collidepoint(mouse):
        pygame.draw.rect(screen,COLORS['LIGHT_GREY'],one_player_rect.inflate(10,10))
        screen.blit(one_player_text_larger,(155,160))
    else:
        pygame.draw.rect(screen,COLORS['WHITE'],one_player_rect)
        screen.blit(one_player_text,(170,160))
    if two_player_rect.collidepoint(mouse):
        pygame.draw.rect(screen,COLORS['LIGHT_GREY'],two_player_rect.inflate(10,10))
        screen.blit(two_player_text_larger,(145,312))
    else:
        pygame.draw.rect(screen,COLORS['WHITE'],two_player_rect)
        screen.blit(two_player_text,(157,312))
    if quit_rect.collidepoint(mouse):
        pygame.draw.rect(screen,COLORS['LIGHT_GREY'],quit_rect.inflate(10,10))
        screen.blit(quit_text_larger,(210,825))
    else:
        pygame.draw.rect(screen,COLORS['WHITE'],quit_rect)
        screen.blit(quit_text,(210,825))

    pygame.display.update()
    
    return (0,0)

def play_again():

    menu_music.stop()
    if not play_music.get_busy():
        play_music.play(playing_sound)

    title_font = pygame.font.SysFont('Consolas',66)
    yes_no_font = pygame.font.SysFont('Consolas',40)
    play_again_text = title_font.render('Play Again?' , True , COLORS['BLACK'])
    yes_text = yes_no_font.render('Yes' , True , COLORS['BLACK'])
    no_text = yes_no_font.render('No' , True , COLORS['BLACK'])

    play_again_rect = Rect((50,200),(400,200))
    yes_rect = Rect((70,325),(150,60))
    no_rect = Rect((275,325),(150,60))
    pygame.draw.rect(screen,COLORS['LIGHT_GREY'],play_again_rect)
    pygame.draw.rect(screen,COLORS['GREEN'],yes_rect)
    pygame.draw.rect(screen,COLORS['RED'],no_rect)
    screen.blit(play_again_text,(55,210))
    screen.blit(yes_text,(110,337))
    screen.blit(no_text,(328,340))
    pygame.display.update()

    for ev in pygame.event.get():
          
        if ev.type == pygame.QUIT: 
            pygame.quit()
        
        if ev.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if yes_rect.collidepoint(pos):
                fx.play(button_press_sound)
                return 1
            elif no_rect.collidepoint(pos):
                fx.play(button_press_sound)
                return 2
    return 0

def reset_vars():
    global state
    global players
    global pattern
    global patterns
    global hints
    global round
    global pressed_tile
    global verify
    global won
    global done
    global picked_tile

    state = 0
    picked_tile = -1
    pattern = [-1,-1,-1,-1]
    patterns = [[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
    hints = [[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1],[-1,-1,-1,-1]]
    round = 0
    pressed_tile = (-1,-1)
    verify = False
    won = False
    done = False

while True:
    if state == 0:
        players,state = menu()
    elif state == 1:
        choose_pattern()
    elif state == 2:
        play()

    if won:
        while True:
            again = play_again()
            if again == 0:
                continue
            elif again == 1:
                reset_vars()
                state = 1
                break
            else:
                reset_vars()
                state = 0
                break