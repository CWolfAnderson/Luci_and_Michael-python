"""Rock module

"""

import pygame
import random
from spritesheet_functions import SpriteSheet

class Rock(pygame.sprite.Sprite):

    def __init__(self, x, y):

        super().__init__()

        sprite_sheet = SpriteSheet("res/img/rocks.png")

        rand = random.randrange(0, 7)
        if rand == 0:
            # [0][1]
            image = sprite_sheet.get_image(74, 9, 58, 55)
            # rotate the rock
            rand = random.randrange(0, 4)
            if rand == 0:
                self.image = pygame.transform.flip(image, True, False)
            elif rand == 1:
                self.image = pygame.transform.flip(image, False, True)
            elif rand == 2:
                self.image = pygame.transform.flip(image, True, True)
            else:
                self.image = sprite_sheet.get_image(74, 9, 58, 55)
        elif rand == 1:
            # [0][2]
            image = sprite_sheet.get_image(144, 2, 57, 62)
            # rotate the rock
            rand = random.randrange(0, 4)
            if rand == 0:
                self.image = pygame.transform.flip(image, True, False)
            elif rand == 1:
                self.image = pygame.transform.flip(image, False, True)
            elif rand == 2:
                self.image = pygame.transform.flip(image, True, True)
            else:
                self.image = sprite_sheet.get_image(144, 2, 57, 62)
        elif rand == 2:
            # [1][2]
            image = sprite_sheet.get_image(142, 75, 58, 56)
            # rotate the pot (it shouldn't be upside down
            rand = random.randrange(0, 2)
            if rand == 0:
                self.image = pygame.transform.flip(image, True, False)
            else:
                self.image = sprite_sheet.get_image(142, 75, 58, 56)
        elif rand == 3:
            # [2][1]
            image = sprite_sheet.get_image(76, 145, 53, 55)
            # rotate the rock
            rand = random.randrange(0, 4)
            if rand == 0:
                self.image = pygame.transform.flip(image, True, False)
            elif rand == 1:
                self.image = pygame.transform.flip(image, False, True)
            elif rand == 2:
                self.image = pygame.transform.flip(image, True, True)
            else:
                self.image = sprite_sheet.get_image(76, 145, 53, 55)
        elif rand == 4:
            # [2][2]
            image = sprite_sheet.get_image(76, 145, 53, 55)
            # rotate the pot
            rand = random.randrange(0, 2)
            if rand == 0:
                self.image = pygame.transform.flip(image, True, False)
            else:
                self.image = sprite_sheet.get_image(142, 144, 58, 56)
        elif rand == 5:
            # [3][0]
            image = sprite_sheet.get_image(4, 207, 128, 130)
            # rotate the rock
            rand = random.randrange(0, 4)
            if rand == 0:
                self.image = pygame.transform.flip(image, True, False)
            elif rand == 1:
                self.image = pygame.transform.flip(image, False, True)
            elif rand == 2:
                self.image = pygame.transform.flip(image, True, True)
            else:
                self.image = sprite_sheet.get_image(4, 207, 128, 130)
        # elif rand == 6:
        #     # [4][0]
        #     image = sprite_sheet.get_image(7, 336, 56, 126)
        #     # rotate the rock
        #     rand = random.randrange(0, 4)
        #     if rand == 0:
        #         self.image = pygame.transform.flip(image, True, False)
        #     elif rand == 1:
        #         self.image = pygame.transform.flip(image, False, True)
        #     elif rand == 2:
        #         self.image = pygame.transform.flip(image, True, True)
        #     else:
        #         self.image = sprite_sheet.get_image(7, 336, 56, 126)
        elif rand == 6:
            # [5][0]
            image = sprite_sheet.get_image(9, 488, 119, 57)
            # rotate the rock
            rand = random.randrange(0, 4)
            if rand == 0:
                self.image = pygame.transform.flip(image, True, False)
            elif rand == 1:
                self.image = pygame.transform.flip(image, False, True)
            elif rand == 2:
                self.image = pygame.transform.flip(image, True, True)
            else:
                self.image = sprite_sheet.get_image(9, 488, 119, 57)
        # elif rand == 8:
        #     self.image = sprite_sheet.get_image(, , , )
        # elif rand == 9:
        #     self.image = sprite_sheet.get_image(, , , )
        # elif rand == 10:
        #     self.image = sprite_sheet.get_image(, , , )
        # elif rand == 11:
        #     self.image = sprite_sheet.get_image(, , , )
        # elif rand == 12:
        #     self.image = sprite_sheet.get_image(, , , )
        # elif rand == :
        #     self.image = sprite_sheet.get_image(, , , )



        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y