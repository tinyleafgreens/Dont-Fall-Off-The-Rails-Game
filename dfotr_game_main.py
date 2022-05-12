import sys
import pygame
from settings import Settings
from dfotr_classes import Algo, Chart
from random import randint
import traceback
from time import time
import os


class AlgoGame:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.settings = Settings()
        self.max_bar_len = self.settings.max_bar_length
        self.min_bar_len = self.settings.min_bar_length

        self.bg = pygame.image.load('img_folder/silvio_bg.png')
        self.bg_go = pygame.image.load('img_folder/silvio_bg_game_over.png')
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.scrolling = False
        self.num_lives = 3
        self.score = 0

        self.game_started = False
        self.game_over = False
        self.stop_time = time()

        self.chart_group = pygame.sprite.Group()
        self.algo_group = pygame.sprite.GroupSingle()

        pygame.display.set_caption("Don't Fall Off The Rails! by Tinyleaf Greens")

        # Initialize clock
        self.clock = pygame.time.Clock()
        self.total_time = 0
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)

        # Form is
        first_chart = Chart(0, int(self.settings.screen_height/2), randint(-10, 0), self.screen.get_width(), self)
        self.second_chart = Chart(first_chart.rect.right - 200, first_chart.rect.bottom - (self.settings.bar_height / 2), randint(0, 10), randint(self.min_bar_len, self.max_bar_len), self)
        self.chart_group.add(first_chart)
        self.chart_group.add(self.second_chart)
        self.algo = Algo(self)
        pygame.display.set_icon(self.algo.image)

        self.algo_group.add(self.algo)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events
            self.clock.tick(self.settings.fps)
            if self.scrolling:
                self.total_time += self.clock.get_rawtime()
                if self.total_time > 1000:
                    # print(self.settings.scroll_speed)
                    self.settings.scroll_speed += 0.5
                    self.algo.settings.algo_speed += 0.15
                    self.total_time = 0
            self._check_events()
            self._check_collision()
            self.algo.update()
            if self.scrolling:
                if self.second_chart.rect.right < self.settings.screen_width + 100:
                    newest_chart = self._make_new_chart()
                    self.chart_group.add(newest_chart)
                    self.second_chart = newest_chart
                    self.score += int(self.settings.scroll_speed)
            if self.scrolling:
                self.chart_group.update()

            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if self.game_started is True and time() > (self.stop_time + 0.5) and pygame.KEYDOWN and not self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT):
                        self.scrolling = True
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_started is False:
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT):
                        self.game_started = True
                        self.scrolling = True
                if self.scrolling:
                    if event.key == pygame.K_UP:
                        self.algo.moving_up = True
                    elif event.key == pygame.K_DOWN:
                        self.algo.moving_down = True
                    if event.key == pygame.K_LEFT:
                        self.algo.moving_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.algo.moving_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.algo.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.algo.moving_down = False
                if event.key == pygame.K_LEFT:
                    self.algo.moving_left = False
                elif event.key == pygame.K_RIGHT:
                    self.algo.moving_right = False

            if self.game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run()

    def _update_screen(self):
        """Updates the screen images and flip to new screen"""
        # Redraw the screen during each pass through the loop
        self.screen.blit(self.bg, (0, 0))
        self.chart_group.draw(self.screen)
        self._draw_text()
        if not self.scrolling:
            image = self.settings.font.render(f'{"You fell off the rails! " if self.game_started else ""}'
                                              f'Press any arrow key to {"begin" if not self.game_started else "continue"}', True, (0, 0, 0))
            self.screen.blit(image, (self.screen.get_width() * 0.05, self.screen.get_height() * 0.08))

            # Show before game start only
            if not self.game_started:
                image = self.settings.fancy_font.render('"Don\'t Fall off the Rails"', True, (0, 0, 0))
                self.screen.blit(image, (self.screen.get_width() * 0.05, self.screen.get_height() * 0.75))
                image = self.settings.fancy_font.render('   By: Tinyleaf Greens', True, (0, 0, 0))
                self.screen.blit(image, (self.screen.get_width() * 0.05, self.screen.get_height() * 0.75 + self.settings.font_size * 1.3))

        self.algo.blitme()
        # Make the most recently drawn screen visible.
        if self.game_over:
            self.screen.blit(self.bg_go, (0, 0))
            image = self.settings.font.render('GAME OVER.', True, (0, 0, 0))
            self.screen.blit(image, (self.screen.get_width() * 0.05, self.screen.get_height() / 2 - self.settings.font_size))
            image = self.settings.font.render(f'FINAL SCORE: {self.score}', True, (0, 0, 0))
            self.screen.blit(image, (self.screen.get_width() * 0.05, self.screen.get_height() / 2 + (0.5 * self.settings.font_size)))
            image = self.settings.font.render('(PRESS SPACE TO RESTART)', True, (0, 0, 0))
            self.screen.blit(image, (self.screen.get_width() * 0.05, self.screen.get_height() / 2 + (2 * self.settings.font_size)))

        pygame.display.flip()

    def _make_new_chart(self):
        if self.second_chart.rect.topright[1] < 500:
            rotation = randint(-40, 0)
        elif self.second_chart.rect.bottomright[1] > self.settings.screen_height - 500:
            rotation = randint(0, 40)
        else:
            rotation = randint(-30, 30)

        if self.second_chart.rotation >= 0:
            newest_chart = Chart(self.second_chart.rect.right - 200,
                                 self.second_chart.rect.top + (self.settings.bar_height / 2), rotation,
                                 randint(self.min_bar_len, self.max_bar_len), self)
        else:
            newest_chart = Chart(self.second_chart.rect.right - 200,
                                 self.second_chart.rect.bottom - (self.settings.bar_height / 2), rotation,
                                 randint(self.min_bar_len, self.max_bar_len), self)
        return newest_chart

    def _check_collision(self):
        colliding_sprites = pygame.sprite.spritecollide(self.algo, self.chart_group, False, collided=pygame.sprite.collide_mask)
        if not colliding_sprites:
            if not self.game_over:
                self._lose_life()

    def _lose_life(self):
        if self.num_lives == 0:
            self.settings.font_size *= 1.5
            self.scrolling = False
            self.game_over = True

        self.algo.moving_up = False
        self.algo.moving_down = False
        self.algo.moving_right = False
        self.algo.moving_left = False

        self.num_lives -= 1
        self.scrolling = False
        sprite_num = 0
        while self.chart_group.sprites()[sprite_num].rect.centerx < 50:
            sprite_num += 1
        self.algo.rect.center = self.chart_group.sprites()[sprite_num].rect.center
        self.algo.x = self.chart_group.sprites()[sprite_num].rect.centerx - (self.algo.image.get_width()/2)
        self.algo.y = self.chart_group.sprites()[sprite_num].rect.centery - (self.algo.image.get_height()/2)
        self.stop_time = time()
        for sprite in self.chart_group.sprites():
            sprite.scroll_speed -= 1
        self.settings.scroll_speed -= 1


    def _draw_text(self):
        score = self.score
        num_lives = self.num_lives

        # Score Counter
        text_color = (0, 0, 0)
        image = self.settings.font.render(f'Score: {score}', True, text_color)
        self.screen.blit(image, (self.screen.get_width() * 0.8, 0))

        # Lives Counter
        image = self.settings.font.render(f'Lives Remaining: {num_lives}', True, text_color)
        self.screen.blit(image, (self.screen.get_width() * 0.05, 0))

def run():
    ai = AlgoGame()
    ai.run_game()

run()
