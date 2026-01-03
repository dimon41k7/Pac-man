import pygame

class Input:
    def get_direction(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            return -1, 0, "left"
        if keys[pygame.K_d]:
            return 1, 0, "right"
        if keys[pygame.K_w]:
            return 0, -1, "up"
        if keys[pygame.K_s]:
            return 0, 1, "down"

        return 0, 0, None