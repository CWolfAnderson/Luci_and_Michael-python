import pygame
from spritesheet_functions import SpriteSheet
import random

class Character(pygame.sprite.Sprite):

    def __init__(self, name, x, y, walls, screen):

        super().__init__()

        self.name = name
        self.screen = screen

        # character stats
        self.hp = 100
        # speed any greater than 7 will cause the character to glitch through walls
        self.speed = 6.5
        self.shot_range = 10
        self.damage = 5
        self.range = 5
        self.shot_speed = 9.5
        self.is_dead = False
        self.is_flying = False

        # time player needs to wait to shoot again (in microseconds)
        self.shot_wait_time = 0.5

        # timer used to prevent spamming of projectiles
        self.last_shot_time = 0

        # items the character has picked up
        self.items = []

        # items the character can pick up
        self.pickups = []

        self.change_x = 0
        self.change_y = 0

        # size of shots [[v_width, v_height], [h_width, h_height]]
        self.shot_size = [[27, 44], [44, 26]]

        # used for inherited x & y for shooting
        self.old_x = 0
        self.old_y = 0

        # all the walls that it can collide with
        self.walls = walls

        self.powerups = pygame.sprite.Group()

        # start with both characters looking down
        self.direction = "D"

        self.walking_frames_u = []
        self.walking_frames_d = []
        self.walking_frames_l = []
        self.walking_frames_r = []

        if name == "Luci":
            # __image_path = os.path.join(os.path.dirname(__file__), os.pardir, 'images/star.png')
            sprite_sheet = SpriteSheet("res/img/luci_sprite_sheet_dark.png")

        else:
            sprite_sheet = SpriteSheet("res/img/michael_sprite_sheet_light.png")

        # __image_path = os.path.join(os.path.dirname(__file__), os.pardir, 'images/star.png')
        # self.image = pygame.image.load(__image_path).convert_alpha()
        #
        # self.mask = pygame.mask.from_surface(self.image)
        # self.rect = self.image.get_rect()

        # up
        image = sprite_sheet.get_image(4, 94, 82, 82)
        self.walking_frames_u.append(image)
        image = sprite_sheet.get_image(94, 99, 82, 77)
        self.walking_frames_u.append(image)
        image = sprite_sheet.get_image(184, 94, 82, 82)
        self.walking_frames_u.append(image)
        image = sprite_sheet.get_image(274, 99, 82, 77)
        self.walking_frames_u.append(image)

        # down
        image = sprite_sheet.get_image(4, 4, 82, 82)
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(94, 9, 82, 77)
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(184, 4, 82, 82)
        self.walking_frames_d.append(image)
        image = sprite_sheet.get_image(274, 9, 82, 77)
        self.walking_frames_d.append(image)

        # left
        image = sprite_sheet.get_image(19, 184, 52, 82)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(109, 179, 47, 87)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(194, 184, 57, 82)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(289, 179, 47, 87)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # right
        image = sprite_sheet.get_image(19, 184, 52, 82)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(109, 179, 47, 87)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(194, 184, 57, 82)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(289, 179, 47, 87)
        self.walking_frames_r.append(image)

        # set the image the player starts with
        self.image = self.walking_frames_d[0]

        self.width = 82
        self.height = 82

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.pickup_sounds = [pygame.mixer.Sound("res/sounds/pickup1.wav"), pygame.mixer.Sound("res/sounds/pickup2.wav")]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        """ Move the player. """

        # add to inherited x & y
        self.old_x = self.change_x
        self.old_y = self.change_y

        # check if they should be dead
        if self.check_death() == True:
            self.die()

        if not self.is_dead:

            # pixels character must move before next sprite loads
            pixels_til_update = 40

            # move up/down
            self.rect.y += self.change_y

            if not self.is_flying:
                # see if we hit top/bottom walls
                wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
                for wall in wall_hit_list:
                    # if we are moving down, set our bottom side to the top side of the wall
                    if self.change_y > 0:
                        self.rect.bottom = wall.rect.top
                    else:
                        self.rect.top = wall.rect.bottom

                    # self.change_x = 0
                    # self.change_y = 0

            # move left/right
            self.rect.x += self.change_x

            if not self.is_flying:
                # see if we hit left/right walls
                wall_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
                for wall in wall_hit_list:

                    # if we are moving right, set our right side to the left side of the wall
                    if self.change_x > 0:
                        self.rect.right = wall.rect.left
                    else:
                        # otherwise if we are moving left, do the opposite.
                        self.rect.left = wall.rect.right

                    # self.change_x = 0
                    # self.change_y = 0

            # see if we hit a powerup
            powerup_hit_list = pygame.sprite.spritecollide(self, self.powerups, True)
            for powerup in powerup_hit_list:
                self.pickup_sounds[random.randint(0, 1)].play()
                self.apply_powerup(powerup)

            # update sprite
            pos_y = self.rect.y
            pos_x = self.rect.x

            if self.direction == "U":
                frame = (pos_y // pixels_til_update) % len(self.walking_frames_u)
                self.image = self.walking_frames_u[frame]
                # self.width = 82
                # self.height = 82
                # self.rect = self.image.get_rect()
                self.rect.x = pos_x
                self.rect.y = pos_y
            elif self.direction == "D":
                frame = (pos_y // pixels_til_update) % len(self.walking_frames_d)
                self.image = self.walking_frames_d[frame]
                # self.width = 82
                # self.height = 82
                # self.rect = self.image.get_rect()
                self.rect.x = pos_x
                self.rect.y = pos_y

            if self.direction == "R":
                frame = (pos_x // pixels_til_update) % len(self.walking_frames_r)

                self.image = self.walking_frames_r[frame]
                # self.rect = self.image.rect
                self.rect = self.image.get_rect()
                self.rect.x = pos_x
                self.rect.y = pos_y
            elif self.direction == "L":
                frame = (pos_x // pixels_til_update) % len(self.walking_frames_l)
                self.image = self.walking_frames_l[frame]
                self.rect = self.image.get_rect()
                self.rect.x = pos_x
                self.rect.y = pos_y

            self.stop()

    def check_death(self):
        if self.hp < 1:
            return True
        else:
            return False

    def die(self):
        if self.name == "Luci":
            self.image = pygame.image.load("res/img/luci_dead.png").convert_alpha()
        else:
            self.image = pygame.image.load("res/img/michael_dead.png").convert_alpha()

        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.is_dead = True

    def is_dead(self):
        return self.is_dead

    def add_wall(self, wall):
        self.walls.append(wall)

    # player-controlled movement
    def go_up(self):
        """ Called when the user hits "W". """
        self.change_y = -self.speed
    def go_down(self):
        """ Called when the user hits "S". """
        self.change_y = self.speed
    def go_left(self):
        """ Called when the user hits "A". """
        self.change_x = -self.speed
    def go_right(self):
        """ Called when the user hits "D". """
        self.change_x = self.speed
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
        self.change_y = 0

    def face_up(self):
        self.direction = "U"
        return "U"

    def face_down(self):
        self.direction = "D"
        return "D"

    def face_left(self):
        self.direction = "L"
        return "L"

    def face_right(self):
        self.direction = "R"
        return "R"

    # getters
    def get_name(self):
        return self.name

    def get_hp(self):
        return self.hp

    def get_shot_speed(self):
        return self.shot_speed

    def get_shot_range(self):
        return self.shot_range

    def get_shot_damage(self):
        return self.damage

    def get_direction(self):
        return self.direction

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_vx(self):
        return self.old_x

    def get_vy(self):
        return self.old_y

    def get_shot_size(self):
        return self.shot_size

    def decrease_hp(self, amount):
        self.hp -= amount

    def increase_hp(self, amount):
        self.hp += amount

    def set_last_shot_time(self, time):
        self.last_shot_time = time

    def add_powerup(self, pups):
        self.powerups.add(pups)

    def apply_powerup(self, pup):
        if pup.powerup_name == "canceling_shots":
            self.display_powerup("Cancelling Shots")
        elif pup.powerup_name == "speed_increase":
            self.display_powerup("Speed Up")
            self.speed += 0.5
        elif pup.powerup_name == "flight":
            self.display_powerup("Flight")
            self.is_flying = True
        elif pup.powerup_name == "faster_shooting":
            self.display_powerup("Faster Shooting")
            self.shot_wait_time -= 0.1
        elif pup.powerup_name == "big_shot":
            self.display_powerup("Big Shot")
            self.shot_size[0][0] += 7
            self.shot_size[0][1] += 7
            self.shot_size[1][0] += 7
            self.shot_size[1][1] += 7
        elif pup.powerup_name == "increased_damage":
            self.display_powerup("Moar Damage")
            self.damage += 2
        elif pup.powerup_name == "speed_decrease":
            self.display_powerup("Slow Down")
            self.speed -= 0.5
        elif pup.powerup_name == "slower_shooting":
            self.display_powerup("Slower Shooting")
            self.shot_wait_time += 0.1
        elif pup.powerup_name == "small_shot":
            self.display_powerup("Small Shot")
            if self.shot_size[0][0] > 7 and self.shot_size[1][0] > 7:
                self.shot_size[0][0] -= 7
                self.shot_size[0][1] -= 7
                self.shot_size[1][0] -= 7
                self.shot_size[1][1] -= 7
        elif pup.powerup_name == "decreased_damage":
            self.display_powerup("Decreased Damage")
            self.damage -= 2
        elif pup.powerup_name == "god_mode":
            self.display_powerup("God Mode")
            self.speed = 9
            self.damage += 20
            self.shot_wait_time = 0.1
            self.is_flying = True

    def display_powerup(self, pup_name):
        # get powerup and prepare to display it
        x = self.rect.x
        y = self.rect.y
        font = pygame.font.SysFont("Arial", 20, True, False)  # (name, size, bold, italic)
        text = font.render(pup_name, True, pygame.Color(0, 0, 0))  # (text to display, anti aliasing, color)
        self.screen.blit(text, [x, y-20])

    # powerups
    def increase_shot_wait_time(self):
        self.shot_wait_time += 250000

    def decrease_shot_wait_time(self):
        self.shot_wait_time -= 250000

    def increase_speed(self):
        self.speed += 1

    def decrease_speed(self):
        self.speed -= 1