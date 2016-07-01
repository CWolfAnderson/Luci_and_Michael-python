"""Main module for Luci & Michael

    Christoph Anderson

    HowTo:
        For Lucifer:
            Use "W", "A", "S", and "D" to move up, left, down, & right respectively
            Use "J", "K", "L", and ";" to shoot left, up, down, & right respectively
        For Michael:
            Use "UP", "DOWN", "LEFT", and "RIGHT" to move up, left, down, & right respectively
            Use (on the number pad) "6", "3", "2", and "enter" to shoot left, up, down, & right respectively

        Collect weapons and upgrades
        Deplete your opponent's health before they deplete yours

    Run the program from the command line:
        $ python main.py

    Additional Files:

    Attribute(s):
        Globals:
            all_sprite_list
            wall_list
            powerups
            lucis_shots
            michaels_shots
            luci_group
            michael_group
            screen_width
            screen_height
            luci
            michael
            time_since_last_powerup
            luci_shot_sounds
            michael_shot_sounds
            played_death_music

        FPS (int): frames per second
        fpsClock (clock object): clock
        windowSize (tuple): size of the screen (or 0,0 for full-screen)
        screen (Pygame display): main screen being displayed

"""

import random
import sys

import pygame
from pygame.locals import *
from time import time as cTime

from Shot import Shot
from Character import Character
from Powerup import Powerup
from Wall import Wall
from Rock import Rock

all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
powerups = pygame.sprite.Group()
lucis_shots = pygame.sprite.Group()
michaels_shots = pygame.sprite.Group()
luci_group = pygame.sprite.Group()
michael_group = pygame.sprite.Group()

screen_width = 0
screen_height = 0

luci = "Luci"
michael = "Michael"

time_since_last_powerup = 0

# sounds
luci_shot_sounds = []
michael_shot_sounds = []

played_death_music = False

def main():
    """
    main function
    """

    pygame.init()

    joystick.init()  # Allow joystick support

    # Joystick controller
    jController = None

    # If there is a joystick, initialize with JoystickController
    jCount = joystick.get_count()
    if jCount > 0:
        joysticks = [joystick.Joystick(i) for i in range(jCount)]
        joysticks[0].init()  # Default to first joystick
        jController = JoystickController(joysticks[0], 0.5)

    else:
        joystick.quit()  # Deinit joystick module

    global all_sprite_list
    global wall_list
    global screen_width
    global screen_height
    global luci
    global michael
    global time_since_last_powerup
    global lucis_shots
    global michaels_shots
    global luci_group
    global michael_group
    global luci_shot_sounds
    global michael_shot_sounds
    global played_death_music

    luci_shot_sounds.append(pygame.mixer.Sound("res/sounds/luci_shot1.ogg"))
    luci_shot_sounds.append(pygame.mixer.Sound("res/sounds/luci_shot2.ogg"))
    michael_shot_sounds.append(pygame.mixer.Sound("res/sounds/michael_shot1.ogg"))
    michael_shot_sounds.append(pygame.mixer.Sound("res/sounds/michael_shot2.ogg"))

    hurt_sounds = []
    hurt_sounds.append(pygame.mixer.Sound("res/sounds/hurt_sound1.ogg"))
    hurt_sounds.append(pygame.mixer.Sound("res/sounds/hurt_sound2.ogg"))

    FPS = 60
    fpsClock = pygame.time.Clock()

    window_size = (0, 0)
    # window_size = (1200, 800) # if (0, 0) is wonky
    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

    screen_width = pygame.display.Info().current_w
    screen_height = pygame.display.Info().current_h

    pygame.display.set_caption("Luci & Michael")

    RED = pygame.Color(200, 0, 0)
    WHITE = pygame.Color(204, 204, 204)

    screen.fill(RED)

    # reset the game
    reset_game(screen)

    # display the intro screen
    game_intro(screen)

    luci_move_up = False
    luci_move_down = False
    luci_move_left = False
    luci_move_right = False
    michael_move_up = False
    michael_move_down = False
    michael_move_left = False
    michael_move_right = False

    while True:

        for event in pygame.event.get():

            show_random_powerup(time_since_last_powerup, all_sprite_list, powerups, luci, michael)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYUP:
                # luci stop moving
                if event.key == K_w:
                    luci_move_up = False
                if event.key == K_s:
                    luci_move_down = False
                if event.key == K_a:
                    luci_move_left = False
                if event.key == K_d:
                    luci_move_right = False

                # michael stop moving
                if event.key == K_UP:
                    michael_move_up = False
                if event.key == K_DOWN:
                    michael_move_down = False
                if event.key == K_LEFT:
                    michael_move_left = False
                if event.key == K_RIGHT:
                    michael_move_right = False

            if event.type == pygame.KEYDOWN:

                # game reset
                if event.key == K_ESCAPE:
                    game_intro(screen)
                    reset_game(screen)

                # game pause
                if event.key == K_SPACE:
                    game_intro(screen)

                # keydown for luci
                if event.key == K_w:
                    luci_move_up = True
                if event.key == K_s:
                    luci_move_down = True
                if event.key == K_a:
                    luci_move_left = True
                if event.key == K_d:
                    luci_move_right = True

                # keydown for michael
                if event.key == K_UP:
                    michael_move_up = True
                if event.key == K_DOWN:
                    michael_move_down = True
                if event.key == K_LEFT:
                    michael_move_left = True
                if event.key == K_RIGHT:
                    michael_move_right = True

                # luci shoot
                if event.key == K_i:
                    luci.face_up()
                    if can_shoot(luci):
                        shoot(luci, all_sprite_list, lucis_shots)
                elif event.key == K_k:
                    luci.face_down()
                    if can_shoot(luci):
                        shoot(luci, all_sprite_list, lucis_shots)
                elif event.key == K_j:
                    luci.face_left()
                    if can_shoot(luci):
                        shoot(luci, all_sprite_list, lucis_shots)
                elif event.key == K_l:
                    luci.face_right()
                    if can_shoot(luci):
                        shoot(luci, all_sprite_list, lucis_shots)

                # michael shoot
                if event.key == K_KP6:
                    michael.face_up()
                    if can_shoot(michael):
                        shoot(michael, all_sprite_list, michaels_shots)
                elif event.key == K_KP3:
                    michael.face_down()
                    if can_shoot(michael):
                        shoot(michael, all_sprite_list, michaels_shots)
                elif event.key == K_KP2:
                    michael.face_left()
                    if can_shoot(michael):
                        shoot(michael, all_sprite_list, michaels_shots)
                elif event.key == K_KP_ENTER:
                    michael.face_right()
                    if can_shoot(michael):
                        shoot(michael, all_sprite_list, michaels_shots)

                # check if a player is dead
                if luci.is_dead or michael.is_dead:
                    # allow the game to restart by pressing space bar
                    if event.key == K_SPACE:
                        # display the intro screen
                        game_intro(screen)
                        reset_game(screen)

        # lucy move
        if luci_move_up:
            luci.go_up()
        if luci_move_down:
            luci.go_down()
        if luci_move_left:
            luci.go_left()
        if luci_move_right:
            luci.go_right()

        # michael move
        if michael_move_up:
            michael.go_up()
        if michael_move_down:
            michael.go_down()
        if michael_move_left:
            michael.go_left()
        if michael_move_right:
            michael.go_right()


        # calculate mechanics for each luci shot
        for shot in lucis_shots:

            # see if it hit a wall
            wall_hit_list = pygame.sprite.spritecollide(shot, wall_list, False)

            # for each wall hit, remove the shot
            for hit in wall_hit_list:
                lucis_shots.remove(shot)
                all_sprite_list.remove(shot)

            # see if it hit michael
            enemy_hit_list = pygame.sprite.spritecollide(shot, michael_group, False)

            # for each player hit, remove the projectile
            for hit in enemy_hit_list:
                lucis_shots.remove(shot)
                all_sprite_list.remove(shot)
                michael.decrease_hp(luci.damage)
                # play sound
                hurt_sounds[random.randint(0, 1)].play()

        # calculate mechanics for each michael shot
        for shot in michaels_shots:

            # see if it hit a wall
            wall_hit_list = pygame.sprite.spritecollide(shot, wall_list, False)

            # for each wall hit, remove the shot
            for hit in wall_hit_list:
                michaels_shots.remove(shot)
                all_sprite_list.remove(shot)

            # see if it hit luci
            enemy_hit_list = pygame.sprite.spritecollide(shot, luci_group, False)

            # for each player hit, remove the projectile
            for hit in enemy_hit_list:
                michaels_shots.remove(shot)
                all_sprite_list.remove(shot)
                luci.decrease_hp(michael.damage)
                # play sound
                hurt_sounds[random.randint(0, 1)].play()

        # make sure this is before anything else
        screen.fill(RED)

        all_sprite_list.update()

        all_sprite_list.draw(screen)

        # update health
        font = pygame.font.SysFont("Arial", 20, True, False)  # (name, size, bold, italic)
        if luci.get_hp() < 1:
            if not played_death_music:
                play_death_music()
                played_death_music = True
            text = font.render("Lucifer Morningstar: </3", True, WHITE)  # (text to display, anti aliasing, color)
        else:
            health_bar = ""
            for hp in range(0, luci.get_hp(), 10):
                health_bar += "<3"
            text = font.render("Lucifer Morningstar: " + health_bar, True, WHITE)  # (text to display, anti aliasing, color)

        screen.blit(text, [200, 20])
        font = pygame.font.SysFont("Arial", 20, True, False)  # (name, size, bold, italic)
        if michael.get_hp() < 1:
            if not played_death_music:
                play_death_music()
                played_death_music = True
            text = font.render("Archangel Michael: </3", True, WHITE)  # (text to display, anti aliasing, color)
        else:
            health_bar = ""
            for hp in range(0, michael.get_hp(), 10):
                health_bar += "<3"
            text = font.render("Archangel Michael: " + health_bar, True, WHITE)  # (text to display, anti aliasing, color)
        screen.blit(text, [screen_width-500, 20])

        luci.draw(screen)
        michael.draw(screen)

        pygame.display.update()
        fpsClock.tick(FPS)

def reset_game(screen):
    """
    Reset the game variables & map
    :param screen: pygame screen
    """
    global all_sprite_list
    global wall_list
    global screen_width
    global screen_height
    global luci
    global michael
    global time_since_last_powerup
    global lucis_shots
    global michaels_shots
    global luci_group
    global michael_group
    global powerups
    global played_death_music

    played_death_music = False

    all_sprite_list = pygame.sprite.Group()
    wall_list = pygame.sprite.Group()

    BLACK = pygame.Color(0, 0, 0)

    # top wall
    wall = Wall(10, 0, screen_width, 10, BLACK)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    # bottom wall
    wall = Wall(0, screen_height - 10, screen_width, 10, BLACK)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    # left wall
    wall = Wall(0, 0, 10, screen_height, BLACK)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    # right wall
    wall = Wall(screen_width - 10, 0, 10, screen_height, BLACK)
    wall_list.add(wall)
    all_sprite_list.add(wall)

    for i in range(20):
        # (x, y, width, height, color)
        rand_x = random.randrange(0, screen_width-60)
        rand_y = random.randrange(0, screen_height-60)
        rock = Rock(rand_x, rand_y)
        wall_list.add(rock)
        all_sprite_list.add(rock)

    # create Lucifer Morningstar character
    rand_x = random.randrange(0, screen_width/2)
    rand_y = random.randrange(0, screen_height-300)
    luci = Character("Luci", rand_x, rand_y, wall_list, screen)
    luci.draw(screen)

    # create Archangel Michael character
    rand_x = random.randrange(screen_width/2, screen_width-200)
    rand_y = random.randrange(0, screen_height-300)
    michael = Character("Michael", rand_x, rand_y, wall_list, screen)
    michael.draw(screen)

    all_sprite_list.add(luci)
    all_sprite_list.add(michael)

    # to check if a shot hits a player
    luci_group = pygame.sprite.Group()
    michael_group = pygame.sprite.Group()

    luci_group.add(luci)
    michael_group.add(michael)

    lucis_shots = pygame.sprite.Group()
    michaels_shots = pygame.sprite.Group()

    # powerups
    powerups = pygame.sprite.Group()
    time_since_last_powerup = [0]

def play_death_music():
    """
    play sad music
    """
    pygame.mixer.Sound("res/sounds/died.ogg").play()
    pygame.mixer.music.load('res/music/death.ogg')
    pygame.mixer.music.play()

def game_intro(screen):
    """
    Display the intro screen
    :param screen: pygame screen object
    """

    FPS = 60
    fpsClock = pygame.time.Clock()

    intro = True

    # load background music
    pygame.mixer.music.load("res/music/titleScreenLoop.ogg")
    pygame.mixer.music.play(-1, 0)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:

                if event.key == K_SPACE:
                    intro = False

                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit()

            screen.fill(pygame.Color(200, 0, 0))

            BLACK = pygame.Color(0, 0, 0)

            # display banner
            # zapfino, noteworthy
            font = pygame.font.SysFont("trajanpro", 60, True, False)  # (name, size, bold, italic)
            text = font.render("Luci & Michael", True, BLACK)  # (text to display, anti aliasing, color)

            # get width of text, used for centering
            banner_width = text.get_width()
            screen_width = pygame.display.Info().current_w

            screen.blit(text, [(screen_width/2)-(banner_width/2), 60])

            # add luci image to screen
            luci_img = pygame.image.load("res/img/luci.png").convert_alpha()
            screen.blit(luci_img, ((screen_width/3)+25, 150))

            # add michael image to screen
            luci_img = pygame.image.load("res/img/michael.png").convert_alpha()
            screen.blit(luci_img, ((screen_width/2)+125, 150))

            # print luci's control
            font = pygame.font.SysFont("noteworthy", 24, True, False)
            text = font.render("Lucifer Morningstar Controls:", True, BLACK)
            screen.blit(text, [(screen_width/3)-50, 275])

            # print michael's control
            font = pygame.font.SysFont("noteworthy", 24, True, False)
            text = font.render("Archangel Michael Controls:", True, BLACK)
            screen.blit(text, [(screen_width/2)+50, 275])

            font = pygame.font.SysFont("noteworthy", 20, True, False)

            luci_instructions = "WASD: up, down, left, right", "I: shoot up", "J: shoot left", "K: shoot down", "L: shoot right"
            michael_instructions = "Arrow keys: up, down, left, right",  "Numpad 6: shoot up", "Numpad 2: shoot left", "Numpad 3: shoot down", "Numpad enter: shoot right"

            # add luci's controls to the screen
            instruction_starting_y = 325
            for instruction in luci_instructions:
                text = font.render(instruction, True, BLACK)
                screen.blit(text, [(screen_width/3)-50, instruction_starting_y])
                instruction_starting_y += 30

            # add michael's controls to the screen
            instruction_starting_y = 325
            for instruction in michael_instructions:
                text = font.render(instruction, True, BLACK)
                screen.blit(text, [(screen_width/2)+50, instruction_starting_y])
                instruction_starting_y += 30

            # press spacebar to start
            text = font.render("Press spacebar to start (and pause).", True, BLACK)
            screen.blit(text, [(screen_width/2) - (text.get_width()/2), 550])

            # press esc to quit
            text = font.render("Press escape button to quit (or reset the game).", True, BLACK)
            screen.blit(text, [(screen_width/2) - (text.get_width()/2), 600])

            pygame.display.update()
            fpsClock.tick(FPS)

    # load background music
    pygame.mixer.music.load('res/music/fight.ogg')
    pygame.mixer.music.set_volume(0.6)
    pygame.mixer.music.play(-1, 0)


def can_shoot(character):
    """
    Returns a boolean of whether the player can shoot or not
    :param character: character that wants to shoot
    :return: true if the player can shoot, false otherwise
    """
    current_time = cTime()
    time_until_shoot_again = character.last_shot_time + character.shot_wait_time
    if current_time > time_until_shoot_again:
        return True
    return False

def shoot(character, all_sprites, all_projectiles):
    """
    Put the shot on the screen
    :param character: character that is shooting
    :param all_sprites: group of all the sprites
    :param all_projectiles: group of all the projectiles
    """

    # name, direction, ix, iy, speed, damage,  range, shot size
    shot = Shot(character.get_name(), character.get_direction(), character.get_vx(), character.get_vy(), character.get_shot_speed(), character.get_shot_damage(), character.get_shot_range(), character.get_shot_size())

    # set the shot so it is where the player is
    if character.get_direction() == "L":
        shot.rect.x = character.rect.x + (character.get_width()-90)
    elif character.get_direction() == "R":
        shot.rect.x = character.rect.x + (character.get_width()-60)
    else:
        shot.rect.x = character.rect.x + (character.get_width()-55)

    shot.rect.y = character.rect.y + (character.get_height() / 2)

    # add the shot to the lists
    all_sprites.add(shot)
    all_projectiles.add(shot)

    # update last_shot_time
    character.set_last_shot_time(cTime())

    # play shot sound
    global luci_shot_sounds
    global michael_shot_sounds

    if character.get_name() == "Luci":
        luci_shot_sounds[random.randint(0, 1)].play()
    else:
        michael_shot_sounds[random.randint(0, 1)].play()

def show_random_powerup(last_powerup_time, all_sprites, powerups, luci, michael):
    """
    Calculate whether or not to display a powerups
    :param last_powerup_time: self-explanitory
    :param all_sprites: group of all the sprites
    :param powerups: group of all the powerups
    :param luci: luci object
    :param michael: michael object
    """
    current_time = cTime()

    if current_time > last_powerup_time[0] + random.randint(7, 13):
        last_powerup_time[0] = current_time
        display_powerup(all_sprites, powerups, luci, michael)

def display_powerup(all_sprites, powerups, luci, michael):
    """
    Puts the powerup on the screen
    :param all_sprites: group of all the sprites
    :param powerups: group of all the powerups
    :param luci: luci object
    :param michael: michael object
    """
    screen_width = pygame.display.Info().current_w
    screen_height = pygame.display.Info().current_h
    rand_x = random.randrange(25, screen_width-25)
    rand_y = random.randrange(25, screen_height-25)

    powerup = Powerup(rand_x, rand_y)

    luci.add_powerup(powerup)
    michael.add_powerup(powerup)

    # add the powerup to the lists
    all_sprites.add(powerup)
    powerups.add(powerup)


if __name__ == "__main__":
    main()