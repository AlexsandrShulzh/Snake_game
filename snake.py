import pygame
import random

# Инициализация Pygame
pygame.init()

# Глобальные константы
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 25
FPS = 60
INITIAL_SPEED = 7
GAME_TIME = 30  # Время игры в секундах

# Цвета
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

# Режимы игры
NORMAL_MODE = 0
ENDLESS_MODE = 1

UP = 0
DOWN = 0
LEFT = 0
RIGHT = 0 
n = 0
pressed = False
record = 0
pole_image = pygame.image.load('pole.png')
apple_image = pygame.image.load('apple.png')
snake_body = pygame.image.load('snake_body.png')
snake_head = pygame.image.load('snake_head.png')
snake_tail = pygame.image.load('snake_tail.png')
snake_down = pygame.transform.rotate(snake_body, 180)
snake_right = pygame.transform.rotate(snake_body, -90)
snake_left = pygame.transform.rotate(snake_body, 90)
snake_head_left = pygame.transform.rotate(snake_head, 90)
snake_head_right = pygame.transform.rotate(snake_head, -90)
snake_head_down = pygame.transform.rotate(snake_head, 180)
snake_tail_left = pygame.transform.rotate(snake_tail, 90)
snake_tail_right = pygame.transform.rotate(snake_tail, -90)
snake_tail_down = pygame.transform.rotate(snake_tail, 180)

snake_body.set_colorkey(WHITE)
snake_head.set_colorkey(WHITE)
snake_tail.set_colorkey(WHITE)
snake_left.set_colorkey(WHITE)
snake_right.set_colorkey(WHITE)
snake_down.set_colorkey(WHITE)
snake_head_left.set_colorkey(WHITE)
snake_head_down.set_colorkey(WHITE)
snake_head_right.set_colorkey(WHITE)
snake_tail_left.set_colorkey(WHITE)
snake_tail_down.set_colorkey(WHITE)
snake_tail_right.set_colorkey(WHITE)

image_body = snake_body
image_head = snake_head
image_tail = snake_tail


# Функция отрисовки змейки и игрового поля
def draw_snake(snake_list):
    global UP
    global DOWN
    global LEFT
    global RIGHT
    global pressed
    global image_body
    global n
    global image_head
    global image_tail
    
    for x, y in snake_list:
        x_h, y_h = snake_list[n]
        x_t = snake_list[0][0]
        y_t = snake_list[0][1]      
        if pressed == False:
            image_body = snake_body
            image_head = snake_head
            image_tail = snake_tail
            pressed = True
        elif UP == 1: 
            image_body = snake_body
            image_head = snake_head
            image_tail = snake_tail
            UP -= 1
        elif DOWN == 1:
            image_body = snake_down
            image_head = snake_head_down
            image_tail = snake_tail_down
            DOWN -= 1
        elif LEFT == 1:
            image_body = snake_left
            image_head = snake_head_left
            image_tail = snake_tail_left
            LEFT -= 1
        elif RIGHT == 1:
            image_body = snake_right
            image_head = snake_head_right
            image_tail = snake_tail_right
            RIGHT -= 1
        if (x == x_h and y_h == y) or (x == x_t and y == y_t):
            screen.blit(image_head, (x_h, y_h))
            screen.blit(image_tail, (x_t, y_t))
        else:
            screen.blit(image_body, (x, y))
            
            
# Функция выбора режима игры
def choose_game_mode():
    screen.blit(pole_image, (0, 0))

    # Текст и инструкции
    font = pygame.font.SysFont(None, 36)
    mode_text = font.render("Выберите режим сложности:", True, WHITE)
    normal_text = font.render("Нормальный режим(стены препятствия)", True, WHITE)
    endless_text = font.render("Лёгкий режим(нет препятствий)", True, WHITE)
    start_text_n = font.render("Нажмите N чтобы играть в нормальный режим", True, WHITE)
    start_text_e = font.render("Нажмите E чтобы играть в лёгкий", True, WHITE)

    # Отрисовка текста на экране
    screen.blit(mode_text, (SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2 - 100))
    screen.blit(normal_text, (SCREEN_WIDTH // 2 - 290, SCREEN_HEIGHT // 2 - 50))
    screen.blit(endless_text, (SCREEN_WIDTH // 2 - 290, SCREEN_HEIGHT // 2))
    screen.blit(start_text_n, (SCREEN_WIDTH // 2 - 290, SCREEN_HEIGHT // 4 * 3))
    screen.blit(start_text_e, (SCREEN_WIDTH // 2 - 290, SCREEN_HEIGHT // 4 * 2.5))
    pygame.display.flip()

    # Цикл выбора режима
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:  # Нормальный режим
                    return NORMAL_MODE
                elif event.key == pygame.K_e:  # Бесконечный режим
                    return ENDLESS_MODE

def game():
    global UP
    global DOWN
    global LEFT
    global RIGHT
    global n
    # Получение выбранного режима
    game_mode = choose_game_mode()
    snake_list = [[100, 100]]  # Список координат сегментов змейки
    snake_length = 1
    x, y = 100, 100  # Начальные координаты головы змейки
    score = 0
    n = 0
    food_x, food_y = random.randrange(0, SCREEN_WIDTH - CELL_SIZE, CELL_SIZE), random.randrange(0, SCREEN_HEIGHT - CELL_SIZE, CELL_SIZE)  # Координаты еды

    dx, dy = 0, 0  # Направление движения змейки
    step = CELL_SIZE
    speed = INITIAL_SPEED

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks() 

    game_over = False
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -step
                    UP += 1
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, step
                    DOWN += 1
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -step, 0
                    LEFT += 1
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = step, 0
                    RIGHT += 1
                elif event.key == pygame.K_r and game_over:  # Перезапуск игры по нажатию клавиши "R"
                    game()
                
        x += dx
        y += dy

        if game_mode == NORMAL_MODE:
            if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
                game_over = True
        elif game_mode == ENDLESS_MODE:
            if x >= SCREEN_WIDTH:
                x = 0
            elif x < 0:
                x = SCREEN_WIDTH - CELL_SIZE
            if y >= SCREEN_HEIGHT:
                y = 0
            elif y < 0:
                y = SCREEN_HEIGHT - CELL_SIZE

        if [x, y] in snake_list[1:]:
            game_over = True

        if x == food_x and y == food_y:
            snake_length += 1
            score += 1
            n += 1
            food_x, food_y = random.randrange(0, SCREEN_WIDTH - CELL_SIZE, CELL_SIZE), random.randrange(0, SCREEN_HEIGHT - CELL_SIZE, CELL_SIZE)
            if food_x == x and food_y == y:
                food_x, food_y = random.randrange(0, SCREEN_WIDTH - CELL_SIZE, CELL_SIZE), random.randrange(0, SCREEN_HEIGHT - CELL_SIZE, CELL_SIZE)

            
            # Обновление таймера при съедании новой еды
            start_time = pygame.time.get_ticks()  # Сбрасываем таймер

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]
        pole_rect = pole_image.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(pole_image, pole_rect)
        draw_snake(snake_list)
        apple_image.set_colorkey((255, 255, 255))
        screen.blit(apple_image, (food_x, food_y))
        apple_image.set_colorkey((255, 255, 255))

        # Отображение счетчика очков и таймера
        font = pygame.font.SysFont(None, 48)
        score_text = font.render(f'Очки: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        time_text = font.render(f'Время: {GAME_TIME - elapsed_time}', True, WHITE)
        screen.blit(time_text, (425, 10))

        pygame.display.flip()
        clock.tick(speed)

        if elapsed_time > GAME_TIME:
            game_over = True

        # Увеличение скорости с каждым новым очком

        if speed < 30:
            speed = INITIAL_SPEED + (score // 2)
        else:
            pass

    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render('Вы проиграли', True, WHITE)
    score_text = font.render(f'Очки: {score}', True, WHITE)
    restart_text = font.render('Нажмите R для перезапуска', True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 24))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 24))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 230, SCREEN_HEIGHT // 2 + 64))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Перезапуск игры по нажатию клавиши "R"
                    game()

    game()

# Создание экрана и запуск игры
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка')
game()
