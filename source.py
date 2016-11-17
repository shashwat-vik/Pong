import sys
import pygame

class Screen:
    def __init__(self):
        # GAME PARAMETERS
        self.SCREEN_WIDTH = 700
        self.SCREEN_HEIGHT = 500
        self.FPS = 200

        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.CLOCK = pygame.time.Clock()

        # COLORS
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

class Pong(Screen):
    def __init__(self):
        Screen.__init__(self)

    def main(self):
        pygame.init()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.CLOCK.tick(self.FPS)

if __name__ == '__main__':
    pong = Pong()
    pong.main()
