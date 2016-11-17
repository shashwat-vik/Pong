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
        self.LINE_THICKNESS = 8
        self.PADDLE_SIZE = 50
        self.PADDLE_OFFSET = 20

    def init_components(self):
        ##########
        # INITIAL POSITIONS
        ball_pos_X = (self.SCREEN_WIDTH - self.LINE_THICKNESS)//2
        ball_pos_Y = (self.SCREEN_HEIGHT - self.LINE_THICKNESS)//2
        paddle_pos_Y = (self.SCREEN_HEIGHT - self.PADDLE_SIZE)//2
        ##########
        # BALL, PADDLE1, PADDLE2
        self.ball = pygame.Rect((ball_pos_X, ball_pos_Y), (self.LINE_THICKNESS, self.LINE_THICKNESS))
        self.paddle1 = pygame.Rect((self.PADDLE_OFFSET, paddle_pos_Y), (self.LINE_THICKNESS, self.PADDLE_SIZE))
        self.paddle2 = pygame.Rect((self.SCREEN_WIDTH - self.LINE_THICKNESS - self.PADDLE_OFFSET, paddle_pos_Y), (self.LINE_THICKNESS, self.PADDLE_SIZE))

        self.draw_components()

    def draw_ball(self, ball):
        pygame.draw.rect(self.SCREEN, self.WHITE, ball)

    def draw_paddle(self, paddle):
        if paddle.top < self.LINE_THICKNESS:
            paddle.top = self.LINE_THICKNESS
        elif paddle.bottom > (self.SCREEN_HEIGHT - self.LINE_THICKNESS):
            paddle.bottom = self.SCREEN_HEIGHT - self.LINE_THICKNESS
        pygame.draw.rect(self.SCREEN, self.WHITE, paddle)

    def draw_arena(self):
        self.SCREEN.fill(self.BLACK)
        # Center Line
        pygame.draw.line(self.SCREEN, self.WHITE, (self.SCREEN_WIDTH//2, 0), (self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT), self.LINE_THICKNESS//4)
        # Draw Outline of Arena
        pygame.draw.rect(self.SCREEN, self.WHITE, ((0, 0),(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)), self.LINE_THICKNESS*2)

    def draw_components(self):
        self.draw_arena()
        self.draw_paddle(self.paddle1)
        self.draw_paddle(self.paddle2)
        self.draw_ball(self.ball)

    def main(self):
        pygame.init()
        self.init_components()

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
