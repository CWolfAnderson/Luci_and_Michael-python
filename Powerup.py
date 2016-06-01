import pygame
import random
from spritesheet_functions import SpriteSheet

class Powerup(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self, x, y):
        # call the parent class (Sprite) constructor
        super().__init__()

        sprite_sheet = SpriteSheet("res/img/space.png")

        # powerups
        powerups = ["canceling_shots", # 5%
                    "flight", # 5%
                    "speed_increase", # 10%
                    "speed_decrease", # 10%
                    "increased_damage", # 10%
                    "decreased_damage", # 10%
                    "faster_shooting", # 10%
                    "slower_shooting", # 10%
                    "big_shot", # 10%
                    "small_shot", # 10%
                    "double_shot", # 3%
                    "god_mode"] # 3%

        # rand = random.choice(powerups)
        rand = random.randrange(1, 97)

        # powerup images
        # [1][0]    mars
        first = sprite_sheet.get_image(4, 52, 71, 72)
        # [1][1]    white
        second = sprite_sheet.get_image(82, 52, 72, 72)
        # [1][2]    cracked
        third = sprite_sheet.get_image(160, 48, 72, 76)
        # [1][3]    purple streaks
        fourth = sprite_sheet.get_image(239, 52, 69, 73)
        # [1][4]    earth
        fifth = sprite_sheet.get_image(317, 52, 71, 73)
        # [1][5]    venus
        sixth = sprite_sheet.get_image(395, 52, 71, 72)
        # [2][0]    neptune
        seventh = sprite_sheet.get_image(4, 128, 73, 74)
        # [2][1]    sun
        eighth = sprite_sheet.get_image(78, 130, 78, 72)
        # [2][2]    black hole
        ninth = sprite_sheet.get_image(157, 128, 79, 72)
        # [2][3]    moon
        tenth = sprite_sheet.get_image(239, 130, 55, 72)
        # [2][4]    other blue one
        eleventh = sprite_sheet.get_image(317, 130, 71, 72)
        # [2][5]    volcano
        twelfth = sprite_sheet.get_image(395, 129, 71, 71)

        if rand <= 5:
            self.powerup_name = powerups[0] # canceling_shots
            image = first
            self.image = pygame.transform.scale(image, (35, 36))
        elif rand > 5 and rand <= 10:
            self.powerup_name = powerups[1] # flight
            image = seventh
            self.image = pygame.transform.scale(image, (35, 35))
        elif rand > 10 and rand <= 20:
            self.powerup_name = powerups[2] # speed_increase
            image = fourth
            self.image = pygame.transform.scale(image, (35, 37))
        elif rand > 20 and rand <= 30:
            self.powerup_name = powerups[3] # speed_decrease
            image = second
            self.image = pygame.transform.scale(image, (34, 36))
        elif rand > 30 and rand <= 40:
            self.powerup_name = powerups[4] # increased_damage
            image = fifth
            self.image = pygame.transform.scale(image, (35, 36))
        elif rand > 40 and rand <= 50:
            self.powerup_name = powerups[5] # decreased_damage
            image = sixth
            self.image = pygame.transform.scale(image, (35, 36))
        elif rand > 50 and rand <= 60:
            self.powerup_name = powerups[6] # faster_shooting
            image = eighth
            self.image = pygame.transform.scale(image, (36, 36))
        elif rand > 60 and rand <= 70:
            self.powerup_name = powerups[7] # slower_shooting
            image = third
            self.image = pygame.transform.scale(image, (37, 36))
        elif rand > 70 and rand <= 80:
            self.powerup_name = powerups[8] # big_shot
            image = ninth
            self.image = pygame.transform.scale(image, (37, 36))
        elif rand > 80 and rand <= 90:
            self.powerup_name = powerups[9] # small_shot
            image = tenth
            self.image = pygame.transform.scale(image, (25, 36))
        elif rand > 90 and rand <= 93:
            self.powerup_name = powerups[10] # double_shot
            image = eleventh
            self.image = pygame.transform.scale(image, (35, 36))
        elif rand > 93 and rand <= 96:
            self.powerup_name = powerups[11] # god_mode
            image = twelfth
            self.image = pygame.transform.scale(image, (35, 35))

        #     self.powerup_name = powerups[11]
        #     image = twelfth
        # elif rand == 12:
        #     # [][]
        #     self.powerup_name = powerups[rand]
        #     image = sprite_sheet.get_image(,, , )
        #     self.image = pygame.transform.scale(image, (35, 36))
        # elif rand == 13:
        #     # [][]
        #     self.powerup_name = powerups[rand]
        #     image = sprite_sheet.get_image(,, , )
        #     self.image = pygame.transform.scale(image, (35, 36))
        # elif rand == 14:
        #     # [][]
        #     self.powerup_name = powerups[rand]
        #     image = sprite_sheet.get_image(,, , )
        #     self.image = pygame.transform.scale(image, (35, 36))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y