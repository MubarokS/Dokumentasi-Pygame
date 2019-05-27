__author__ = 'Mubarok'

#MENGIMPOR LIBRARY
import pygame
import random

#MENDEFENISIKAN WARNA DAN
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# BERFUNGSI UNTUK MENDEFENISIKAN TEXT
font_name=pygame.font.match_font('arial black')
def draw_text(surf, text,size, x, y):
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,WHITE)
    text_rect=text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

#BERFUNGSI UNTUK MENDEFENISIKAN SHIELD PLAYER
def draw_shield(surf, x, y, pct):
    if pct<0:
        pct=0
    Bar_Lenght=100
    Bar_Height=10
    fill=(pct/100)*Bar_Lenght
    outline_rect=pygame.Rect(x, y, Bar_Lenght, Bar_Height)
    fill_rect=pygame.Rect(x,y,fill,Bar_Height)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect,2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([5, 5])
        self.image=pygame.image.load("assets/player.png").convert()
        self.image=pygame.transform.scale(self.image,(100,100))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.vx=0
        self.vy=0
        self.shield=100
        self.shoot_delay=250
        self.last_shoot=pygame.time.get_ticks()

    def update(self):
        self.vx=0
        self.vy=0

        keys= pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.vx = -7
        if keys[pygame.K_DOWN]:
            self.vy = +7
        if keys[pygame.K_LCTRL]:
            self.shoot()
        self.rect.y += self.vx
        self.rect.y += self.vy

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            bullet = Bullet()
            bullet.rect.x = player.rect.x - 40
            bullet.rect.y = player.rect.y + 40
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)
            shoot_sound.play()


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([10, 14])
        self.image=pygame.image.load("assets/peluru.png")
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.x -=5

class Pow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(['shield'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y=random.randrange(screen_width - self.rect.y)
        self.rect.x=random.randrange(-50,-40)
        self.speedy = 5

    def update(self):
        self.rect.x += self.speedy
        if self.rect.x > screen_width:
            self.rect.y=random.randrange(screen_width - self.rect.y)
            self.rect.x=random.randrange(-50,-40)
            self.speedy = 5

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface([30,40])
        self.image=pygame.image.load("assets/musuh.png")
        self.rect = self.image.get_rect()
        self.rect.y=random.randrange(screen_width - self.rect.y)
        self.rect.x=random.randrange(-50,-40)
        self.speedy=random.randrange(7,11)

    def update(self):
        self.rect.x += self.speedy
        if self.rect.x > screen_width:
            self.rect.y=random.randrange(screen_width - self.rect.y)
            self.rect.x=random.randrange(-50,-40)
            self.speedy=random.randrange(7,11)

#MENAMPILKAN SCREEN AWAL DAN GAME OVER SCREEN
def show_game_over_screen():
    draw_text(screen,"DODGE  AND FIRE !",64,screen_width/2,screen_height/4)
    draw_text(screen," ",22,screen_width/2,screen_height/2)
    draw_text(screen,"PRESS ANY KEY TO CONTINUE",18,screen_width/2,screen_height * 3/ 4)
    pygame.display.flip()
    waiting=True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting=False

#VARIABEL FPS
FPS = 60

#INISIALISASI LIBRARY PYGAME
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("DODGE AND FIRE")#MENAMPILKAN JUDUL PADA JENDELA GUI
pygame.mixer.music.load("audio/backsound.ogg")#MENGAKSES ASSETS BERUPA MUSIK
pygame.mixer_music.get_volume()
pygame.mixer.music.set_volume(0.4)#MENSETTING VOLUME BACKSOUND
shoot_sound=pygame.mixer.Sound("audio/shoot.wav")#MENGAKSES ASSETS BERUPA MUSIK SAAT PELURU KELUAR
ledakan_sound=pygame.mixer.Sound("audio/Explosion.wav")#MENGAKSES ASSETS BERUPA MUSIK SAAT LEDAKAN

#MENDEFINISKAN PANJANG DAN LEBAR JENDELA GUI
screen_width = 1280
screen_height = 640
screen = pygame.display.set_mode([screen_width, screen_height])

#MENDEFENISIKAN NYAWA TAMBAHAN
powerup_images = {}
powerup_images['shield'] = pygame.image.load("assets/shield_gold.png").convert()

#VARIABEL GLOBAL BAGI GAME
all_sprites_list = pygame.sprite.Group()
mobs=pygame.sprite.Group()
powerups=pygame.sprite.Group()
block_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
game_over=True
running = True
clock = pygame.time.Clock()

#VARIABEL PLAYER YANG MENGAKSES CLASS PLAYER
player = Player()
all_sprites_list.add(player)
for i in range(8):
    m=Enemy()
    all_sprites_list.add(m)
    mobs.add(m)
score = 0
player.rect.y = 300
player.rect.x = 1100

#MENGAKSES GAMBAR BACKGROUND AGAR DAPAT DITAMPILKAN PADA JENDELA GAME
bacground=pygame.image.load("assets/background.png").convert()
bacground_rect=bacground.get_rect()



pygame.mixer.music.play(loops=-1)

# -------- Main Program Loop ----------- #
while running:
    if game_over:
        show_game_over_screen()
        game_over = False
        all_sprites_list = pygame.sprite.Group()
        mobs=pygame.sprite.Group()
        block_list = pygame.sprite.Group()
        bullet_list = pygame.sprite.Group()
        player = Player()
        all_sprites_list.add(player)
        player.rect.y = 300
        player.rect.x = 1100
        for i in range(8):
            m=Enemy()
            all_sprites_list.add(m)
            mobs.add(m)
        score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites_list.update()
    hits=pygame.sprite.groupcollide(mobs,bullet_list,True,True)
    for hit in hits:
        m = Enemy()
        ledakan_sound.play()
        score += 1
        all_sprites_list.add(m)
        if random.random() > 0.9:
            pow = Pow()
            all_sprites_list.add(pow)
            powerups.add(pow)
        mobs.add(m)

    hits=pygame.sprite.spritecollide(player,mobs,True)
    if hits:
        player.shield -=20
        if player.shield <=0:
            game_over=True

    for bullet in bullet_list:
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(score)

        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

    medic = pygame.sprite.spritecollide(player, powerups, True)
    for hit in medic:
        if hit.type == 'shield':
            player.shield += 20
            if player.shield >= 100:
                player.shield = 100

    screen.blit(bacground,bacground_rect)
    all_sprites_list.draw(screen)
    draw_text(screen,str(score),30, screen_width/2,10)
    draw_shield(screen,10,10,player.shield)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
