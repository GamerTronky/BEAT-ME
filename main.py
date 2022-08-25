try:
    import pygame
    import os
    from random import *
    from threading import *
except:
    print('Error: you need to have installed pygame, os, random and threading libary in order to run this code.')
    exit()
print('\n'*50+'BEAT ME')
width,height=900,500
win=pygame.display.set_mode((width,height))
pygame.display.set_caption('BEAT ME')
white=(255,255,255)
black=(0,0,0)
redC=(255,0,0)
yellowC=(255,255,0)
border=pygame.Rect(width//2,0,10,height)
pygame.font.init()
pygame.mixer.init()
bullet_hit_sound=pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
bullet_fire_sound=pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))
race_start_CD=pygame.mixer.Sound(os.path.join('Assets','RaceStartCD1.mp3'))
weaker_font=pygame.font.SysFont('comicsans',20)
weak_font=pygame.font.SysFont('comicsans',40)
win_font=pygame.font.SysFont('comicsans',100)
level='mainMenu'
fps=60
sw,sh=55,40
vel=5
bullet_vel=7
max_bullets=5
red_wins=0
yellow_wins=0
run=True
yellow_hit=pygame.USEREVENT+1
red_hit=pygame.USEREVENT+2
two_player_mode_button_image=pygame.image.load('Assets/2PlayerModeButton.png').convert_alpha()
one_player_mode_button_image=pygame.image.load('Assets/1PlayerModeButton.png').convert_alpha()
yellow_spaceship_image=pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
yellow_spaceship=pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_image,(sw,sh)),90)
red_spaceship_image=pygame.image.load(os.path.join('Assets','spaceship_red.png'))
red_spaceship=pygame.transform.rotate(pygame.transform.scale(red_spaceship_image,(sw,sh)),270)
space=pygame.transform.scale(pygame.image.load(os.path.join('Assets','space.png')),(width,height))
bh=two_player_mode_button_image.get_height()
bw=two_player_mode_button_image.get_width()
bw//=2
class Button:
    def __init__(self,x,y,image,scale):
        width=image.get_width()
        height=image.get_height()
        self.image=pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked=False
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        win.blit(self.image, (self.rect.x, self.rect.y))
        return action
two_player_mode_button=Button(width//2-bw,height//2-bh//2,two_player_mode_button_image,1)
one_player_mode_button=Button(width//2-bw,height//2+bh,one_player_mode_button_image,1)
def draw_window(red, yellow, yellow_bullets, red_bullets, red_hp, yellow_hp, red_wins, yellow_wins):
    win.blit(space,(0,0))
    pygame.draw.rect(win,black,border)
    red_hp_text=weak_font.render('Health: '+str(red_hp),1,white)
    yellow_hp_text=weak_font.render('Health: '+str(yellow_hp),1,white)
    red_wins_text=weak_font.render('Wins: '+str(red_wins),1,white)
    yellow_wins_text=weak_font.render('Wins: '+str(yellow_wins),1,white)
    win.blit(red_hp_text,(width-red_hp_text.get_width()-10,10))
    win.blit(yellow_hp_text,(10,10))
    win.blit(red_wins_text,(width-red_hp_text.get_width()-10,red_hp_text.get_height()-10))
    win.blit(yellow_wins_text,(10,yellow_hp_text.get_height()-10))
    win.blit(yellow_spaceship,(yellow.x,yellow.y))
    win.blit(red_spaceship,(red.x,red.y))
    for bullet in red_bullets:
        pygame.draw.rect(win,redC,bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(win,yellowC,bullet)
    pygame.display.update()
def yellow_movement(keys_pressed, yellow):
    global level
    if level=='2PlayerGame':
        if keys_pressed[pygame.K_a] and yellow.x-vel>0: # LEFT
            yellow.x-=vel
        if keys_pressed[pygame.K_d] and yellow.x+vel+yellow.width<border.x: # RIGHT
            yellow.x+=vel
        if keys_pressed[pygame.K_w] and yellow.y-vel>0: # UP
            yellow.y-=vel
        if keys_pressed[pygame.K_s] and yellow.y+vel+yellow.width<height: # DOWN
            yellow.y+=vel
    elif level=='1PlayerGame':
        if keys_pressed[pygame.K_LEFT] and yellow.x-vel>0: # LEFT
            yellow.x-=vel
        if keys_pressed[pygame.K_RIGHT] and yellow.x+vel+yellow.width<border.x: # RIGHT
            yellow.x+=vel
        if keys_pressed[pygame.K_UP] and yellow.y-vel>0: # UP
            yellow.y-=vel
        if keys_pressed[pygame.K_DOWN] and yellow.y+vel+yellow.width<height: # DOWN
            yellow.y+=vel
def red_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x-vel>border.x+border.width: # LEFT
        red.x-=vel
    if keys_pressed[pygame.K_RIGHT] and red.x+vel+red.width<width: # RIGHT
        red.x+=vel
    if keys_pressed[pygame.K_UP] and red.y-vel>0: # UP
        red.y-=vel
    if keys_pressed[pygame.K_DOWN] and red.y+vel+red.width<height: # DOWN
        red.y+=vel
# noinspection PyUnreachableCode
def red_bot_movement(yellow_bullets,red,red_bullets,shotgen,movegen):
    clock=pygame.time.Clock()
    while run:
        clock.tick(fps)
        if level=='1PlayerGame':
            if not movegen:
                bullets=[]
                bulletsx=[]
                redy=[]
                for bulletex in yellow_bullets:
                    if bulletex.x<red.x+red.width:
                        bulletsx.append(bulletex)
                for bulletexey in bulletsx:
                    for i in range(bulletexey.y,bulletexey.y+bulletexey.height):
                        bullets.append(i)
                if bullets:
                    for i in range(red.y,red.y+red.width):
                        redy.append(i)
                    for bexeyey in bullets:
                        if bexeyey in redy:
                            desty=0
                            if desty<height//2:
                                desty=50
                                movegen.append('UP')
                                movegen.append(desty)
                            elif desty>height//2:
                                desty=height-50
                                movegen.append('DOWN')
                                movegen.append(desty)
                            else:
                                desty=choice([50,height-50])
                                movegen.append(choice(['UP','DOWN']))
                                movegen.append(desty)
                            break
                elif not bullets:
                    if yellow.y>red.y:
                        if red.y+vel+red.width<height:
                            red.y+=vel
                    elif yellow.y<red.y:
                        if red.y-vel>0:
                            red.y-=vel
            elif movegen:
                if movegen[0]=='UP':
                    if movegen[1]<red.y:
                        if red.y-vel>0:
                            red.y-=vel
                    else:
                        movegen.clear()
                elif movegen[0]=='DOWN':
                    if movegen[1]>red.y:
                        if red.y+vel+red.width<height:
                            red.y+=vel
                    else:
                        movegen.clear()
            if len(shotgen)==0:
                if len(red_bullets)<max_bullets:
                    bullet=pygame.Rect(red.x,red.y+red.width/2,10,5)
                    red_bullets.append(bullet)
                    bullet_fire_sound.play()
                    lent=width-(width-red.x)
                    li=0
                    while li<lent*1.9:
                        li+=bullet_vel
                    shotgen.append(li//fps)
            elif len(shotgen)>0:
                if shotgen[0]>0:
                    shotgen[0]-=1
                elif shotgen[0]==0:
                    shotgen.clear()
def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x+=bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x>width:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x-=bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x<0:
            red_bullets.remove(bullet)
def draw_win(winner_text):
    global max_bullets,level
    draw_text=win_font.render(winner_text,1,white)
    win.blit(draw_text,(width/2-draw_text.get_width()/2,height/2-draw_text.get_height()/2))
    pygame.display.update()
    mxbf=max_bullets
    max_bullets=0
    clocko=pygame.time.Clock()
    ticks=0
    timetg=2000
    while True:
        global run
        clocko.tick(fps)
        for eventr in pygame.event.get():
            if eventr.type==pygame.QUIT:
                run=False
                pygame.quit()
        if ticks>timetg/6:
            break
        ticks+=1
    max_bullets=mxbf
    level=f'{level}Start'
def main(red_wins,yellow_wins):
    global level,yellow,red,red_bullets,yellow_bullet,run
    yellow=pygame.Rect(100, 300, sw,sh)
    red=pygame.Rect(700, 300, sw,sh)
    red_bullets=[]
    yellow_bullets=[]
    shotgen=[]
    movegen=[]
    red_hp=10
    yellow_hp=10
    clock=pygame.time.Clock()
    run=True
    rm=Thread(target=red_bot_movement,args=(yellow_bullets,red,red_bullets,shotgen,movegen))
    rm.start()
    while run:
        clock.tick(fps)
        if level=='mainMenu':
            win.blit(space,(0,0))
            choose_player_count_mode=weak_font.render('Choose mode',1,white)
            two_player_description=weaker_font.render('2 Player: Yellow: WASD and left CTRL. Red: Arrows and right CTRL.',1,white)
            one_player_description=weaker_font.render('1 Player: Yellow: Arrows and BOTH CTRL and right SHIFT to shoot.',1,white)
            cpcmw=choose_player_count_mode.get_width()
            win.blit(choose_player_count_mode,(width//2-cpcmw//2,100))
            win.blit(two_player_description,(150,420))
            win.blit(one_player_description,(150,445))
            if two_player_mode_button.draw():
                level='2PlayerGameStart'
            if one_player_mode_button.draw():
                level='1PlayerGameStart'
            pygame.display.update()
        if level=='2PlayerGameStart' or level=='1PlayerGameStart':
            draw_window(red,yellow,yellow_bullets,red_bullets,red_hp,yellow_hp,red_wins,yellow_wins)
            marks=['READY','SET','GO!']
            def do_tick():
                ticks=0
                tick_limit=500
                tick_limit//=12
                while True:
                    if ticks==tick_limit:
                        break
                    clock.tick(fps)
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            pygame.quit()
                            exit()
                    ticks+=1
            for i in range(0,3):
                do_tick()
                ready_set_go=win_font.render(marks[i],1,white)
                draw_window(red,yellow,yellow_bullets,red_bullets,red_hp,yellow_hp,red_wins,yellow_wins)
                win.blit(ready_set_go,(width/2-ready_set_go.get_width()/2,height/2-ready_set_go.get_height()/2))
                race_start_CD.play()
                pygame.display.update()
                do_tick()
                pygame.display.update()
                i+=1
            if level=='2PlayerGameStart':
                level='2PlayerGame'
            if level=='1PlayerGameStart':
                level='1PlayerGame'
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
            if level=='2PlayerGame'or level=='1PlayerGame':
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_LCTRL and len(yellow_bullets)<max_bullets:
                        bullet=pygame.Rect(yellow.x+yellow.width-20,yellow.y+yellow.width/2,10,5)
                        yellow_bullets.append(bullet)
                        bullet_fire_sound.play()
                    if level=='2PlayerGame':
                        if event.key==pygame.K_RCTRL and len(red_bullets)<max_bullets:
                            bullet=pygame.Rect(red.x,red.y+red.width/2,10,5)
                            red_bullets.append(bullet)
                            bullet_fire_sound.play()
                    if level=='1PlayerGame':
                        if event.key==pygame.K_RCTRL and len(yellow_bullets)<max_bullets:
                            bullet=pygame.Rect(yellow.x+yellow.width-20,yellow.y+yellow.width/2,10,5)
                            yellow_bullets.append(bullet)
                            bullet_fire_sound.play()
                        elif event.key==pygame.K_RSHIFT and len(yellow_bullets)<max_bullets:
                            bullet=pygame.Rect(yellow.x+yellow.width-20,yellow.y+yellow.width/2,10,5)
                            yellow_bullets.append(bullet)
                            bullet_fire_sound.play()
                if event.type==red_hit:
                    red_hp-=1
                    bullet_hit_sound.play()
                if event.type==yellow_hit:
                    yellow_hp-=1
                    bullet_hit_sound.play()
        if level=='2PlayerGame'or level=='1PlayerGame':
            winner_text=''
            if red_hp<1:
                winner_text='Yellow WINS!'
                yellow_wins+=1
            if yellow_hp<1:
                winner_text='Red WINS!'
                red_wins+=1
            keys_pressed=pygame.key.get_pressed()
            yellow_movement(keys_pressed, yellow)
            if level=='2PlayerGame':
                red_movement(keys_pressed,red)
            handle_bullets(yellow_bullets,red_bullets,yellow,red)
            draw_window(red,yellow,yellow_bullets,red_bullets,red_hp,yellow_hp,red_wins,yellow_wins)
            if winner_text !='':
                draw_win(winner_text)
                break
    main(red_wins,yellow_wins)
if __name__=='__main__':
    main(red_wins, yellow_wins)