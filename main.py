import pygame
import random
import os
import sys


pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Balloon")
FPS = 60
level = 0
score = 0
font = pygame.font.SysFont(None, 30)
clock = pygame.time.Clock()
iteration = 0
collided = 0
explosion_frame = 0


def load_best_score():
    try:
        with open('data/best_score.txt', 'r') as file:
            s = file.read().strip()
            if s:
                return int(s)
            return 0
    except FileNotFoundError:
        return 0


def save_best_score(new_best_score):
    with open('data/best_score.txt', 'w') as file:
        file.write(str(new_best_score))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


balloon_img = pygame.transform.scale(load_image("balloon.png"), (75, 75))
background_images = [pygame.transform.scale(load_image("ocean1.png"), (WIDTH, HEIGHT)),
                     pygame.transform.scale(load_image("ocean2.png"), (WIDTH, HEIGHT)),
                     pygame.transform.scale(load_image("ocean3.png"), (WIDTH, HEIGHT)),
                     pygame.transform.scale(load_image("ocean4.png"), (WIDTH, HEIGHT)),
                     pygame.transform.scale(load_image("ocean5.png"), (WIDTH, HEIGHT))]


class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = balloon_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.mask = pygame.mask.from_surface(self.image)
        self.prev_mouse_pos = pygame.mouse.get_pos()

    def change_image(self, img):
        self.image = img

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.centerx -= 5
        elif keys[pygame.K_RIGHT]:
            self.rect.centerx += 5
        else:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos != self.prev_mouse_pos:
                mouse_x, _ = pygame.mouse.get_pos()
                self.rect.centerx = mouse_x
            self.prev_mouse_pos = mouse_pos

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH


balloon = Balloon()


class Cloud(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()

        w, h = load_image("cloud_shape_5.png").get_size()

        self.frames = [pygame.transform.scale(load_image("cloud_shape_1.png"), (w, h)),
                       pygame.transform.scale(load_image("cloud_shape_2.png"), (w, h)),
                       pygame.transform.scale(load_image("cloud_shape_3.png"), (w, h)),
                       pygame.transform.scale(load_image("cloud_shape_4.png"), (w, h)),
                       pygame.transform.scale(load_image("cloud_shape_5.png"), (w, h)),
                       pygame.transform.scale(load_image("cloud_shape_4.png"), (w, h)),
                       pygame.transform.scale(load_image("cloud_shape_3.png"), (w, h)),
                       pygame.transform.scale(load_image("cloud_shape_2.png"), (w, h))]

        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = 0
        self.speed_y = speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global collided, score, explosion_frame
        if not collided:
            self.rect.y += self.speed_y

        if iteration % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        if self.rect.top > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            score += 1
        if pygame.sprite.collide_mask(self, balloon):
            collided += 1

        if collided:
            frames = [pygame.transform.scale(load_image("Explosion_1.png"), (100, 100)),
                      pygame.transform.scale(load_image("Explosion_2.png"), (100, 100)),
                      pygame.transform.scale(load_image("Explosion_3.png"), (100, 100)),
                      pygame.transform.scale(load_image("Explosion_4.png"), (100, 100)),
                      pygame.transform.scale(load_image("Explosion_1.png"), (100, 100))]
            if iteration % 5 == 0:
                explosion_frame += 1
                balloon.change_image(frames[explosion_frame % 5])


all_sprites = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites.add(balloon)


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global level
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(pygame.transform.scale(load_image("fon.png"), (WIDTH, HEIGHT)), (0, 0))

        font = pygame.font.SysFont(None, 30)

        rules = font.render("Escape clouds!", True, (29, 41, 81))
        screen.blit(rules, (WIDTH // 2 - rules.get_width() // 2, HEIGHT // 2 - 150))

        choose_level_text = font.render("Choose level", True, (29, 41, 81))
        screen.blit(choose_level_text, (WIDTH // 2 - choose_level_text.get_width() // 2,
                                        HEIGHT // 2 - 75))

        level_buttons = []
        for i in range(5):
            button_rect = pygame.Rect(WIDTH // 2 - 270 + i * 120,
                                      HEIGHT // 2 - 30, 50, 50)
            button_color = (0, 128, 129)
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                button_color = (0, 100, 100)
            pygame.draw.rect(screen, button_color, button_rect)
            button_text = font.render(str(i + 1), True, (29, 41, 81))
            screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                                      button_rect.centery - button_text.get_height() // 2))
            level_buttons.append(button_rect)

        best_score_text = font.render("Рекорд: " + str(load_best_score()), True, (29, 41, 81))
        screen.blit(best_score_text, (WIDTH // 2 - best_score_text.get_width() // 2,
                                      HEIGHT // 2 + 75))

        pygame.display.update()
        clock.tick(15)

        mouse_pos = pygame.mouse.get_pos()
        for i, button_rect in enumerate(level_buttons):
            if button_rect.collidepoint(mouse_pos):
                if pygame.mouse.get_pressed()[0]:
                    level = i + 1
                    intro = False


start_screen()
cloud_speed = 1 + level * 2
background_img = background_images[level - 1]


def game_over_screen():
    game_over = True
    if score > load_best_score():
        save_best_score(score)

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        screen.blit(background_img, (0, 0))

        font = pygame.font.SysFont(None, 50)
        game_over_text = font.render("Game over", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2,
                                     HEIGHT // 4 - game_over_text.get_height() // 2))
        score_text = font.render("Score: " + str(score), True, (29, 41, 81))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2,
                                 HEIGHT // 4 + 50))

        restart_button_rect = pygame.Rect(WIDTH // 2 - 100,
                                          HEIGHT // 4 + 100, 200, 50)
        button_color = (0, 128, 129)
        if restart_button_rect.collidepoint(pygame.mouse.get_pos()):
            button_color = (0, 100, 100)
        pygame.draw.rect(screen, button_color, restart_button_rect)
        restart_text = font.render("Replay", True, (29, 41, 81))
        screen.blit(restart_text, (restart_button_rect.centerx - restart_text.get_width() // 2,
                                   restart_button_rect.centery - restart_text.get_height() // 2))

        choose_level_button_rect = pygame.Rect(WIDTH // 2 - 125,
                                               HEIGHT // 4 + 175, 250, 50)
        button_color = (0, 128, 129)
        if choose_level_button_rect.collidepoint(pygame.mouse.get_pos()):
            button_color = (0, 100, 100)
        pygame.draw.rect(screen, button_color, choose_level_button_rect)
        choose_level_text = font.render("Choose level", True, (29, 41, 81))
        screen.blit(choose_level_text, (choose_level_button_rect.centerx - choose_level_text.get_width() // 2,
                                        choose_level_button_rect.centery - choose_level_text.get_height() // 2))

        font = pygame.font.SysFont(None, 30)
        best_score_text = font.render("Best score: " + str(load_best_score()), True, (29, 41, 81))
        screen.blit(best_score_text, (WIDTH // 2 - best_score_text.get_width() // 2,
                                      HEIGHT // 4 + 275))

        pygame.display.update()
        clock.tick(15)

        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if restart_button_rect.collidepoint(mouse_pos) or any(keys):
            if pygame.mouse.get_pressed()[0] or any(keys):
                game_over = False
        elif choose_level_button_rect.collidepoint(mouse_pos) or any(keys):
            if pygame.mouse.get_pressed()[0] or any(keys):
                game_over = False
                start_screen()


running = True

while running:
    screen.blit(background_img, (0, 0))

    iteration = (iteration + 1) % 1000000000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if random.randint(1, 150) < 3:
        cloud = Cloud(cloud_speed)
        all_sprites.add(cloud)
        clouds.add(cloud)

    all_sprites.update()
    if collided > 0 and explosion_frame > 40:
        collided = 0
        explosion_frame = 0
        game_over_screen()
        balloon = Balloon()
        all_sprites = pygame.sprite.Group()
        clouds = pygame.sprite.Group()
        all_sprites.add(balloon)
        score = 0
        cloud_speed = 1 + level * 2
        background_img = background_images[level - 1]

    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    all_sprites.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

terminate()