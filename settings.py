import pygame


class Settings:
    """A class to store the settings for Algo Game."""

    def __init__(self):
        """Initialize Game Settings"""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bar_height = 200
        # self.bg_color = (255, 255, 255)
        self.algo_speed = 5.5
        self.fps = 60
        self.scroll_speed = 9.5
        self.min_bar_length = 500
        self.max_bar_length = 1200
        self.font_size = 40
        self.font = pygame.font.SysFont('Impact', self.font_size)
        self.fancy_font = pygame.font.SysFont('Berlin Sans FB', int(self.font_size * 1.3), bold=False)

