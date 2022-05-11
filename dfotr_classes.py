import pygame
from math import tan, sin, cos

class Algo(pygame.sprite.Sprite):

    def __init__(self, ai_game):
        pygame.sprite.Sprite.__init__(self)
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.num_lives = 3
        self.game_over = False
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.algo_logo = pygame.image.load('img_folder/algo_logo.png')
        self.image = pygame.transform.scale(self.algo_logo, (50, 50))
        self.rect = self.image.get_rect()

        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

        self.rect.midleft = self.screen_rect.midleft
        self.rect.x += 20


        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        if self.moving_up is True and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.algo_speed
        elif self.moving_down is True and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.algo_speed
        if self.moving_left is True and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.algo_speed
        elif self.moving_right is True and self.rect.right < self.screen_rect.right:
            self.x += self.settings.algo_speed

        self.rect.y = self.y
        self.rect.x = self.x

    def blitme(self):
        """Draw the Algo at its current location."""
        self.screen.blit(self.image, self.rect)


class Chart(pygame.sprite.Sprite):
    def __init__(self, x, y, rotation, bar_width, ai_game):
        pygame.sprite.Sprite.__init__(self)
        self.screen = ai_game.screen
        self.initialize_image(ai_game, bar_width, rotation)
        self.settings = ai_game.settings
        self.rotation = rotation

        pivot_position = (x, y)
        rotated_image, rotated_image_rect = self.rotate_about_point(rotation, pivot_position)
        self.image = rotated_image
        self.rect = rotated_image_rect

        while self.rect.top < 0:
            bar_width -= 25
            rotation -= 5
            self.initialize_image(ai_game, bar_width, rotation)
            pivot_position = (x, y)
            rotated_image, rotated_image_rect = self.rotate_about_point(rotation, pivot_position)
            self.image = rotated_image
            self.rect = rotated_image_rect

        while self.rect.bottom > ai_game.settings.screen_height:
            bar_width -= 25
            rotation += 5
            self.initialize_image(ai_game, bar_width, rotation)
            pivot_position = (x, y)
            rotated_image, rotated_image_rect = self.rotate_about_point(rotation, pivot_position)
            self.image = rotated_image
            self.rect = rotated_image_rect

        self.mask = pygame.mask.from_surface(self.image)

        self.scroll_speed = ai_game.settings.scroll_speed

    def initialize_image(self, ai_game, bar_width, rotation):
        img_height = ai_game.settings.bar_height
        img_width = bar_width
        self.image = pygame.Surface((img_width, img_height), pygame.SRCALPHA)
        if rotation >= 0:
            color = ai_game.green
        else:
            color = ai_game.red
        self.image.fill(color)

    def rotate_about_point(self, rotation, pivot_position):
        image_rect = self.image.get_rect(midleft=pivot_position)
        offset_center_to_pivot = pygame.math.Vector2(pivot_position) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-rotation)
        rotated_image_center = (pivot_position[0] - rotated_offset.x, pivot_position[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(self.image, rotation)
        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
        return rotated_image, rotated_image_rect


    def update(self):
        self.rect.x -= self.scroll_speed
        if self.image.get_width() < 200:
            self.kill()
        if self.rect.right < -200:
            self.kill()

    def blitme(self):
        """Draw the chart at its current location."""
        self.screen.blit(self.image, self.rect)


def to_rad(num):
    return num * 3.14 / 180