import pygame as pg
from pygame.locals import *
import time, random, sys

pg.init()
pg.font.init()

#set up the output screen
screen_width=960
screen_height=600
screen = pg.display.set_mode([screen_width, screen_height])
pg.display.set_caption('Snake Game by Shivani')
BackGround = Background('C:/Users/shiva/OneDrive/Documents/NYIT-MSDS-stuff/class-610-programming/Final-Project/Resources/bg-12.jpeg')


my_font = pg.font.SysFont('Calibri', 25, bold=True)
clock = pg.time.Clock()


# Define Colors 
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

class Background(pg.sprite.Sprite):
    def __init__(self, image_file):
        pg.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pg.image.load(image_file)
        screen.blit(pg.transform.scale(self.image, (800,600)), (0,0))
        pg.display.flip()   
        self.rect = self.image.get_rect()

# Score display
def show_score(choice, color):
    score_surface = my_font.render('Score: ' + str(score)  + '  &  Speed: ' + str(snake_speed), True, white)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (135, screen_height/1.05)
    else:
        score_rect.midtop = (screen_width/2, screen_height/1.25)
    screen.blit(score_surface, score_rect)

# Game Over
def gover():
    gover_surface = my_font.render('Game Over!', True, maroon)
    gover_rect = gover_surface.get_rect()
    gover_rect.midtop = (screen_width/2, screen_height/4)
    screen.blit(gover_surface, gover_rect)

    again = my_font.render("Play Again - Press 'P'",True, white)
    again_rect = again.get_rect()
    again_rect.midtop = (screen_width/2, screen_height/2.2)
    screen.blit(again, again_rect)

    game_quit = my_font.render("Quit - Press 'Q'",True, white)
    quit_rect = game_quit.get_rect()
    quit_rect.midtop = (screen_width/2, screen_height/2)
    screen.blit(game_quit, quit_rect)

    show_score(0, red)
    pg.display.flip()
    while True:
        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    pg.quit()
                    sys.exit()
                if event.key == pg.K_p:
                    main()
            elif event.type == pg.QUIT:
                pg.quit()
                sys.exit()

# Main logic
def main():
    global score, snake_speed
    score = 0

    #Snake inforamation
    snake_position = [100, 50]
    snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
    snake_speed = 10
    snake_direction = 'RIGHT'
    change_to = snake_direction

    # fruit position
    food_pos = [random.randrange(1, (screen_width//10)) * 10,
                    random.randrange(1, (screen_height//10)) * 10]
    food_spawn = True

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pg.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pg.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pg.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pg.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pg.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pg.K_ESCAPE:
                    pg.event.post(pg.event.Event(pg.QUIT))

        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'UP' and snake_direction != 'DOWN':
            snake_direction = 'UP'
        if change_to == 'DOWN' and snake_direction != 'UP':
            snake_direction = 'DOWN'
        if change_to == 'LEFT' and snake_direction != 'RIGHT':
            snake_direction = 'LEFT'
        if change_to == 'RIGHT' and snake_direction != 'LEFT':
            snake_direction = 'RIGHT'

        # Moving the snake
        if snake_direction == 'UP':
            snake_position[1] -= 10
        if snake_direction == 'DOWN':
            snake_position[1] += 10
        if snake_direction == 'LEFT':
            snake_position[0] -= 10
        if snake_direction == 'RIGHT':
            snake_position[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == food_pos[0] and snake_position[1] == food_pos[1]:
            score += 1
            if score%5 == 0:
                snake_speed += 2
            food_spawn = False
        else:
            snake_body.pop()

        # Spawning food on the screen
        if not food_spawn:
            food_pos = [random.randrange(1, (screen_width//10)) * 10, random.randrange(1, (screen_height//10)) * 10]
        food_spawn = True

        # GFX
        screen.blit(BackGround.image, BackGround.rect)
        BackGround.rect
        for pos in snake_body:
            # Snake body
            pg.draw.rect(screen, green, pg.Rect(pos[0], pos[1], 10, 10))

        # Snake food
        pg.draw.rect(screen, red, pg.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        # Getting out of bounds
        if snake_position[0] < 0 or snake_position[0] > screen_width-10:
            gover()
        if snake_position[1] < 0 or snake_position[1] > screen_height-10:
            gover()
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                gover()

        show_score(1, white)
        # Refresh game screen
        pg.display.update()
        # Refresh rate
        clock.tick(snake_speed)


if __name__ == '__main__':
    main()