import pygame,time,random,sys,os

pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.height,self.width=75,75
        self.x,self.y=max_x/2-self.width*0.5,max_y/2-self.height*0.5
        self.x_change,self.y_change=0,0
        self.image=pygame.Surface((self.height,self.width))
        self.rect=self.image.get_rect()
        self.rect.topleft=(self.x,self.y)
        self.health=1000
        self.maxhealth=1000
        #self.level=1
        self.sparkling=False
        self.sparkletime=0
        #self.exp=0

    def update(self):
        global gamequit
        self.x+=self.x_change
        self.y+=self.y_change
        if self.x-5>max_x:
            self.x=5-self.width
        if self.y-5>max_y:
            self.y=5-self.height
        if self.x<0-(self.width-5):
            self.x=max_x-5
        if self.y<0-(self.height-5):
            self.y=max_y-5
        self.rect.topleft=self.x,self.y
        if self.health<=0:
            text(50,"Failed in floor"+str(floor),max_x/2,max_y/2)
            pygame.display.update()
            time.sleep(3)
            self.kill()
            pygame.quit()
            quit()
        if self.sparkling:
            self.sparkletime-=1
            if self.sparkletime<=0:
                self.sparkling==False
                self.sparkletime=0
            if self.sparkletime%2==0:
                pygame.draw.rect(window,(0,225,0),(self.x,self.y,self.width,self.height))
            else:
                pygame.draw.rect(window,(255,100,50),(self.x,self.y,self.width,self.height))
        else:
            pygame.draw.rect(window,(0,225,0),(self.x,self.y,self.width,self.height))
        pygame.draw.rect(window,(100,100,100,0.3),(0,max_y-20,self.maxhealth/10,20))
        pygame.draw.rect(window,(225,10,10,0.3),(0,max_y-20,self.health/10,20))
        self.rect.topleft=(self.x,self.y)

    def got_hit(self,losshealth):
        self.health-=losshealth
        self.sparkling=True
        self.sparkletime=30
    

class Enemy(pygame.sprite.Sprite):
    def __init__(self,groups):
        super(Enemy, self).__init__()
        self.radius=30
        self.x=random.randrange(100,max_x-100)
        self.y=random.randrange(100,max_y-100)
        self.image=pygame.Surface((self.radius*2,self.radius*2))
        self.rect=self.image.get_rect()
        #self.rect.center=(self.x,self.y)
        self.add(groups)
        self.speed=random.randrange(5,16,3)
        self.isdieing=False
        self.counting=10

    def update(self):
        if self.speed<=0:
            if self.speed==0:
                self.speed=random.randrange(1,9,2)
            else:
                self.speed=0-self.speed
        if self.x-self.speed !=0:
            self.x=random.randrange(self.x-self.speed,self.x+self.speed)
        else:
            self.x+=self.speed
        if self.y-self.speed !=0:
            self.y=random.randrange(self.y-self.speed,self.y+self.speed)
        else:
            self.y+=self.speed 
        if self.x+self.radius>=max_x:
            self.x=max_x-self.radius
        if self.y+self.radius>=max_y:
            self.y=max_y-self.radius
        if self.x+self.radius<0:
            self.x=0-self.radius
        if self.y+self.radius<0:
            self.y=0-self.radius            
        self.rect.center=self.x,self.y
        if random.randrange(1,5)==4:
            if self.speed-3 !=0:     
                self.speed=random.randrange(self.speed-3,self.speed+3)
            else:
                self.speed+=2
        if self.isdieing:
            self.counting-=1
        if self.counting%2==0:
            pygame.draw.circle(window,(150,150,150),(self.x,self.y),self.radius)
        else:
            pygame.draw.circle(window,(255,10,10),(self.x,self.y),self.radius)
        if self.counting<=0:
            self.isdieing=False
            self.kill()
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self,groups,x,y,target_x,target_y):
        super(Bullet,self).__init__()
        self.radius=10
        self.height,self.width=7,7
        self.x=x
        self.y=y
        self.image=pygame.Surface((self.radius,self.radius))
        self.rect=self.image.get_rect()
        speed=random.randint(15000,20000)/100000
        self.plus_x=(0-(x-target_x))*speed
        self.plus_y=(0-(y-target_y))*speed
        self.add(groups)
        self.started_x=self.x
        self.started_y=self.y

    def update(self):
        self.x+=self.plus_x   
        self.y+=self.plus_y
        self.x=int(self.x)
        self.y=int(self.y)
        self.rect.center=(self.x,self.y)
        pygame.draw.rect(window,(50,110,200),(self.x,self.y,self.height,self.width))
        if self.x>max_x or self.x<0 or self.y>max_y or self.y<0:
            self.kill()


class EnemyBullet(Bullet):
    def update(self):
        self.x+=self.plus_x/5
        self.y+=self.plus_y/5
        self.x=int(self.x)
        self.y=int(self.y)
        self.rect.center=(self.x,self.y)
        pygame.draw.circle(window,(0,0,0),(self.x,self.y),self.radius)
        if self.x>max_x or self.x<0 or self.y>max_y or self.y<0:
            self.kill()


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss,self).__init__()
        self.x=random.choice([player.x+150,player.x-150,player.x+random.randrange(-200,200)])
        self.y=random.choice([player.x+150,player.y-150,player.y+random.randrange(-200,200)])
        if self.x <= 50:
            self.x=50
        if self.y<=50:
            self.y=50
        if self.x>=750:
            self.x=750
        if self.y>=750:
            self.y=750
        self.maxhealth=1000*(2**floor)*[1,1.2,1.3][floor-1]
        self.health=self.maxhealth
        self.height,self.width=100,100
        self.image=pygame.image.load("boss"+str(floor)+".png")
        self.rect=self.image.get_rect()
        self.rect.topleft=(self.x,self.y)
        self.target=[[400,0],[25,800],[775,800]]
        self.shoot_clockwise=True
    
    def update(self):
        global floor,bossfighting
        window.blit(self.image,(self.x,self.y))
        pygame.draw.rect(window,(125,125,125),(self.x,self.y+self.height+10
                        ,self.maxhealth/10/(2**floor)/[1,1.2,1.3][floor-1],10))
        pygame.draw.rect(window,(225,25,25),(self.x,self.y+self.height+10
                        ,self.health/10/(2**floor)/[1,1.2,1.3][floor-1],10))


class skill(pygame.sprite.Sprite):
    def __init__(self,number):
        self.number=number
        self.image=pygame.image.load("skill"+str(number)+".png")
        self.rect=self.image.get_rect()
        self.colling_maxtime=[300,700,1200][number-1]
        self.colling=0
        (self.x,self.y)=[(650,600),(700,600),(755,600)][number-1]
        if number == 2:
            self.lighting=pygame.image.load("lighting.png")
        if number == 3:
            self.running=False
    def update(self):
        window.blit(self.image,(self.x,self.y))
        if self.colling>0:
            text(20,str(int(self.colling/20)+1),self.x+22,self.y+20)
            self.colling-=1
        text(15,str(self.number),self.x+35,self.y+10)                


class glass(pygame.sprite.Sprite):
    def __init__(self,x,y,groups):
        super(glass,self).__init__()
        self.x=x
        self.y=y
        self.add(groups)
        self.face_direction=random.choice([1,2,3,4])
        self.image=pygame.Surface((50,50))
        self.rect=self.image.get_rect()
        self.started_x=x
        self.started_y=y
    def update(self):
        if self.face_direction == 1:    
            pygame.draw.polygon((window), (20,225,255), [[self.x, self.y], [self.x-50, self.y], [self.x, self.y-50]])
            self.rect.bottomright=self.x,self.y
        if self.face_direction == 2:    
            pygame.draw.polygon((window), (20,225,255), [[self.x, self.y], [self.x+50, self.y], [self.x, self.y-50]])
            self.rect.bottomleft=self.x,self.y 
        if self.face_direction == 3:    
            pygame.draw.polygon((window), (20,225,255), [[self.x, self.y], [self.x+50, self.y], [self.x, self.y+50]])
            self.rect.topleft=self.x,self.y 
        if self.face_direction == 4:    
            pygame.draw.polygon((window), (20,225,255), [[self.x, self.y], [self.x-50, self.y], [self.x, self.y+50]])
            self.rect.topright=self.x,self.y         


def text(text_size,text,x,y):
    text_big = pygame.font.Font("arial.ttf",text_size)
    TextSurf,TextRect = text_objects(text,text_big)
    TextRect.center = (x,y)
    window.blit(TextSurf,TextRect)
    
def text_objects(text,font):
    textsurface=font.render(text,True,(0,0,0))
    return textsurface,textsurface.get_rect()

def menu():
    os.system("cls")
    string1='歡迎來到「一個方塊的冒險」'
    for letter in string1:
        print(letter,end='')
        sys.stdout.flush()
        time.sleep(0.15)
    print()    
    time.sleep(0.2)
    string2="如果你要進入遊戲請輸入Y，否則輸入任意鍵退出遊戲"
    for letter in string2:
        print(letter,end='')
        sys.stdout.flush()
        time.sleep(0.15)
    print()    
    time.sleep(0.2)
    choice=input().lower()
    if choice == "y":
        string3="在遊戲中，數字鍵可以招喚技能，方向鍵或wasd鍵可以移動，遊戲即將在5秒後開始"
        for letter in string3:
            print(letter,end='')
            time.sleep(0.15)
            sys.stdout.flush()
        time.sleep(5)
        max_x,max_y=800,800
        game()
    else:
        pygame.quit()
        quit()

def control():
    global dieenemy
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.y_change=-8
                if skill3.running:
                    player.y_change=-100
                    skill3.running=False
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.y_change=8
                if skill3.running:
                    player.y_change=100
                    skill3.running=False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.x_change=-8
                if skill3.running:
                    player.x_change=-100
                    skill3.running=False
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.x_change=8
                if skill3.running:
                    player.x_change=100
                    skill3.running=False
            if event.key == pygame.K_1 and skill1.colling==0:
                player.health+=player.maxhealth/5
                if player.health>=player.maxhealth:
                    player.health=player.maxhealth
                skill1.colling=skill1.colling_maxtime
            if event.key == pygame.K_2 and skill2.colling==0:
                if bossfighting:
                    window.blit(skill2.lighting,(boss.x+50,boss.y-30))
                    boss.health-=boss.maxhealth/20
                    pygame.display.update()
                    time.sleep(0.5)
                    thunder_sound=pygame.mixer.Sound("thunder.wav")
                    pygame.mixer.Sound.play(thunder_sound)
                    time.sleep(0.5)
                else:
                    for enemy in enemies:
                        window.blit(skill2.lighting,(enemy.x-100,enemy.y-180))
                        pygame.display.update()
                        time.sleep(0.15)
                    pygame.display.update()
                    time.sleep(0.5)
                    thunder_sound=pygame.mixer.Sound("thunder.wav")
                    pygame.mixer.Sound.play(thunder_sound)
                    time.sleep(0.5)
                    dieenemy+=enemies
                    for enemy in enemies:
                        enemy.kill()
                skill2.colling=skill2.colling_maxtime
            if event.key == pygame.K_3 and skill3.colling==0:
                skill3.running=True
                skill3.colling=skill3.colling_maxtime
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT,
                             pygame.K_a,pygame.K_w,pygame.K_s,pygame.K_d):
                player.x_change,player.y_change=0,0
        
def set_up():
    global enemies,max_x,max_y,window,player,gamequit,click,mouse,skill3,skill2,glasses
    global front_sight1,front_sight2 ,background_list,floor,bullets,enemybullets,shot_sound,explode_sound
    global count1,dieenemy,enemy_dead,bossfighting,force_plus,plustime,bossbullets,skill1
    max_x,max_y=800,800
    floor = 1
    shot_sound=pygame.mixer.Sound("shot.wav") 
    explode_sound=pygame.mixer.Sound("explode.wav") 
    click=pygame.mouse.get_pressed()
    mouse=pygame.mouse.get_pos()
    window_size = (max_x, max_y)
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption('一個方塊的冒險')
    player = Player()
    gamequit=False
    enemies=pygame.sprite.Group()
    front_sight1 = pygame.image.load("front_sight.png")
    front_sight2 = pygame.image.load("red_front_sight.png")
    background_list=[pygame.image.load("floor1background.png"), 
                     pygame.image.load("floor2background.png"),  
                     pygame.image.load("floor3background.png"),
                     pygame.image.load("floor1background.png"),
                     pygame.image.load("floor1background.png"),]
    bullets=pygame.sprite.Group()
    enemybullets=pygame.sprite.Group()
    bossbullets=pygame.sprite.Group()
    count1=50
    dieenemy=[]
    enemy_dead=0
    bossfighting=False
    force_plus=1
    plustime=0
    skill1=skill(1)
    skill2=skill(2)
    skill3=skill(3)
    glasses=pygame.sprite.Group()
    pygame.mixer.music.load("floor1music.mp3")
    pygame.mixer.music.play(-1)
def play():
    global count1,dieenemy,enemy_dead,floor,bossfighting,boss,force_plus,plustime
    if floor==4:
        pygame.mixer.music.load("floor4music.mp3")
        pygame.mixer.music.play(-1)
        text(120,"Victory!",400,400)
        pygame.display.update()
        time.sleep(0.5)
        ok=0
        while ok == 0:
            ok=input("無限模式?[0=不好,1=好]")
            if ok == "1" or "好" or ok[0]=="y" or ok[0]=="Y":
                floor=5
                pygame.mixer.music.load("floor5music.mp3")
                pygame.mixer.music.play(-1)
            else:
                pygame.quit()
                quit()
    window.blit(background_list[floor-1],(0,0))
    click = pygame.mouse.get_pressed()
    mouse = pygame.mouse.get_pos()
    for enemy in enemies:
        enemy.update()
    for bullet in bullets:
        bullet.update()
    for enemybullet in enemybullets:
        enemybullet.update()
    if not bossfighting:
        if len(enemies)==0:
            for _ in range(random.randrange(1,4+floor)):
                Enemy(enemies)
    else:
        boss.update()
        if boss.health<=0:
            floor+=1
            if floor == 2:
                pygame.mixer.music.load("floor2music.mp3")
                pygame.mixer.music.play(-1)
                for _ in range(random.randrange(5,20)):
                    glass(random.randrange(100,701),random.randrange(100,701),glasses)
            if floor == 3:
                pygame.mixer.music.load("floor3music.mp3")
                pygame.mixer.music.play(-1)
                for g in glasses:
                    g.kill()
                for b in bullets:
                    b.kill()
            bossfighting=False
            boss.kill()
        elif floor == 1:
            boss_collide=pygame.sprite.collide_rect(boss,player)
            boss_got_hit=pygame.sprite.spritecollide(boss,bullets,True)
            for i in range(len(boss_got_hit)):
                boss.health-=random.randrange(1,15)
                explode_sound.play()
            if boss_collide:
                player.got_hit(player.maxhealth*1/25)
                plustime+=3
            if plustime>0:
                plustime-=1
                force_plus=1.5
            else:
                force_plus=1
            dx=boss.x-player.x
            dy=boss.y-player.y
            distance=(dx**2+dy**2)**0.5
            player.x+=dx/distance*3*force_plus
            player.y+=dy/distance*3*force_plus
        elif floor == 2:
            boss_collide=pygame.sprite.collide_rect(boss,player)
            boss_got_hit=pygame.sprite.spritecollide(boss,bullets,True)
            player_got_hit=pygame.sprite.spritecollide(player,bossbullets,True)
            for i in range(len(player_got_hit)):
                player.health-=player.maxhealth*1/15
                explode_sound.play()
            for i in range(len(boss_got_hit)):
                boss.health-=random.randrange(10,35)
                EnemyBullet(bossbullets,boss.x+50,boss.y+50,player.x,player.y)
                shot_sound.play()
                explode_sound.play()
            for bullet in bossbullets:
                bullet.update()
            if boss_collide:
                player.got_hit(player.maxhealth*1/50)
        elif floor == 3:
            boss_collide=pygame.sprite.collide_rect(boss,player)
            boss_got_hit=pygame.sprite.spritecollide(boss,bullets,True)
            player_got_hit=pygame.sprite.spritecollide(player,bossbullets,True)
            for i in range(len(player_got_hit)):
                player.health-=player.maxhealth*1/50
            if boss.shoot_clockwise:
                for target in boss.target:
                    if target[0]>=0 and target[1]==0:
                        target[0]+=25
                    if target[0]>=800 and target[1]>=0:
                        target[1]+=25
                    if target[1]==800 and target[0]<=800:
                        target[0]-=25
                    if target[0]==0 and target[1]<=800:
                        target[1]-=25
                    EnemyBullet(bossbullets,boss.x+50,boss.y+50,target[0],target[1])
                if random.randrange(1,301)==300:
                    boss.shoot_clockwise=False
            else:
                for target in boss.target:
                    if target[0]>=0 and target[1]==0:
                        target[0]-=25
                    if target[0]>=800 and target[1]>=0:
                        target[1]-=25
                    if target[1]==800 and target[0]<=800:
                        target[0]+=25
                    if target[0]==0 and target[1]<=800:
                        target[1]+=25
                    EnemyBullet(bossbullets,boss.x+50,boss.y+50,target[0],target[1])
                    shot_sound.play()
            for bullet in bossbullets:
                bullet.update() 
            for _ in range(len(boss_got_hit)):
                boss.health-=random.randrange(10,40)
            for _ in range(boss_collide):
                player.health-=player.maxhealth*1/30
    if count1==0:
        count1=random.randrange(20,60,10)
        for enemy in enemies:
            EnemyBullet(enemybullets,enemy.x+enemy.radius,enemy.y+enemy.radius,
                        player.x+player.height/2,player.y+player.width/2)
            shot_sound.play()
    else:
        count1-=1
    if floor == 2:
        for g in glasses:
            touch_glasses1=pygame.sprite.spritecollide(g,bullets,False)
            touch_glasses2=pygame.sprite.spritecollide(g,enemybullets,False) 
            for b in touch_glasses1:
                if g.face_direction == 1:
                    if b.x>=g.x-50 and b.x<=g.x and b.y>=g.y:
                        b.started_x-=(b.started_x-(g.x-25))*2
                    if b.y>=g.y-50 and b.y<=g.y and b.x>=g.x:
                        b.started_y-=(b.started_y-(g.y-25))*2
                    else:
                        if b.x-(g.x-25) >= b.y-(g.y-25):
                            b.started_x-=(b.started_x-(g.x-25))*2
                        else:
                            b.started_y-=(b.started_y-(g.y-25))*2
                if g.face_direction == 2:
                    if b.x>=g.x and b.x<=g.x+50 and b.y>=g.y:
                        b.started_x-=(b.started_x-(g.x+25))*2
                    if b.y>=g.y-5 and b.y<=g.y and b.x<=g.x:
                        b.started_y-=(b.started_y-(g.y-25))*2
                    else:
                        if b.x-(g.x+25) >= b.y-(g.y-25):
                            b.started_x-=(b.started_x-(g.x+25))*2
                        else:
                            b.started_y-=(b.started_y-(g.y-25))*2
                if g.face_direction == 3:
                    if b.x>=g.x and b.x<=g.x+50 and b.y<=g.y:
                        b.started_x -= (b.started_x-(g.x+25))
                    if b.y>=g.y and b.y<=g.y+50 and b.x<=g.x:
                        b.started_y -= (b.started_y-(g.y+25))
                    else:
                        if b.x-(g.x+25) >= b.y-(g.y+25):
                            b.started_x-=(b.started_x-(g.x+25))*2
                        else:
                            b.started_y-=(b.started_y-(g.y+25))*2
                if g.face_direction == 4:
                    if b.x>=g.x-50 and b.x<g.x and b.y<g.y:
                        b.started_x -= (b.started_x-(g.x-25))
                    if b.y>=g.y and b.y<=g.y+50 and b.x>g.x:
                        b.started_y-=(b.started_y-(g.y+25))*2
                    else:
                        if b.x-(g.x-25) >= b.y-(g.y+25):
                            b.started_x-=(b.started_x-(g.x-25))*2
                        else:
                            b.started_y-=(b.started_y-(g.y+25))*2
                Bullet(bullets,b.x,b.y,b.started_x,b.started_y) 
                b.kill()    
            for b in touch_glasses2:
                if g.face_direction == 1:
                    if b.x>=g.x-50 and b.x<=g.x and b.y>=g.y:
                        b.started_x-=(b.started_x-(g.x-25))*2
                    if b.y>=g.y-50 and b.y<=g.y and b.x>=g.x:
                        b.started_y-=(b.started_y-(g.y-25))*2
                    else:
                        if b.x-(g.x-25) >= b.y-(g.y-25):
                            b.started_x-=(b.started_x-(g.x-25))*2
                        else:
                            b.started_y-=(b.started_y-(g.y-25))*2
                if g.face_direction == 2:
                    if b.x>=g.x and b.x<=g.x+50 and b.y>=g.y:
                        b.started_x-=(b.started_x-(g.x+25))*2
                    if b.y>=g.y-5 and b.y<=g.y and b.x<=g.x:
                        b.started_y-=(b.started_y-(g.y-25))*2
                    else:
                        if b.x-(g.x+25) >= b.y-(g.y-25):
                            b.started_x-=(b.started_x-(g.x+25))*2
                        else:
                            b.started_y-=(b.started_y-(g.y-25))*2
                if g.face_direction == 3:
                    if b.x>=g.x and b.x<=g.x+50 and b.y<=g.y:
                        b.started_x -= (b.started_x-(g.x+25))
                    if b.y>=g.y and b.y<=g.y+50 and b.x<=g.x:
                        b.started_y -= (b.started_y-(g.y+25))
                    else:
                        if b.x-(g.x+25) >= b.y-(g.y+25):
                            b.started_x-=(b.started_x-(g.x+25))*2
                        else:
                            b.started_y-=(b.started_y-(g.y+25))*2
                if g.face_direction == 4:
                    if b.x>=g.x-50 and b.x<g.x and b.y<g.y:
                        b.started_x -= (b.started_x-(g.x-25))
                    if b.y>=g.y and b.y<=g.y+50 and b.x>g.x:
                        b.started_y-=(b.started_y-(g.y+25))*2
                    else:
                        if b.x-(g.x-25) >= b.y-(g.y+25):
                            b.started_x-=(b.started_x-(g.x-25))*2
                        else:
                            b.started_y-=(b.started_y-(g.y+25))*2
                EnemyBullet(enemybullets,b.x,b.y,b.started_x,b.started_y) 
                b.kill()     
            g.update()
    player.update()
    dieenemy=pygame.sprite.spritecollide(player,enemies,False)
    dieenemy+=pygame.sprite.groupcollide(enemies,bullets,False,True)
    pygame.sprite.groupcollide(enemybullets,bullets,True,True)
    got_hit_times=pygame.sprite.spritecollide(player,enemybullets,True)
    for d in dieenemy:
        explode_sound.play()
        if d.isdieing == False:
            d.isdieing=True
            enemy_dead+=1
            skill2.colling-=20
            if skill2.colling<=0:
                skill2.colling=0
    for i in range(len(got_hit_times)):
        player.got_hit(random.randrange(10,100,5))
        explode_sound.play()
    if enemy_dead>=[35,50,120,10000000,10000000000000][floor-1]:
        enemy_dead=0
        bossfighting=True
        for enemy in enemies:
            enemy.kill()
        boss=Boss()
    if click[0]==1 or click[2]==1:
        shot_sound.play()
        window.blit(front_sight2,(mouse[0]-32,mouse[1]-32))
        Bullet(bullets,player.x+player.height/2,player.y+player.width/2,mouse[0],mouse[1])
    else:
        window.blit(front_sight1,(mouse[0]-32,mouse[1]-32))
    skill1.update()
    skill2.update()
    skill3.update()
    pygame.display.update()

def game():
    set_up()
    for _ in range(5):
        Enemy(enemies) 
    while not gamequit:
        pygame.time.Clock().tick(20)
        control()
        play()
    pygame.quit()
    quit()

if __name__ == '__main__':
    menu()
