import pygame
import os
import random
import copy
pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
       pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
        pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png")) #배경

#Strategy 패턴
#Stategy
class DinosaurStrategy:
    def userinput(self, dinosaur, userInput):
        pass

#Concrete Strategy1
class RunningStrategy(DinosaurStrategy):
    def userinput(self, dinosaur, userInput):
        dinosaur.run()

#Concrete Strategy2
class DuckingStrategy(DinosaurStrategy):
    def userinput(self, dinosaur, userInput):
        dinosaur.duck()

#Concrete Strategy3
class JumpingStrategy(DinosaurStrategy):
    def userinput(self, dinosaur, userInput):
        dinosaur.jump()

#API
class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.strategy = RunningStrategy()

    def update(self, userInput):
        if self.dino_jump:
            self.strategy = JumpingStrategy()
        elif userInput[pygame.K_DOWN]:
            self.strategy = DuckingStrategy()
        else:
            self.strategy = RunningStrategy()

        self.strategy.userinput(self, userInput)

        if self.step_index >= 10:
            self.step_index = 0

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

#Factory 패턴 -> 장애물 객체 생성
class ObstacleFactory:
    @staticmethod
    def create_obstacle(obstacle_type):
        if obstacle_type == "small_cactus":
            return SmallCactus(SMALL_CACTUS)
        elif obstacle_type == "large_cactus":
            return LargeCactus(LARGE_CACTUS)
        elif obstacle_type == "bird":
            return Bird(BIRD)
        else:
            raise ValueError(f"Unknown obstacle type: {obstacle_type}")

#Prototype 패턴 -> 새로운 장애물 생성
class Prototype:
    def clone(self):
        return copy.deepcopy(self)

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
            del self

    def draw(self, SCREEN):
        # pygame.draw.rect(SCREEN, (0, 0, 0), self.rect, 2)
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle, Prototype):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle, Prototype):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle, Prototype):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000) #구름의 x,y좌표
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self): #move right to left
        self.x -= game_speed #구름 이미지의 x좌표에서 game_speed인 14씩 감소함
        if self.x < -self.width:
            #ex) self.width가 100이고 x좌표가 0이면 구름의 오른쪽 끝은 x+self.width=100
            #    x좌표가 -100(-self.width)이면 구름의 오른쪽 끝은 -100+self.width=0이므로 전체 이미지가 화면 밖으로 사라짐을 의미 
            self.x = SCREEN_WIDTH + random.randint(1000, 1600) #구름 이미지 좌표 reset
            self.y = random.randint(50, 100)

    def draw(self, SCREEN): #화면에 구름 출력
        SCREEN.blit(self.image, (self.x, self.y))

def main():
    global obstacles, game_speed, x_pos_bg, y_pos_bg, points
    run = True
    font = pygame.font.Font('freesansbold.ttf', 15)
    clock = pygame.time.Clock()
    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 14
    points = 0
    player = Dinosaur()
    clouds = []
    obstacles = []
    death_count = 0

    for i in range(0, 2):
        clouds.append(Cloud())

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        background()
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            obstacle_type = random.choice(["small_cactus", "large_cactus", "bird"])
            new_obstacle = ObstacleFactory.create_obstacle(obstacle_type)
            obstacles.append(new_obstacle)

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.dino_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        for cloud in clouds:
            cloud.draw(SCREEN)
            cloud.update()

        score()

        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH//2-20, SCREEN_HEIGHT//2-140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()

menu(death_count=0) #게임 시작 화면