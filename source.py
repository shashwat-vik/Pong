import sys
import pygame

class Screen:
    def __init__(self):
        # GAME PARAMETERS
        self.SCREEN_WIDTH = 400
        self.SCREEN_HEIGHT = 300
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
        # BALL, PADDLE1, PADDLE2, SCORE
        self.ball = pygame.Rect((ball_pos_X, ball_pos_Y), (self.LINE_THICKNESS, self.LINE_THICKNESS))
        self.ballDirX = -1
        self.ballDirY = -1

        self.paddle1 = pygame.Rect((self.PADDLE_OFFSET, paddle_pos_Y), (self.LINE_THICKNESS, self.PADDLE_SIZE))
        self.paddle1_velocity = 0
        self.paddle2 = pygame.Rect((self.SCREEN_WIDTH - self.LINE_THICKNESS - self.PADDLE_OFFSET, paddle_pos_Y), (self.LINE_THICKNESS, self.PADDLE_SIZE))

        self.SCORE = 0
        self.FONT_SIZE = 18
        self.FONT_WRITER = pygame.font.Font(pygame.font.match_font('consolas'),self.FONT_SIZE)

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

    def move_ball(self):
        self.ball.x += self.ballDirX
        self.ball.y += self.ballDirY

    def check_boundary_collision(self):
        if self.ball.top == self.LINE_THICKNESS or self.ball.bottom == (self.SCREEN_HEIGHT - self.LINE_THICKNESS):
            self.ballDirY *= -1
        if self.ball.left == self.LINE_THICKNESS or self.ball.right == (self.SCREEN_WIDTH - self.LINE_THICKNESS):
            self.ballDirX *= -1

    def check_paddle_collision(self):
        if self.ballDirX == -1:
            if self.paddle1.right == self.ball.left and self.paddle1.top < self.ball.top and self.paddle1.bottom > self.ball.bottom:
                self.ballDirX *= -1
        if self.ballDirX == 1:
            if self.paddle2.left == self.ball.right and self.paddle2.top < self.ball.top and self.paddle2.bottom > self.ball.bottom:
                self.ballDirX *= -1

    def evil_AI(self):
        # HIT
        if self.ballDirX == 1:
            if self.paddle2.centery < self.ball.centery:
                self.paddle2.y += 1
            elif self.paddle2.centery > self.ball.centery:
                self.paddle2.y -= 1
        # CENTER-ALIGN
        elif self.ballDirX == -1:
            if self.paddle2.centery < self.SCREEN_HEIGHT/2:
                self.paddle2.y += 1
            elif self.paddle2.centery > self.SCREEN_HEIGHT/2:
                self.paddle2.y -= 1

    def paddle1_control(self):
        self.paddle1.centery += self.paddle1_velocity

    def display_score(self):
        data = "SCORE: {0}".format(self.SCORE)
        score_surface = self.FONT_WRITER.render(data, True, self.WHITE)
        score_rect = score_surface.get_rect()
        score_rect.topleft = (self.SCREEN_WIDTH - self.LINE_THICKNESS - self.PADDLE_OFFSET - score_rect.width, self.LINE_THICKNESS + self.PADDLE_OFFSET)

        self.SCREEN.blit(score_surface, score_rect)

    def update_score(self):
        # Reset to 0 if left wall is hit
        if self.ball.left == self.LINE_THICKNESS:
            self.SCORE = 0
        # +1 if ball is hit
        elif self.ballDirX == -1 and self.paddle1.right == self.ball.left and self.paddle1.top < self.ball.top and self.paddle1.bottom > self.ball.bottom:
            self.SCORE += 1
        # +5 on beating evil_AI
        elif self.ball.right == (self.SCREEN_WIDTH - self.LINE_THICKNESS):
            self.SCORE += 5

    def update_components(self):
        self.draw_components()
        self.move_ball()
        self.paddle1_control()
        self.evil_AI()
        self.check_boundary_collision()
        self.update_score()
        self.check_paddle_collision()

        self.display_score()

    def main(self):
        pygame.init()
        self.init_components()
        pygame.mouse.set_visible(False)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    self.paddle1.y = event.pos[1]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.paddle1_velocity = -1
                    elif event.key == pygame.K_DOWN:
                        self.paddle1_velocity = 1
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        self.paddle1_velocity = 0

            self.update_components()

            pygame.display.update()
            self.CLOCK.tick(self.FPS)

if __name__ == '__main__':
    pong = Pong()
    pong.main()
