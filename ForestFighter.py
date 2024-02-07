import pygame
import random as rd
from sys import exit

class Slime(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.walk_ani = [pygame.image.load(f'Assets/Player/Run/Run{i}.png').convert_alpha() for i in range(7)]
        self.walk_index = 0
        self.jump_ani = [pygame.image.load(f'Assets/Player/Jump/Jump{i}.png').convert_alpha() for i in range(8)]
        self.jump_index = 0
        self.image = self.walk_ani[self.walk_index]
        self.rect = self.image.get_rect(midbottom = (50, 75))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound(f"Sfx/JumpSound.wav")
        self.jump_sound.set_volume(0.15)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 350:
           self.gravity = -18
           if sound_state == soundon_surf:
               self.jump_sound.play()
    
    def slime_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 375:
            self.rect.bottom = 375

    def run_animation(self):
        if self.rect.y < 300:
            self.jump_animation()
        else:
            self.walk_index += 0.15
            if self.walk_index > 6:
                self.walk_index = 1
            self.image = self.walk_ani[int(self.walk_index)]
            self.rect.y = self.rect.y + self.rect.height - self.image.get_height()
    
    def jump_animation(self):
        self.jump_index += 0.15
        if self.jump_index > 7:
            self.jump_index = 0
        self.image = self.jump_ani[int(self.jump_index)]

    def update(self):
        self.player_input()
        self.slime_gravity()
        self.run_animation()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "rat":
            self.frames = [pygame.image.load(f'Assets/Rat/RatWalk{i}.png').convert_alpha() for i in range(3)]
            y_pos = 373
        else:
            self.frames = [pygame.image.load(f"Assets/Bird/BirdWalk{i}.png").convert_alpha()for i in range(5)]
            y_pos = rd.randint(225, 360)
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(rd.randint(900, 1200), y_pos))

    def obs_animation(self):
        self.animation_index += 0.08 + (user_score * 0.001)
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.obs_animation()
        self.rect.x -= 5.7 + user_score*0.1
        if self.rect.x < -100:
            self.kill()

def collision():
    return not pygame.sprite.spritecollide(player.sprite, obstacles_group, False)

def display_score():
    curr_time = pygame.time.get_ticks()//1000 - default_time
    scorefont = pygame.font.Font("Fonts/ThaleahFat.ttf", 25)
    scorefont_surface = scorefont.render(f'Your Score: {curr_time}', False, 'black')
    screen.blit(scorefont_surface, (5,5))
    return curr_time

def skele_ani():
    global skele_surf, skele_index, skele_y, move_dir

    skele_index += 0.15
    if skele_index >= 4:
        skele_index = 0
    skele_surf = skele_image[int(skele_index)]
    screen.blit(skele_surf, (370, skele_y))
    skele_y += move_dir * 0.95
    if skele_y <= 20:
        move_dir = 0.60
    elif skele_y >= 60:
        move_dir = -0.90
    
def save_hs(score):
    with open("Save/hs.txt", 'a') as file:
        file.write(str(score)+'\n')

def load_highscores():
    try:
        with open("Save/hs.txt", 'r') as file:
            highscores = [int(line.strip()) for line in file]
            return max(highscores)
    except FileNotFoundError:
        return "Corrupt File"
    
def cloud_spawn(cloud_list):
    for cloud in cloud_list:
        cloud.x -= 2
        screen.blit(cloud_frame, cloud)
    cloud_list = [cloud for cloud in cloud_list if cloud.x > -100]

pygame.init()
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Forest Fighter Beta")
clock = pygame.time.Clock()
default_time = 0

MAIN_MENU = 0
ABOUT = 1
PLAYING = 2
GAME_OVER = 3
ABOUT_PAGE = 4
game_state = MAIN_MENU
player_alive = False

startgame_hover, about_hover, exit_hover, quit_hover, restart_hover, mainmenu_hover = False, False, False, False, False, False
mouse_pos = pygame.mouse.get_pos()

sky_bg = pygame.image.load("Assets/Surfaces/BlueSky_bg.png").convert_alpha()
dirt_bg = pygame.image.load("Assets/Surfaces/dirt.png").convert_alpha()
dirt_x = 0

gameover_sound = pygame.mixer.Sound("Sfx/gameover_sound.wav")
gameover_sound.set_volume(0.1)
game_over = pygame.image.load(f'Assets/Surfaces/game_over1.jpg').convert_alpha()
gameover_played = False

player = pygame.sprite.GroupSingle()
player.add(Slime())

start_font = pygame.font.Font("Fonts/ThaleahFat.ttf", 105)
start_font0 = pygame.font.Font("Fonts/ThaleahFat.ttf", 106)
startfont_surface0 = start_font.render("Forest Fighter", True, 'black')
startfont_surface = start_font.render("Forest Fighter", True, 'green4')
startfont_ypos = 40
title_move_direction = 1

clouds = [pygame.image.load(f"Assets/Clouds/CloudShape{i}.png").convert_alpha() for i in range(3)]
clouds_index = 0
cloud_frame = clouds[clouds_index]
cloud_list = []

sun_bg = pygame.image.load("Assets/Surfaces/Sun.png").convert_alpha()
forest_bg = pygame.image.load("Assets/Surfaces/ForestFix.png").convert_alpha()
forest_bg = pygame.transform.scale(forest_bg, (800, 500))
forest_x = 0

soundon_surf = pygame.image.load("Assets/More/soundon.png").convert_alpha()
soundon_rect = soundon_surf.get_rect(topleft=(15, 35))
soundmute_surf = pygame.image.load("Assets/More/soundmute.png").convert_alpha()
sound_state = soundon_surf
bg_music = pygame.mixer.Sound('Sfx/MainSound_bg.mp3')
bg_music.play(loops=-1)

about_info = pygame.image.load("Assets/Surfaces/About.png").convert_alpha()
aboutinfo_rect = about_info.get_rect(midtop=(400, 20))

attack_img = pygame.image.load("Assets/Player/Attack/Attack.png").convert_alpha()
rat_img = pygame.image.load("Assets/Rat/RatWalk0.png").convert_alpha()
bird_img = pygame.image.load("Assets/Bird/Birdwalk1.png").convert_alpha()
skele_image = [pygame.image.load(f"Assets/Skull/skull{i}.png").convert_alpha() for i in range(5)]
move_dir, skele_index, skele_y = 1, 0, 0
skele_surf = skele_image[skele_index]

obstacles_group = pygame.sprite.Group()
obstacle_rate = int(900 - pygame.time.get_ticks()//1000 * 0.1)
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, obstacle_rate)

CLOUD_UPDATE_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(CLOUD_UPDATE_EVENT, 1000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif game_state == MAIN_MENU:
            if event.type == pygame.MOUSEBUTTONDOWN and startgame_hover:
                player_alive = True
                default_time = pygame.time.get_ticks() // 1000
                game_state = PLAYING
            elif event.type == pygame.MOUSEBUTTONDOWN and about_hover:
                game_state = ABOUT_PAGE
            elif event.type == pygame.MOUSEBUTTONDOWN and exit_hover:
                pygame.quit()
                exit()
        elif game_state == GAME_OVER:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_hover:
                    gameover_sound.stop()
                    player_alive = True
                    default_time = pygame.time.get_ticks() // 1000
                    player.sprite.rect.midbottom = (40, 377)
                    bg_music.play(loops=-1)
                    sound_state = soundon_surf
                    skele_y = 0
                    game_state = PLAYING
                elif mainmenu_hover:
                    gameover_sound.stop()
                    sound_state = soundon_surf
                    game_state = MAIN_MENU
                    bg_music.play(loops=-1)
                elif quit_hover:
                    pygame.quit()
                    exit()

        elif game_state == PLAYING and player_alive:
            if event.type == pygame.MOUSEBUTTONDOWN and soundon_rect.collidepoint(event.pos):
                if sound_state == soundon_surf:
                    sound_state = soundmute_surf
                    bg_music.stop()
                else:
                    sound_state = soundon_surf
                    bg_music.play(loops=-1)

            if event.type == obstacle_timer:
                obstacles_group.add(Obstacles(rd.choice(['rat', 'bird', 'rat', 'bird', 'rat'])))
            elif event.type == CLOUD_UPDATE_EVENT:
                cloud_list.append(clouds[rd.randint(0,2)].get_rect(midbottom=(rd.randint(800, 1000), rd.randint(0, 350))))
            
    if game_state == MAIN_MENU:
        version = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 10)
        version_surf = version.render("Beta Version", False, "white")
        creator = version.render("Created by Arzaka", False, "white")

        mainmenu_blits = [(sky_bg, (0, 0)), (sun_bg, (490, -190)), (forest_bg, (0,-100)), (dirt_bg, (0, 375)), (startfont_surface0, (70, startfont_ypos)), (startfont_surface, (80, startfont_ypos)), (version_surf, (685, 470)), (creator, (670, 485))]
        screen.blits(mainmenu_blits)

        startfont_ypos += title_move_direction * 0.95
        if startfont_ypos <= 65:
            title_move_direction = 0.80
        elif startfont_ypos >= 100:
            title_move_direction = -1.15

        startgame_font = pygame.font.Font("Fonts/ThaleahFat.ttf", 50)
        startgame_font0 = pygame.font.Font("Fonts/ThaleahFat.ttf", 50)
        startgame_surface = startgame_font.render("Start Game", False, "green4")
        startgame_surface0 = startgame_font0.render("Start Game", False, "black")
        startgame_rect = startgame_surface.get_rect(center=(400,250))
        startgame_rect1 = startgame_surface0.get_rect(center=(395,250))

        about_font = pygame.font.Font("Fonts/ThaleahFat.ttf", 50)
        about_font0 = pygame.font.Font("Fonts/ThaleahFat.ttf", 50)
        about_surface = about_font.render("About", False, "green4")
        about_surface0 = about_font0.render("About", False, "black")
        about_rect = startgame_surface.get_rect(center=(450,350))
        about_rect0 = startgame_surface0.get_rect(center=(445,350))

        exit_font = pygame.font.Font("Fonts/ThaleahFat.ttf", 50)
        exit_font0 = pygame.font.Font("Fonts/ThaleahFat.ttf", 50)
        exit_surface = exit_font.render("Quit", False, "green4")
        exit_surface0 = exit_font0.render("Quit", False, "black")
        exit_rect = exit_surface.get_rect(center=(390, 450))
        exit_rect0 = exit_surface0.get_rect(center=(385, 450))

        mouse_pos = pygame.mouse.get_pos()
        if startgame_rect.collidepoint(mouse_pos):
            startfont = "white"
            startgame_surface = startgame_font.render("Start Game", False, startfont)
            startgame_surface = pygame.transform.scale(startgame_surface, (int(startgame_surface.get_width() * 1.1), int(startgame_surface.get_height() * 1.1)))
            startgame_rect = startgame_surface.get_rect(center=startgame_rect.center)
            startgame_hover = True
        else:
            startgame_hover = False
        
        if about_rect.collidepoint(mouse_pos): 
            startfont = "white"
            about_surface = about_font.render("About", False, startfont)
            about_surface = pygame.transform.scale(about_surface, (int(about_surface.get_width() * 1.1), int(about_surface.get_height() * 1.1)))
            about_rect = about_surface.get_rect(center=(395, 350))
            about_hover = True
        else:
            about_hover = False
        
        if exit_rect.collidepoint(mouse_pos):
            startfont = "white"
            exit_surface = exit_font.render("QUIT", False, startfont)
            exit_surface = pygame.transform.scale(exit_surface, (int(exit_surface.get_width() * 1.11), int(exit_surface.get_height() * 1.11)))
            exit_rect = exit_surface.get_rect(center=(390, 450))
            exit_hover = True
        else:
            exit_hover = False
        
        mainmenu_blits0 = [(startgame_surface0, (startgame_rect1)), (startgame_surface, (startgame_rect)), (about_surface0, (about_rect0)), (about_surface, (about_rect)), (exit_surface0, (exit_rect0)), (exit_surface, (exit_rect))]
        for surf, rec in mainmenu_blits0:
            screen.blit(surf, rec)

    elif game_state == ABOUT_PAGE:
        adventurer = pygame.image.load("Assets/More/adventurer.png").convert_alpha()
        about_data = [(sky_bg, (0, 0)), (sun_bg, (490, -190)), (forest_bg, (0,-100)), (dirt_bg, (0, 375)), (about_info, aboutinfo_rect), (adventurer, (510, 85))]
        for bg, pos in about_data:
            screen.blit(bg, pos)

        about_font = pygame.font.Font("Fonts/ThaleahFat.ttf", 45)
        about_font_surface = about_font.render("Forest Fighter", False, "white")
        about_font_bg = pygame.font.Font("Fonts/ThaleahFat.ttf", 45)
        about_font_surface_bg = about_font_bg.render("Forest Fighter", False, "black")
        about_font_rect_bg = about_font_surface_bg.get_rect(midtop=(325, 74))
        about_font_rect = about_font_surface.get_rect(midtop=(330, 75))
        story_font = pygame.font.Font("Fonts/ThaleahFat.ttf", 25)

        story_data = [("Once upon a time...", (150, 120)), ("there's a soldier named Andy", (160, 150)), ("Andy fought in the woods and got cursed", (160, 180)), ("He got cursed by a wizard into a slime", (160, 210)),
                      ("He wants a revenge, but its not that easy..", (160, 240)), ("So, do you want to help Andy", (160, 300)), ("to get his revenge???", (160, 330))]
        
        for words, pos in story_data:
            story_surf = story_font.render(words, False, "white")
            screen.blit(story_surf, pos)
    
        story_font0 = pygame.font.Font("Fonts/ThaleahFat.ttf", 30)
        story_surf7 = story_font0.render("Lets fight!", False, 'red')
        screen.blit(story_surf7, (180, 375))

        about_data0 = [(attack_img, (350, 380)), (rat_img, (500, 410)), (bird_img, (570, 375)), (about_font_surface_bg, about_font_rect_bg), (about_font_surface, about_font_rect)]
        for bg, pos in about_data0:
            screen.blit(bg, pos)

        back = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 25)
        back_surf = version.render("Press SPACE to back", False, "white")
        screen.blit(back_surf, (520, 475))

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            game_state = MAIN_MENU

    elif game_state == PLAYING:
        screen.blit(sky_bg, (0, 0))
        screen.blit(sun_bg, (490, -190))
        cloud_spawn(cloud_list)

        user_score = display_score()
        screen.blit(forest_bg, (forest_x,-100))
        screen.blit(forest_bg, (forest_x + forest_bg.get_width(), -100))
        forest_x -= 3 + user_score * 0.08
        if abs(forest_x) >= forest_bg.get_width():
            forest_x = 0

        screen.blit(dirt_bg, (dirt_x, 375))
        screen.blit(dirt_bg, (dirt_x+dirt_bg.get_width(), 375))
        dirt_x -= 5 + user_score * 0.08
        if abs(dirt_x) >= dirt_bg.get_width():
            dirt_x = 0
        screen.blit(sound_state, soundon_rect)

        player.draw(screen)
        player.update()
        obstacles_group.draw(screen)
        obstacles_group.update()

        if collision() == False:
            save_hs(user_score)
            game_state = GAME_OVER
            obstacles_group.empty()
            player_alive = False
            gameover_played = False

    elif game_state == GAME_OVER:
        mouse_pos = pygame.mouse.get_pos()
        if not gameover_played:
            bg_music.stop()
            gameover_sound.play()
            gameover_played = True

        screen.blit(game_over, (0,0))
        skele_ani()

        gameover_font = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 30)
        gameover_surf = gameover_font.render('Game Over!', False, "white")
        score_font = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 35)
        scorefont_surface = score_font.render(f"Your Score: {user_score}", False, 'black')
        scorefont_rect = scorefont_surface.get_rect(center=(400, 220))
        highscore_font = pygame.font.Font("Fonts/PixeloidSans-Bold.ttf", 20)
        highscore_surface = highscore_font.render(f"Your highscore: {load_highscores()}", False, 'black')
        highscore_rect = highscore_surface.get_rect(center = (400, 270))

        screen.blit(gameover_surf, (300, 130))
        screen.blit(scorefont_surface, scorefont_rect)
        screen.blit(highscore_surface, highscore_rect)

        restart_font = pygame.font.Font("Fonts/ThaleahFat.ttf", 50)
        restart_surf = restart_font.render("Restart", False, "green4")
        restart_rect = restart_surf.get_rect(center=(410, 325))
        restart_font0 = pygame.font.Font("Fonts/ThaleahFat.ttf", 50)
        restart_surf0 = restart_font0.render("Restart", False, "black")
        restart_rect0 = restart_surf0.get_rect(center=(405, 325))

        if restart_rect.collidepoint(mouse_pos):
            restart_hover = True
            restart_surf = restart_font.render("Restart", False, "white")
            restart_surf = pygame.transform.scale(restart_surf, (int(restart_surf.get_width()*1.1), int(restart_surf.get_height()*1.1)))
            restart_rect = restart_surf.get_rect(center=(405, 325))
        else:
            restart_hover = False

        mainmenu_font = pygame.font.Font("Fonts/Thaleahfat.ttf", 50)
        mainmenu_surf = mainmenu_font.render("Main Menu", False, "green4")
        mainmenu_rect = mainmenu_surf.get_rect(center=(280, 370))
        mainmenu0_font = pygame.font.Font("Fonts/ThaleahFat.ttf", 50)
        mainmenu0_surf = mainmenu0_font.render("Main Menu", False, "black")
        mainmenu0_rect = mainmenu0_surf.get_rect(center=(275, 370))

        if mainmenu_rect.collidepoint(mouse_pos):
            mainmenu_hover = True
            mainmenu_surf = mainmenu_font.render("Main Menu", False, "white")
            mainmenu_surf = pygame.transform.scale(mainmenu_surf, (int(mainmenu_surf.get_width()*1.1), int(mainmenu_surf.get_height()*1.1)))
            mainmenu_rect = mainmenu_surf.get_rect(center=(275, 370))
        else:
            mainmenu_hover = False

        quit_font = pygame.font.Font("Fonts/Thaleahfat.ttf", 50)
        quit_surf = quit_font.render("Quit Game", False, "green4")
        quit_rect = quit_surf.get_rect(center=(525, 370))
        quit0_font = pygame.font.Font("Fonts/Thaleahfat.ttf", 50)
        quit0_surf = quit0_font.render("Quit Game", False, "black")
        quit0_rect = quit0_surf.get_rect(center=(520, 370))

        if quit_rect.collidepoint(mouse_pos):
            quit_hover = True
            quit_surf = quit_font.render("Quit Game", False, "white")
            quit_surf = pygame.transform.scale(quit_surf, (int(quit_surf.get_width()*1.1), int(quit_surf.get_height()*1.1)))
            quit_rect = quit_surf.get_rect(center=(520, 370))
        else:
            quit_hover = False

        gameover_blits = [(restart_surf0, restart_rect0), (restart_surf, restart_rect), (mainmenu0_surf, mainmenu0_rect), (mainmenu_surf, mainmenu_rect), (quit0_surf, quit0_rect), (quit_surf, quit_rect)]
        for surf, rec in gameover_blits:
            screen.blit(surf, rec)

    pygame.display.update()
    clock.tick(60)