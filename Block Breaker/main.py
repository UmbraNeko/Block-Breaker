import pygame, sys
from button import Button
import random

pygame.mixer.pre_init(44100, -16, 1, 512)

pygame.init()

pygame.mixer.music.load("music/main_music.mp3")

s_keydowm = pygame.mixer.Sound('music/keydown.mp3')
s_jump = pygame.mixer.Sound('music/jump.mp3')
s_lose_h = pygame.mixer.Sound('music/lose_h.mp3')
s_break = pygame.mixer.Sound('music/break.mp3')
s_level_1 = pygame.mixer.Sound('music/level_1.mp3')
s_level_2 = pygame.mixer.Sound('music/level_2.mp3')
s_level_3 = pygame.mixer.Sound('music/level_3.mp3')
s_victory = pygame.mixer.Sound('music/Victory.mp3')
s_game_over = pygame.mixer.Sound('music/GAME_OVER.mp3')
s_level_select = pygame.mixer.Sound('music/level_select.mp3')


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

HEIGHT = 720
WIDTH = 1280

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BLOCK BREAKER")

BACK_GROUND = pygame.image.load("assets/Background.png")

clock = pygame.time.Clock()
FPS = 30

class Striker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.speed = speed
        self.color = color
  
        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)
        self.striker = pygame.draw.rect(SCREEN, 
                               self.color, self.strikerRect)
  
    def display(self):
        self.striker = pygame.draw.rect(SCREEN, 
                            self.color, self.strikerRect)
  
    def update(self, xFac):
        self.posx += self.speed*xFac
  
        if self.posx <= 0:
            self.posx = 0
        elif self.posx+self.width >= WIDTH:
            self.posx = WIDTH-self.width
  
        self.strikerRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)
  
    def getRect(self):
        return self.strikerRect
class Block:
    def __init__(self, posx, posy, width, height, color):
        self.posx, self.posy = posx, posy
        self.width, self.height = width, height
        self.color = color
        self.damage = 100

        if color == RED:
            self.health = 300
        if color == WHITE:
            self.health = 200
        if color == GREEN:
            self.health = 100
  
        self.blockRect = pygame.Rect(
            self.posx, self.posy, self.width, self.height)
        self.block = pygame.draw.rect(SCREEN, self.color, 
                                      self.blockRect)
  
    def display(self):
        if self.health > 0:
            self.brick = pygame.draw.rect(SCREEN, 
                                self.color, self.blockRect)
  
    def hit(self):
        self.health -= self.damage
        s_jump.play()
        if self.health == 0:
            s_break.play()
  
    def getRect(self):
        return self.blockRect
  
    def getHealth(self):
        return self.health
class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx, self.posy = posx, posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac, self.yFac = 1, 1
  
        self.ball = pygame.draw.circle(
            SCREEN, self.color, (self.posx,
                                 self.posy), self.radius)
  
    def display(self):
        self.ball = pygame.draw.circle(
            SCREEN, self.color, (self.posx, 
                                 self.posy), self.radius)
  
    def update(self):
        self.posx += self.xFac*self.speed
        self.posy += self.yFac*self.speed
  
        if self.posx <= 0 or self.posx >= WIDTH:
            self.xFac *= -1
  
        if self.posy <= 0:
            self.yFac *= -1
  
        if self.posy >= HEIGHT:
            return True
  
        return False
  
    def reset(self):
        self.posx = 0
        self.posy = HEIGHT
        self.xFac, self.yFac = 1, -1
  
    def hit(self):
        self.yFac *= -1
  
    def getRect(self):
        return self.ball

def GAME(level):
    if level == 1:
        s_level_1.play(-1)
    if level == 2:
        s_level_2.play(-1)
    if level == 3:  
        s_level_3.play(-1)

    running = True
    lives = 3
    score = 0
  
    scoreText = get_font(20).render("score", True, WHITE)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.center = (80, HEIGHT-160)
  
    livesText = get_font(20).render("Lives", True, WHITE)
    livesTextRect = livesText.get_rect()
    livesTextRect.center = (80, HEIGHT-200)
  
    striker = Striker(0, HEIGHT-50, 100, 20, 10, WHITE)
    strikerXFac = 0
  
    ball = Ball(0, HEIGHT-150, 7, 5, WHITE)
  
    blockWidth, blockHeight = 40, 15
    horizontalGap, verticalGap = 20, 20
    if level == 0:
        listOfBlocks = populateBlocks(0, blockWidth, blockHeight, horizontalGap, verticalGap)
    if level == 1:
        listOfBlocks = populateBlocks(1, blockWidth, blockHeight, horizontalGap, verticalGap)
    if level == 2:
        listOfBlocks = populateBlocks(2, blockWidth, blockHeight, horizontalGap, verticalGap)
    if level == 3:
        listOfBlocks = populateBlocks(3, blockWidth, blockHeight, horizontalGap, verticalGap)
    
    # Game loop
    while running:
        SCREEN.fill(BLACK)
        SCREEN.blit(scoreText, scoreTextRect)
        SCREEN.blit(livesText, livesTextRect)
  
        scoreText = get_font(20).render("Score : " + str(score), True, WHITE)
        livesText = get_font(20).render("Lives : " + str(lives), True, WHITE)
  
        # If all the blocks are destroyed, the Victory() function is called
        if not listOfBlocks:
            Victory(level, score)
    
  
        # All the lives are over. So, the gameOver() function is called
        if lives <= 0:
            running = False
            gameOver(level, score)
            while listOfBlocks:
                listOfBlocks.pop(0) 
  
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    strikerXFac = -1
                if event.key == pygame.K_RIGHT:
                    strikerXFac = 1
                if event.key == pygame.K_p:
                    pause(level)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    strikerXFac = 0
  
        # Collision check
        if(collisionChecker(striker.getRect(),
                            ball.getRect())):
            ball.hit()
        for block in listOfBlocks:
            if(collisionChecker(block.getRect(), ball.getRect())):
                ball.hit()
                block.hit()
  
                if block.getHealth() <= 0:
                    if block.color == GREEN:
                        listOfBlocks.pop(listOfBlocks.index(block))
                        score += 5
                    if block.color == WHITE:
                        listOfBlocks.pop(listOfBlocks.index(block))
                        score += 10
                    if block.color == RED:
                        listOfBlocks.pop(listOfBlocks.index(block))
                        score += 20
  
        # Update
        striker.update(strikerXFac)
        lifeLost = ball.update()
  
        if lifeLost:
            lives -= 1
            s_lose_h.play()
            ball.reset()
            print(lives)
  
        # Display
        striker.display()
        ball.display()
  
        for block in listOfBlocks:
            block.display()
  
        pygame.display.update()
        clock.tick(FPS)
    

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)
def collisionChecker(rect, ball):
    if pygame.Rect.colliderect(rect, ball):
        return True
    
    return False
def populateBlocks(level, blockWidth, blockHeight, 
                   horizontalGap, verticalGap):
    listOfBlocks = []
    
    #test level
    if level == 0:
        listOfBlocks.append(Block(1280-(40*20-40+220), 15*21+100, blockWidth, blockHeight, 
                GREEN))
        return listOfBlocks
        
    if level == 1:

        for i in range(1, 21):
            listOfBlocks.append(Block(40*i+220, 15*i+100, blockWidth, blockHeight, 
                WHITE))
            listOfBlocks.append(Block(1280-(40*i+220), 15*i+100, blockWidth, blockHeight, 
                WHITE))
            listOfBlocks.append(Block(40*i+40+220, 15*i+100, blockWidth, blockHeight, 
                GREEN))
            listOfBlocks.append(Block(1280-(40*i+40+220), 15*i+100, blockWidth, blockHeight, 
                GREEN))
            listOfBlocks.append(Block(40*i-40+220, 15*i+100, blockWidth, blockHeight, 
                GREEN))
            listOfBlocks.append(Block(1280-(40*i-40+220), 15*i+100, blockWidth, blockHeight, 
                GREEN))
        return listOfBlocks
    
    if level == 2:

        for i in range(0, 20):
            for j in range(0, 2):
                listOfBlocks.append(Block(40*i+220, 15*j+15+100, blockWidth, blockHeight, 
                    WHITE))
                if i <= 8:
                    listOfBlocks.append(Block((40*i+220)*2-160, (15*j+15+100)*2, blockWidth, blockHeight, 
                        GREEN))
                listOfBlocks.append(Block(40*i+220, 15*j+15+15*16+100, blockWidth, blockHeight, 
                    WHITE))
        for i in range(0, 14):
            listOfBlocks.append(Block(220, 15*i+45+100, blockWidth, blockHeight, 
                WHITE))
            listOfBlocks.append(Block(1280-(80+220), 15*i+45+100, blockWidth, blockHeight, 
                WHITE))

        return listOfBlocks
    if level == 3:

        for i in range(40, WIDTH-40, blockWidth+horizontalGap):
            for j in range(15, HEIGHT//2-15, blockHeight+verticalGap):
                listOfBlocks.append(
                    Block(i, j, blockWidth, blockHeight, 
                        random.choice([WHITE, GREEN, RED])))
        return listOfBlocks
def pause(level):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                if event.key == pygame.K_q:
                    if level == 1:
                        s_level_1.stop()
                    if level == 2:
                        s_level_2.stop()
                    if level == 3:  
                        s_level_3.stop()
                    play()
        SCREEN.fill(WHITE)
        Pause_TEXT = get_font(90).render("Paused", True, "#b68f40")
        Pause_RECT = Pause_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(Pause_TEXT, Pause_RECT)
        Press_TEXT = get_font(20).render("Press C to continue or Q to quit.", True, "#b68f40")
        Press_RECT = Press_TEXT.get_rect(center=(640, 500))
        SCREEN.blit(Press_TEXT, Press_RECT)

        pygame.display.update()
        clock.tick(FPS)

def gameOver(level, score):
    if level == 1:
        s_level_1.stop()
    if level == 2:
        s_level_2.stop()
    if level == 3:  
        s_level_3.stop()

    s_game_over.play()
    highscore_write(score, level)
    gameOver = True
    while gameOver:
        SCREEN.fill("black")
        MENU_TEXT = get_font(90).render("GAME OVER", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        scoreText = get_font(45).render("Score : " + str(score), True, WHITE)
        scoreTextRect = scoreText.get_rect()
        scoreTextRect.center = (640, HEIGHT-400)
        SCREEN.blit(scoreText, scoreTextRect)


        Try_again =  Button(image=None, pos=(640, 500), 
                            text_input="Try again", font=get_font(45), base_color="RED", hovering_color="Green")
        Try_again.changeColor(pygame.mouse.get_pos())
        Try_again.update(SCREEN)

        PLAY_BACK = Button(image=None, pos=(640, 600), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(pygame.mouse.get_pos())
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Try_again.checkForInput(pygame.mouse.get_pos()):
                    s_keydowm.play()
                    GAME(level)
                if PLAY_BACK.checkForInput(pygame.mouse.get_pos()):
                    s_keydowm.play()
                    play()
        pygame.display.update()
        clock.tick(FPS)
def Victory(level, score):
    if level == 1:
        s_level_1.stop()
    if level == 2:
        s_level_2.stop()
    if level == 3:  
        s_level_3.stop()

    s_victory.play()
    Victory = True
    while Victory:

        SCREEN.fill("black")
        Victory_TEXT = get_font(90).render("Victory", True, "#b68f40")
        Victory_RECT = Victory_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(Victory_TEXT, Victory_RECT)
        
        scoreText = get_font(45).render("Score : " + str(score), True, WHITE)
        scoreTextRect = scoreText.get_rect()
        scoreTextRect.center = (640, HEIGHT-400)
        SCREEN.blit(scoreText, scoreTextRect)

        if level<3:
            Next_level =  Button(image=None, pos=(640, 500), 
                            text_input="Next level", font=get_font(45), base_color="RED", hovering_color="Green")
            Next_level.changeColor(pygame.mouse.get_pos())
            Next_level.update(SCREEN)
        else:
            Next_level = 0
        PLAY_BACK = Button(image=None, pos=(640, 600), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(pygame.mouse.get_pos())
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level < 3:
                    if Next_level.checkForInput(pygame.mouse.get_pos()):
                        s_keydowm.play()
                        GAME(level+1)
                if PLAY_BACK.checkForInput(pygame.mouse.get_pos()):
                    s_keydowm.play()
                    main_menu()
        pygame.display.update()
        clock.tick(FPS)
def play():
    s_level_select.play(-1)
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("SELECT A LEVEL", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 50))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_LEVEL_0 = Button(image=None, pos=(640, 150), 
                            text_input="LEVEL 0", font=get_font(45), base_color="White", hovering_color="Green")
        PLAY_LEVEL_1 = Button(image=None, pos=(640, 250), 
                            text_input="LEVEL 1", font=get_font(45), base_color="White", hovering_color="Green")
        PLAY_LEVEL_2 = Button(image=None, pos=(640, 350), 
                            text_input="LEVEL 2", font=get_font(45), base_color="White", hovering_color="Green")
        PLAY_LEVEL_3 = Button(image=None, pos=(640, 450), 
                            text_input="LEVEL 3", font=get_font(45), base_color="White", hovering_color="Green")
        
        PLAY_LEVEL_0.changeColor(PLAY_MOUSE_POS)
        PLAY_LEVEL_0.update(SCREEN)
        PLAY_LEVEL_1.changeColor(PLAY_MOUSE_POS)
        PLAY_LEVEL_1.update(SCREEN)
        PLAY_LEVEL_2.changeColor(PLAY_MOUSE_POS)
        PLAY_LEVEL_2.update(SCREEN)
        PLAY_LEVEL_3.changeColor(PLAY_MOUSE_POS)
        PLAY_LEVEL_3.update(SCREEN)


        PLAY_BACK = Button(image=None, pos=(640, 600), 
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_LEVEL_0.checkForInput(PLAY_MOUSE_POS):
                    s_level_select.stop()
                    s_keydowm.play()
                    GAME(0)
                if PLAY_LEVEL_1.checkForInput(PLAY_MOUSE_POS):
                    s_level_select.stop()
                    s_keydowm.play()
                    GAME(1)
                if PLAY_LEVEL_2.checkForInput(PLAY_MOUSE_POS):
                    s_level_select.stop()
                    s_keydowm.play()
                    GAME(2)
                if PLAY_LEVEL_3.checkForInput(PLAY_MOUSE_POS):
                    s_level_select.stop()
                    s_keydowm.play()
                    GAME(3)
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    s_level_select.stop()
                    s_keydowm.play()
                    main_menu()

        pygame.display.update()
    pygame.quit()   
def table():
    highscore_sort()
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")
        file = open("assets/highscore.txt", "r+")         
        content = []
        for line in file:
            content.append(line) 
        for i in range(0, 5):
            TABLE_TEXT = get_font(45).render(content[i][0:-1], True, "Black")
            TABLE_RECT = TABLE_TEXT.get_rect(center=(640, 100+ i*100))
            SCREEN.blit(TABLE_TEXT, TABLE_RECT)

        TABLE_BACK = Button(image=None, pos=(640, 660), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        TABLE_BACK.changeColor(OPTIONS_MOUSE_POS)
        TABLE_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TABLE_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    s_keydowm.play()
                    main_menu()

        pygame.display.update()
def main_menu():
    pygame.mixer.music.play(-1)
    while True:
        SCREEN.blit(BACK_GROUND, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(90).render("BLOCK BREAKER", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        TABLE_OF_HIGHSCORE_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400), 
                            text_input="TABLE", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, TABLE_OF_HIGHSCORE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.music.stop()
                    s_keydowm.play()
                    play()
                if TABLE_OF_HIGHSCORE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    s_keydowm.play()
                    table()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
def highscore_write(score, level):
    file = open("assets/highscore.txt", "r+")   

    to_new = "SCORE: " + str(score) + ', ' + "LEVEL: " + str(level) + "\n"
    print(to_new)   
    if not to_new in file:
        file.write(to_new)
    file.close()
def highscore_sort():
    file = open("assets/highscore.txt", "r+")         
    content = []
    strok = 0
    for line in file:
        content.append(line)
        strok += 1
    for i in range(0, strok):
        print(content[i].split(",")[0].split(" ")[-1])
    for i in range(strok-1):
        for j in range(strok-i-1):
            if int(content[j].split(",")[0].split(" ")[-1]) < int(content[j+1].split(",")[0].split(" ")[-1]):
                content[j], content[j+1] = content[j+1], content[j]
    print()
    file.close()
    file = open("assets/highscore.txt", "r")
    file.close()
    file = open("assets/highscore.txt", "r+")
    for i in range(0, strok):
        file.write(content[i])
    file.close()                                                               
main_menu()

