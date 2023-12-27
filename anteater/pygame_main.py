import pygame
import keyboard
import os
import random


class Game():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.self_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = pygame.display.get_surface().get_size()

        self.clock = pygame.time.Clock()
        self.target_fps = 60

        self.running = True

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.target_fps)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def render(self):
        pygame.display.flip()


class Cell(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
