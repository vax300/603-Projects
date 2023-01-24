'''
603 Final Project from Va Xiong
PING PONG GAME with visuals and sound effects
Does not have a menu or game over screen
This code uses some existing ping pong codes which has been refactored
and modified for this project.
'''

import pygame, sys, random # installed pygame to run the PING PONG GAME
from pygame import mixer # importing mixer for music and sound control

# Define Game and Scoring
class Game_Setup:
    def __init__(self, ball_group, paddle_group):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group

    def run_game(self):
        # Drawing the game objects
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        # Updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = basic_font.render(str(self.player_score), True, accent_color)
        opponent_score = basic_font.render(str(self.opponent_score), True, accent_color)

        player_score_rect = player_score.get_rect(midleft=(screen_width / 2 + 50, screen_height / 30))
        opponent_score_rect = opponent_score.get_rect(midright=(screen_width / 2 - 50, screen_height / 30))

        screen.blit(player_score, player_score_rect)
        screen.blit(opponent_score, opponent_score_rect)

# Create Block for Objects
class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

# Create Ball, Collisions and Timer reset
class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles):
        super().__init__(path, x_pos, y_pos)
        self.speed_x = speed_x * random.choice((-1, 1))
        self.speed_y = speed_y * random.choice((-1, 1))
        self.paddles = paddles
        self.active = False
        self.score_time = 0

    def update(self):
        if self.active:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.collisions()
        else:
            self.counter_reset()

    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(block_sound)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self, self.paddles, False):
            pygame.mixer.Sound.play(block_sound)
            collision_paddle = pygame.sprite.spritecollide(self, self.paddles, False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1

    def reset_ball(self):
        self.active = False
        self.speed_x *= random.choice((-1, 1))
        self.speed_y *= random.choice((-1, 1))
        self.score_time = pygame.time.get_ticks()
        self.rect.center = (screen_width / 2, screen_height / 2)
        pygame.mixer.Sound.play(score_sound)

    def counter_reset(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 5

        if current_time - self.score_time <= 700:
            countdown_number = 5
        if 700 < current_time - self.score_time <= 1400:
            countdown_number = 4
        if 1400 < current_time - self.score_time <= 2100:
            countdown_number = 3
        if 2100 < current_time - self.score_time <= 2800:
            countdown_number = 2
        if 2800 < current_time - self.score_time <= 3500:
            countdown_number = 1
        if current_time - self.score_time >= 3500:
            self.active = True

        time_counter = basic_font.render(str(countdown_number), True, accent_color)
        time_counter_rect = time_counter.get_rect(center=(screen_width / 2, screen_height / 2 + 50))
        pygame.draw.rect(screen, bg_color, time_counter_rect)
        screen.blit(time_counter, time_counter_rect)

# Create Player and Paddle
class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed
        self.movement = 0

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()

# Create AI computer and Paddle
class AI_Player(Block):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__(path, x_pos, y_pos)
        self.speed = speed

    def update(self, ball_group):
        if self.rect.top < ball_group.sprite.rect.y:
            self.rect.y += self.speed
        if self.rect.bottom > ball_group.sprite.rect.y:
            self.rect.y -= self.speed
        self.action()

    def action(self):
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= screen_height: self.rect.bottom = screen_height

# Setup
pygame.mixer.pre_init(44000, -16, 2, 510)
pygame.init()
clock = pygame.time.Clock()

# Window Screen
screen_width = 1200
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ping Pong Game')

# Background Image
background = pygame.image.load('IMG/CircleGreenBg0.png')

# Background Music
mixer.music.load("SOUND/BoxCat-Games-Epic-Song.mp3")
mixer.music.play(-1)
mixer.music.set_volume(.2)

# Text Colors and Font
bg_color = pygame.Color('#2F373F')
accent_color = (200, 200, 200)
basic_font = pygame.font.Font('FONT/impact.ttf', 30)

# Sound Effects
block_sound = pygame.mixer.Sound("SOUND/Bounce.ogg")
pygame.mixer.Sound.set_volume(block_sound, .1)
score_sound = pygame.mixer.Sound("SOUND/Ping.ogg")
pygame.mixer.Sound.set_volume(score_sound, .1)
middle_strip = pygame.Rect(screen_width / 2 - 2, 0, 4, screen_height)

# Paddle Objects
player = Player('IMG/PaddleBlue.png', screen_width - 20, screen_height / 2, 5)
opponent = AI_Player('IMG/PaddleRed.png', 20, screen_width / 2, 5)
paddle_group = pygame.sprite.Group()
paddle_group.add(player)
paddle_group.add(opponent)

# Ball Object
ball = Ball('IMG/BallYellow.png', screen_width / 2, screen_height / 2, 4, 4, paddle_group)
ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

# game start up
game_setup = Game_Setup(ball_sprite, paddle_group)

# Events for keys and paddle movement
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Game window can exit
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN: # Press ESC to exit game anytime
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN: # Press Up or Down key to move Player
            if event.key == pygame.K_UP:
                player.movement -= player.speed
            if event.key == pygame.K_DOWN:
                player.movement += player.speed
        if event.type == pygame.KEYUP: # If Up or Down key is not press, Player stops
            if event.key == pygame.K_UP:
                player.movement += player.speed
            if event.key == pygame.K_DOWN:
                player.movement -= player.speed

    # Background Input
    screen.blit(background, [0, 0])
    pygame.draw.rect(screen, accent_color, middle_strip)

    # Run the game
    game_setup.run_game()

    # Render Input
    pygame.display.flip()
    clock.tick(60)