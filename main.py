import random
import sys

import pygame

pygame.init()
RESOLUTION = (WIDTH, HEIGHT) = (1200, 300)
SCREEN = pygame.display.set_mode(RESOLUTION)
SPRITE = pygame.image.load("sprite.png").convert_alpha()
LOGO = SPRITE.subsurface(2, 2, 72, 64)
GROUND = SPRITE.subsurface(2, 98, 1200, 34)
INC = SPRITE.subsurface(185, 2, 91, 80)
SINKO = SPRITE.subsurface(278, 2, 80, 70)
NUMBERS = (
    SPRITE.subsurface(360, 2, 18, 21),
    SPRITE.subsurface(382, 2, 16, 21),
    SPRITE.subsurface(400, 2, 18, 21),
    SPRITE.subsurface(420, 2, 18, 21),
    SPRITE.subsurface(440, 2, 18, 21),
    SPRITE.subsurface(460, 2, 18, 21),
    SPRITE.subsurface(480, 2, 18, 21),
    SPRITE.subsurface(500, 2, 18, 21),
    SPRITE.subsurface(520, 2, 18, 21),
    SPRITE.subsurface(540, 2, 19, 21),
)
FIRST = SPRITE.subsurface(360, 56, 59, 21)
SECOND = SPRITE.subsurface(423, 56, 62, 21)
THIRD = SPRITE.subsurface(489, 56, 64, 21)
GAMEOVER = SPRITE.subsurface(360, 29, 381, 21)
ISKO = (
    SPRITE.subsurface(743, 2, 71, 94),
    SPRITE.subsurface(816, 2, 71, 94),
    SPRITE.subsurface(962, 2, 71, 94),
    SPRITE.subsurface(889, 2, 71, 94),
    SPRITE.subsurface(1035, 28, 71, 68),
    SPRITE.subsurface(1108, 28, 71, 68),
    SPRITE.subsurface(1181, 2, 71, 94),
)
BACKGROUND = SPRITE.subsurface(2, 134, 1200, 250)
BACKGROUND.set_alpha(64)
BGCOLOR = (230, 230, 230)
pygame.display.set_icon(LOGO)
pygame.display.set_caption("Isko Runner")


class Isko:
    def __init__(self):
        self.image = ISKO[6]
        self.image_index = 0
        self.running = True
        self.ducking = False
        self.jumping = False
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 186
        self.rect.width -= 15
        self.velocity = self.gravity = 15

    def run(self):
        self.image = ISKO[:4][self.image_index // 2]
        self.image_index += 1

    def duck(self):
        self.image = ISKO[4:6][self.image_index // 4]
        self.image_index += 1

    def jump(self):
        self.image = ISKO[2]
        if self.jumping:
            self.rect.y -= self.velocity
            self.velocity -= 1
        if self.velocity < -self.gravity:
            self.velocity = self.gravity
            self.jumping = False

    def cry(self):
        if self.ducking:
            self.rect.y = 186
        self.image = ISKO[6]

    def switch(self, run_switch, duck_switch, jump_switch):
        self.running = run_switch
        self.ducking = duck_switch
        self.jumping = jump_switch

    def update(self, key):
        if (key[pygame.K_UP] or key[pygame.K_SPACE]) and not self.jumping:
            if key[pygame.K_DOWN]:
                self.rect.y = 186
            self.switch(False, False, True)
        elif key[pygame.K_DOWN] and not self.jumping:
            self.rect.y = 212
            self.switch(False, True, False)
        elif not self.jumping:
            self.rect.y = 186
            self.switch(True, False, False)
        if self.ducking:
            self.duck()
        elif self.running:
            self.run()
        elif self.jumping:
            self.jump()
        if self.image_index >= len(ISKO):
            self.image_index = 0

    def draw(self):
        SCREEN.blit(self.image, self.rect)


class Obstacle:
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.velocity = -10
        self.out = False

    def update(self):
        self.rect.x += self.velocity
        if self.rect.x < -(self.rect.width):
            self.out = True

    def draw(self):
        SCREEN.blit(self.image, self.rect)
        self.update()


class Sinko(Obstacle):
    def __init__(self):
        super().__init__(SINKO)
        self.rect.y = 209


class Incomplete(Obstacle):
    def __init__(self):
        super().__init__(INC)
        self.rect.y = 124


class Ground:
    def __init__(self):
        self.image0 = self.image1 = GROUND
        self.rect0 = self.image0.get_rect()
        self.rect1 = self.image1.get_rect()
        self.rect0.bottom = self.rect1.bottom = 300
        self.rect1.left = self.rect0.right
        self.velocity = -10

    def update(self):
        self.rect0.left += self.velocity
        self.rect1.left += self.velocity
        if self.rect0.right < 0:
            self.rect0.left = self.rect1.right
        if self.rect1.right < 0:
            self.rect1.left = self.rect0.right

    def draw(self):
        SCREEN.blit(self.image0, self.rect0)
        SCREEN.blit(self.image1, self.rect1)
        self.update()


class Scoreboard:
    def __init__(self):
        self.score = 0
        self.score_str = str(self.score)
        self.score_list = []
        try:
            with open("leaderboard.txt") as leaderboard:
                for entry in leaderboard:
                    self.score_list.append(entry.replace("\n", ""))
        except FileNotFoundError:
            with open("leaderboard.txt", "w") as leaderboard:
                for _ in range(3):
                    leaderboard.write("00000\n")
                    self.score_list.append("00000")

    def first(self):
        SCREEN.blit(FIRST, (407, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[0][0])], (492, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[0][1])], (513, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[0][2])], (536, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[0][3])], (558, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[0][4])], (580, 20))

    def second(self):
        SCREEN.blit(SECOND, (624, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[1][0])], (712, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[1][1])], (734, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[1][2])], (756, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[1][3])], (778, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[1][4])], (800, 20))

    def third(self):
        SCREEN.blit(THIRD, (844, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[2][0])], (934, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[2][1])], (956, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[2][2])], (978, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[2][3])], (1000, 20))
        SCREEN.blit(NUMBERS[int(self.score_list[2][4])], (1022, 20))

    def current(self):
        self.score_str = str(int(self.score)).rjust(5, "0")
        SCREEN.blit(NUMBERS[int(self.score_str[0])], (1068, 20))
        SCREEN.blit(NUMBERS[int(self.score_str[1])], (1090, 20))
        SCREEN.blit(NUMBERS[int(self.score_str[2])], (1112, 20))
        SCREEN.blit(NUMBERS[int(self.score_str[3])], (1134, 20))
        SCREEN.blit(NUMBERS[int(self.score_str[4])], (1156, 20))

    def increment(self):
        if self.score < 99999:
            self.score += 0.1

    def update(self):
        self.score_str = str(int(self.score)).rjust(5, "0")
        if self.score_str > self.score_list[0]:
            self.score_list[2] = self.score_list[1]
            self.score_list[1] = self.score_list[0]
            self.score_list[0] = self.score_str
        elif self.score_str > self.score_list[1]:
            self.score_list[2] = self.score_list[1]
            self.score_list[1] = self.score_str
        elif self.score_str > self.score_list[2]:
            self.score_list[2] = self.score_str
        with open("leaderboard.txt", "w") as leaderboard:
            for score_str in self.score_list:
                leaderboard.write(f"{score_str}\n")

    def draw(self):
        self.first()
        self.second()
        self.third()
        self.current()


def gamestart():
    scoreboard = Scoreboard()
    while True:
        SCREEN.fill(BGCOLOR)
        SCREEN.blit(BACKGROUND, (0, 61))
        SCREEN.blit(GROUND, (0, 266))
        SCREEN.blit(ISKO[0], (50, 186))
        scoreboard.draw()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in [
                pygame.K_SPACE,
                pygame.K_UP,
            ]:
                gameplay()
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()


def gameplay():
    player = Isko()
    obstacle = Sinko()
    ground = Ground()
    scoreboard = Scoreboard()
    clock = pygame.time.Clock()
    FPS = 30
    while True:
        SCREEN.fill(BGCOLOR)
        SCREEN.blit(BACKGROUND, (0, 61))
        ground.draw()
        if obstacle.out:
            obstacle = Sinko() if random.randint(0, 4) else Incomplete()
        else:
            obstacle.draw()
        if player.rect.colliderect(obstacle.rect):
            scoreboard.update()
            gameover(player, scoreboard)
        else:
            scoreboard.increment()
            scoreboard.draw()
        player.draw()
        player.update(pygame.key.get_pressed())
        clock.tick(FPS)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()


def gameover(player, scoreboard):
    while True:
        SCREEN.blit(GAMEOVER, ((WIDTH - 381) / 2, 83))
        SCREEN.blit(LOGO, ((WIDTH - 72) / 2, 148))
        player.cry()
        player.draw()
        scoreboard.draw()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key in [
                pygame.K_SPACE,
                pygame.K_UP,
            ]:
                gameplay()
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()


def main():
    gamestart()


if __name__ == "__main__":
    main()
