import pygame
import sys

pygame.init()

# configurations
window_height = 500
window_width = 700

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# creating window
display = pygame.display.set_mode((window_width, window_height))

# creating our frame regulator
clock = pygame.time.Clock()

pygame.display.set_caption("Pong")

PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_RADIUS = 10
WINNING_SCORE = 10

SCORE_FONT = pygame.font.SysFont("comicsans", 50)

class Ball:
    COLOR = WHITE
    MAX_VELOCITY = 5
    
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VELOCITY
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
    
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1



class Paddle:
    COLOR = WHITE
    VELOCITY = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height
    
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY
        
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

def handle_paddle_movement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w]:
        if(left_paddle.y == 0):
            return
        left_paddle.move(True)
    if keys[pygame.K_s]:
        if(left_paddle.y + PADDLE_HEIGHT == window_height):
            return
        left_paddle.move(False)

    if keys[pygame.K_UP]:
        if(right_paddle.y == 0):
            return
        right_paddle.move(True)
    if keys[pygame.K_DOWN]:
        if(right_paddle.y + PADDLE_HEIGHT == window_height):
            return
        right_paddle.move(False)

def handle_ball_collision(left_paddle, right_paddle, ball):
    if ball.y + ball.radius  >= window_height:
        ball.y_vel *= -1
    elif ball.y - ball.radius  <= 0:
        ball.y_vel *= -1

    #check collision w left paddle
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1
                
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height/2) / ball.MAX_VELOCITY
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel * -1

    else: #right paddle
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x - right_paddle.width:
                ball.x_vel *= -1
                
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height/2) / ball.MAX_VELOCITY
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel * -1



# draw method, deals with the grahics
def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (window_width//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (window_width*3//4 - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)
    
    ball.draw(win)
    
    pygame.display.update()

# main loop
def main():
    left_paddle = Paddle(0, window_height//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(window_width-PADDLE_WIDTH, window_height//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    game_ball = Ball(window_width/2, window_height/2, BALL_RADIUS)
    left_score = 0
    right_score = 0


    while True:
        clock.tick(60)
        draw(display, [left_paddle, right_paddle], game_ball, left_score, right_score)

        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        game_ball.move()
        handle_ball_collision(left_paddle, right_paddle, game_ball)

        if game_ball.x < 0:
            right_score += 1
            game_ball.reset()
        elif game_ball.x > window_width:
            left_score += 1
            game_ball.reset()

        won = False
        if right_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif left_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"
        
        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            display.blit(text, (window_width//2 - text.get_width()//2, window_height//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            game_ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score, right_score = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    
    
    

main()

