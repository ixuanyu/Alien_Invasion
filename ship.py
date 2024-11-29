import pygame

class Ship:
    def __init__(self):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        self.rect.bottom = self.screen_rect.midbottom

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        