import pygame
import random

pygame.init()

# constants
WIDTH = 960
HEIGHT = 720
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# window setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")
clock = pygame.time.Clock()
FPS = 60

# BG img
bg_img = pygame.transform.scale(pygame.image.load("background.png"), (WIDTH, HEIGHT))


class Paddle:
    speed = 20
    width = 10
    height = 100
    y_pos = int(HEIGHT / 2 - height / 2)

    def __init__(self, x, color):
        self.x_pos = x
        self.color = color

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x_pos, self.y_pos, self.width, self.height))

    def move_up(self):
        self.y_pos = max(self.y_pos - self.speed, 0)

    def move_down(self):
        self.y_pos = min(self.y_pos + self.speed, HEIGHT - self.height)

    def reset_position(self):
        self.y_pos = int(HEIGHT / 2 - self.height / 2)


# paddles
paddle_1 = Paddle(40, RED)
paddle_2 = Paddle(WIDTH - 50, BLUE)


class Score:
    def __init__(self):
        self.score = 0

    def add_1(self):
        self.score += 1

    def get_score(self):
        return self.score


p1_score = Score()
p2_score = Score()


class Ball:
    radius = 8
    x_vel = random.choice([15, -15])
    y_vel = 0

    def __init__(self):
        self.x_pos = WIDTH/2
        self.y_pos = HEIGHT/2

    def set_position(self, x, y):
        self.x_pos = x
        self.y_pos = y

    def set_velocity(self, x, y):
        self.x_vel = x
        self.y_vel = y

    def draw(self, window):
        pygame.draw.circle(window, GREEN, (self.x_pos, self.y_pos), self.radius)

    def move(self):
        if (self.x_pos + self.x_vel < paddle_1.x_pos + paddle_1.width) and (paddle_1.y_pos < self.y_pos + self.y_vel + self.radius < paddle_1.y_pos + paddle_1.height):
            self.x_vel = - self.x_vel
            self.y_vel = - (paddle_1.y_pos + paddle_1.height/2 - self.y_pos)/WIDTH * 100

        elif self.x_pos + self.x_vel < 0:
            p2_score.add_1()
            self.set_position(41, HEIGHT/2)
            self.set_velocity(15, 0)
            self.draw(WIN)
            paddle_1.reset_position()
            paddle_2.reset_position()
            pygame.time.wait(1000)

        if (self.x_pos + self.x_vel > paddle_2.x_pos) and (paddle_2.y_pos < self.y_pos + self.y_vel + self.radius < paddle_2.y_pos + paddle_2.height):
            self.x_vel = - self.x_vel
            self.y_vel = - (paddle_2.y_pos + paddle_2.height / 2 - self.y_pos) /WIDTH * 100

        elif self.x_pos + self.x_vel > WIDTH:
            p1_score.add_1()
            self.set_position(WIDTH-51, HEIGHT / 2)
            self.set_velocity(-15, 0)
            self.draw(WIN)
            paddle_1.reset_position()
            paddle_2.reset_position()
            pygame.time.wait(1000)

        if self.y_pos + self.y_vel > HEIGHT or self.y_pos + self.y_vel < 0:
            self.y_vel = - self.y_vel

        self.x_pos += self.x_vel
        self.y_pos += self.y_vel


ball = Ball()

def draw_text():
    font = pygame.font.SysFont("consolas", 40)
    text = font.render(f"{str(p1_score.get_score())}       {str(p2_score.get_score())}", False, WHITE)
    WIN.blit(text, (WIDTH/2 - 100, 30))


def show_winner(score1, score2):
    if score1 >= 10:
        font = pygame.font.SysFont("consolas", 50)
        text = font.render(f"PLAYER RED WINS!", False, RED)
        WIN.fill(BLACK)
        WIN.blit(text, (280, HEIGHT/2 - 30))
        pygame.time.wait(2000)
        return True

    if score2 >= 10:
        font = pygame.font.SysFont("consolas", 50)
        text = font.render(f"PLAYER BLUE WINS!", False, BLUE)
        WIN.fill(BLACK)
        WIN.blit(text, (280, HEIGHT/2 - 30))
        pygame.time.wait(2000)
        return True

    else:
        return False

def main():
    run = True
    while run:
        if show_winner(p1_score.get_score(), p2_score.get_score()):
            run = False
        clock.tick(FPS)
        WIN.blit(bg_img, (0, 0))
        draw_text()
        paddle_1.draw(WIN)
        paddle_2.draw(WIN)
        ball.draw(WIN)
        ball.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle_1.move_up()
        if keys[pygame.K_s]:
            paddle_1.move_down()
        if keys[pygame.K_UP]:
            paddle_2.move_up()
        if keys[pygame.K_DOWN]:
            paddle_2.move_down()

        show_winner(p1_score.get_score(), p2_score.get_score())
        pygame.display.update()

    pygame.quit()


main()
