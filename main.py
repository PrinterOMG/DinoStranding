import pygame
import random
from os import path
import sys

player_sprite_toggle = True
music_sounds_toggle = False

if music_sounds_toggle:
    snd_dir = path.join(path.dirname(r'data/sounds'), 'sounds')

# noinspection PyBroadException
try:
    save_file = open("save.txt", "r")
    high_score = int(save_file.read())
    save_file.close()
except Exception:
    save_file = open("save.txt", "w")
    high_score = 0
    save_file.write("0")
    save_file.close()


class Object:

    def __init__(self, x, y, width, height):

        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_pos_size(self):

        return [self.x, self.y, self.width, self.height]


class Enemy(Object):

    def __init__(self, x, y, width, height, beast):

        super().__init__(x, y, width, height)
        self.beast = beast


class Cloud(Object):

    def __init__(self, x, y, width, height, line):

        super().__init__(x, y, width, height)
        self.line = line


class Grenade(Object):

    pass


# Отрисовка окна
def draw_window():
    global plusFramesCurrent, plus, animCount, plus_score

    if animCount + 1 >= 60:
        animCount = 0

    # Заливка окна белым
    window.fill(SKY)

    for draw_cloud in clouds:
        # print(cloud.get_pos_size)
        # print(cloud.line)
        pygame.draw.ellipse(window, GRAY, draw_cloud.get_pos_size(), draw_cloud.line)

    if player_sprite_toggle:

        if isJump or end:

            window.blit(player_sprite, [player_x, player_y])

        else:

            window.blit(run_sprites[animCount // 30], [player_x, player_y])
            animCount += 1 + score // 1000
    else:
        # Если игра закончена - песронаж становится красным, пока игра идёт - персонаж становится серым
        if end:

            pygame.draw.rect(window, RED, [player_x, player_y, player_width, player_height])

        else:

            pygame.draw.rect(window, GRAY, [player_x, player_y, player_width, player_height])

    # Отрисовка врага
    for draw_enemy in enemies:
        pygame.draw.rect(window, DARK_GREY, draw_enemy.get_pos_size())

    # Отрисовка очков
    window.blit(line_score, [lineScore_x, lineScore_y])
    window.blit(line_highScore, [lineHighScore_x, lineHighScore_y])

    # Отрисовка +50
    if plus and plusFramesCurrent >= 0:

        window.blit(line_plus, [linePlus_x, linePlus_y])
        plusFramesCurrent -= 1

    else:

        plusFramesCurrent = plusFramesConst
        plus = False
        plus_score = True

    # Отрисовка Окончания игры
    if end:
        window.blit(line_GameOver, [lineGameOver_x, lineGameOver_y])
        window.blit(line_restart, [lineRestart_x, lineRestart_y])

    pygame.draw.rect(window, GRASS, [floor_x, floor_y, floor_width, floor_height])

    # Обновление окна
    pygame.display.update()


def save():
    func_save_file = open("save.txt", "w")
    print("Saved", high_score)
    func_save_file.write(str(high_score))
    func_save_file.close()


# Создание нового врага
def new_enemy(plus_x=0):
    enemy_width = random.randrange(30, 50)
    enemy_height = random.randrange(40, 100)
    enemy_x = window_width + enemy_width + plus_x
    enemy_y = floor_y - enemy_height

    choice = random.randrange(0, 5)
    if choice == 1:

        baby = True

    else:

        baby = False

    enemies.append(Enemy(enemy_x, enemy_y, enemy_width, enemy_height, baby))


# noinspection PyGlobalUndefined
def new_cloud():
    cloud_line = random.randrange(7, 15)
    cloud_width = random.randrange(80, 120)
    cloud_height = random.randrange(40, 65)
    cloud_x = window_width + cloud_width
    cloud_y = random.randrange(0, 85)

    if clouds:

        last_cloud = clouds[-1]

        if not collide(last_cloud.x, last_cloud.y, last_cloud.width + 10, last_cloud.height,
                       cloud_x, cloud_y, cloud_width, cloud_height):
            clouds.append(Cloud(cloud_x, cloud_y, cloud_width, cloud_height, cloud_line))

    else:

        clouds.append(Cloud(cloud_x, cloud_y, cloud_width, cloud_height, cloud_line))


# Функция на проверку столкновения
def collide(p_x, p_y, p_w, p_h, e_x, e_y, e_w, e_h):
    p_w = p_x + p_w
    p_h = p_y + p_h

    e_w = e_x + e_w
    e_h = e_y + e_h

    cond_1 = (e_x <= p_x <= e_w) or (e_x <= p_w <= e_w)
    cond_2 = (e_y <= p_y <= e_h) or (e_y <= p_h <= e_h)
    cond_3 = (p_x <= e_x <= p_w) or (p_x <= e_w <= p_w)
    cond_4 = (p_y <= e_y <= p_h) or (p_y <= e_h <= p_h)

    return ((cond_1 and cond_2) or (cond_3 and cond_4)) or ((cond_1 and cond_4) or (cond_3 and cond_2))


def restart():
    global end, score, enemies, clouds, cloud_start_speed, player_y, isJump, jumpForceCurrent, animCount

    end = False
    score = 0
    enemies = []
    clouds = []
    new_enemy()
    new_cloud()
    cloud_start_speed = random.randrange(2, 5)
    player_y = floor_y - player_height
    isJump = False
    animCount = 0
    jumpForceCurrent = jumpForceConst


def start_screen():
    intro_text = ["Dino Stranding", "", "", "", "", ""
                                                    "Правила игры:",
                  "Просто перепрыгивай через камни",
                  'Прыгать можно на стрелочку вверх, клавишу "W" и пробел',
                  "Для начала игры нажми на любую клавишу",
                  "Удачи!"]

    background = pygame.transform.scale(pygame.image.load('data/img/background.jpg'), (window_width, window_height))
    window.blit(background, (0, 0))
    font_start = pygame.font.Font(None, 30)
    text_coord = 0

    for line in intro_text:
        string_rendered = font_start.render(line, 1, BLACK)
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        window.blit(string_rendered, intro_rect)

    while True:

        for start_event in pygame.event.get():

            if start_event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            elif start_event.type == pygame.KEYDOWN or start_event.type == pygame.MOUSEBUTTONDOWN:

                return

        pygame.display.flip()
        clock.tick(FPS)


# Запуск библиотеки
pygame.init()

if music_sounds_toggle:
    # Звук прыжка
    # noinspection PyUnboundLocalVariable
    shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Jump14.wav'))
    pygame.mixer.music.set_volume(0.4)

# Создание цветов
GRAY = pygame.Color("gray")
WHITE = pygame.Color("white")
GREEN = pygame.Color("green")
RED = pygame.Color("red")
BLACK = pygame.Color("black")
SKY = (117, 187, 253)
GRASS = (93, 161, 48)
SAND = (244, 164, 96)
DARK_GREY = (73, 66, 61)

# Размеры окна
window_width = 1300
window_height = 700

# Создание шрифтов
pygame.font.SysFont("arial", 36)
font = pygame.font.Font(None, 30)
font_GameOver = pygame.font.Font(None, 60)
font_restart = pygame.font.Font(None, 20)
font_plus = pygame.font.Font(None, 35)

# Высота пола
floor_y = window_height - 100
floor_x = 0
floor_width = window_width
floor_height = window_height

# Координаты всех строчек текста
lineScore_x = 20
lineScore_y = 20

linePlus_x = 50
linePlus_y = 80

lineHighScore_x = 20
lineHighScore_y = 50

lineRestart_x = window_width // 2 + 72
lineRestart_y = window_height // 2 - 25

lineGameOver_x = window_width // 2
lineGameOver_y = window_height // 2 - 75

# Параметры игрока
player_width = 80
player_height = 100
player_x = 225
player_y = floor_y - player_height

if player_sprite_toggle:
    player_sprite = pygame.transform.scale(pygame.image.load("data/img/dino/Dino_idle.png"),
                                           [player_width, player_height])
    run_sprites = [
        pygame.transform.scale(pygame.image.load("data/img/dino/Dino_step_1.png"), [player_width, player_height]),
        pygame.transform.scale(pygame.image.load("data/img/dino/Dino_step_2.png"), [player_width, player_height])
    ]
    animCount = 0

grenade_width = 20
grenade_height = 30

# Стартовая скорость врага и его создание
start_enemy_speed = 7
cloud_start_speed = random.randrange(2, 5)

# Очки и лучший результат
score = 0

# Таймер надписи +50 в кадрах
plusFramesConst = plusFramesCurrent = 30

# Разрешение на прыжок, сила прыжка и гравитация
isJump = False
jumpForceConst = jumpForceCurrent = 14
gravity = 5.25

# Кадры в секунду
FPS = 60

# Создание окна и смена его названия
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Dino Stranding")

# Создание строк перезапуска, окончания игры и +50
line_GameOver = font_GameOver.render('GAME OVER', 1, RED)
line_restart = font_restart.render('press "R" to restart', 1, RED)
line_plus = font_plus.render('+125', 1, GREEN)

# Создание таймера кадров
clock = pygame.time.Clock()

start_screen()

if music_sounds_toggle:

    # Мелодия
    expl_sounds = []

    for snd in ['expl3.wav', 'expl6.wav']:
        expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

    pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
    pygame.mixer.music.set_volume(0.2)

    pygame.mixer.music.play(loops=-1)

enemies = []
clouds = []

# Создание флагов
run = True
end = False
plus = False
plus_score = True
double = False

new_enemy()
new_cloud()

while run:
    clock.tick(FPS)

    cloud_choice = random.randrange(0, 60)
    if cloud_choice == 1:
        new_cloud()

    # Изменение очков и скорости врага
    if not end:

        score += 1

        if high_score < score:
            high_score = score

        enemy_speed = score / 333 + start_enemy_speed
        cloud_speed = cloud_start_speed  # + enemy_speed

        for enemy in enemies:

            if enemy.x < 0 - enemy.width:

                enemies.pop(enemies.index(enemy))

            else:

                enemy.x -= enemy_speed
    else:

        cloud_speed = cloud_start_speed

    if enemies:

        last_enemy = enemies[-1]
        # noinspection PyUnboundLocalVariable
        distance = player_width * 3 + enemy_speed * 10 + random.randint(100, 500)
        enemy_choice = random.randrange(0, 20)

        if window_width - last_enemy.x >= distance and enemy_choice == 1:

            if score >= 2000:

                double_choice = random.randrange(0, 3)

                if double_choice == 1:
                    new_enemy()
                    new_enemy(random.randrange(50, 100))

            else:

                new_enemy()

    else:

        new_enemy()

    for cloud in clouds:

        if cloud.x < 0 - cloud.width:

            clouds.pop(clouds.index(cloud))

        else:

            cloud.x -= cloud_speed

    # Создание строк очков
    line_score = font.render(f'Score: {score}', 1, BLACK)
    line_highScore = font.render(f'High score: {high_score}', 1, BLACK)

    # Получение событий
    for event in pygame.event.get():

        # Завершение цикла при нажатии на крестик
        if event.type == pygame.QUIT:

            run = False

            if not end:
                save()

    # Получение всех нажатых клавиш
    keys = pygame.key.get_pressed()

    # Нажатие на прыжок
    if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and not end and not isJump:

        isJump = True

        if music_sounds_toggle:
            # noinspection PyUnboundLocalVariable
            shoot_sound.play()

    # Перезапуск
    if keys[pygame.K_r] and end:
        restart()

    if keys[pygame.K_l]:
        save_file = open("save.txt", "w")
        save_file.write("0")
        save_file.close()

    # if keys[pygame.K_f]:

    # grenade = Grenade(player_width // 2, player_y // 2, grenade_width, grenade_height)

    # Прыжок
    if isJump:

        if jumpForceCurrent >= -jumpForceConst:

            if jumpForceCurrent < 0:

                player_y += (jumpForceCurrent ** 2) // gravity

            else:

                player_y -= (jumpForceCurrent ** 2) // gravity

            jumpForceCurrent -= 1

        else:

            isJump = False
            animCount = 0
            jumpForceCurrent = jumpForceConst

    # Столкновение с врагом (проверка)
    for enemy in enemies:

        if collide(player_x, player_y, player_width, player_height, enemy.x, enemy.y, enemy.width, enemy.height) \
                and not end:
            end = True
            enemy_speed = 0
            save()

    # Перепрыгивание через врага (проверка)
    for enemy in enemies:

        if collide(player_x, player_y, player_width, player_height,
                   enemy.x, 0, enemy.width, window_height - enemy.height) and not end:

            plus = True

            if plus_score:
                score += 125
                # print('plus')
                plus_score = False

    # Вызов отрисовки окна
    draw_window()

# Выход из программы
pygame.quit()
