import pygame
import random
from os import path

file_dir = r'C:/Users/freak/OneDrive/Рабочий стол/Диплом Python/PyGame/' # Указываем путь к фалам для игры

img_dir = file_dir + 'img/' # Путь к изображениям
snd_dir = file_dir + 'snd/' # путь к звукам
# Задаем параметры окна
WIDTH = 480  # Ширина
HEIGHT = 600 # Высота
FPS = 60 # Количество кадров в секунду, для динамических игр 60, для статических 30
POWERUP_TIME = 5000 # Время действия усиления

# Задаем параметры цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init() # Подгружаем основные встроенные модули в pygame
pygame.mixer.init() # Модуль для работы с аудио
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # создаем дисплей
pygame.display.set_caption("Battle in space") # Устанавливаем название окна, дисплея
clock = pygame.time.Clock() # Создаем объект Clock для отслеживания времени

font_name = pygame.font.match_font('arial', bold = True) # Устанавливаем шрифт

# Функция для отрисовки текста
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size) # Задаем шрифт
    text_surface = font.render(text, True, BLACK) # С помощью render создаем поверхность с текстом
    text_rect = text_surface.get_rect() # Получаем размеры и местоположения текста
    text_rect.midtop = (x, y) # Задаем местоположения текста
    surf.blit(text_surface, text_rect) # Отображаем текст на заданной поверхности

# Функция создания нового астеройда
def newmob():
    m = Mob() # Создаем объект mob(астеройд)
    all_sprites.add(m) # Добавляем объект в группу всех объектов
    mobs.add(m) # Добавляем объект в группу астеройдов

# Функция отрисовки полоски брони
def draw_shield_bar(surf, x, y, pct):
    if pct < 0: # Проверяем текущее состояние полоски брони
        pct = 0 # Если оно меньше 0, то прирваниваем к нулю
    BAR_LENGTH = 100 # Задаем длину полоски брони
    BAR_HEIGHT = 10 # Задаем высотку полоски брони
    fill = (pct / 100) * BAR_LENGTH # Считаем сколько будем отображать
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT) # Создаем объект полоски брони
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT) # Создаем объект заполнености полоски брони
    pygame.draw.rect(surf, GREEN, fill_rect) # Рисуем заполненость полоски брони
    pygame.draw.rect(surf, WHITE, outline_rect, 2) # Рисуем полоску брони

# Функция отрисовки жизней
def draw_lives(surf, x, y, lives, img):
    for i in range(lives): # Для общего количества жизней
        img_rect = img.get_rect() # Получаем местоположение жизней
        img_rect.x = x + 30 * i # значение x
        img_rect.y = y # значение y
        surf.blit(img, img_rect) # Отображаем жизни

# Функция отрисовки главного экрана
def show_go_screen():
    screen.blit(background, background_rect) # Отображаем фон
    draw_text(screen, "Battle in space", 64, WIDTH / 2, HEIGHT / 4) # Отрисовываем текст на фоне
    draw_text(screen, "Arrow keys move, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip() # отображаем текст на фоне
    waiting = True # Задаем флаг действия
    while waiting: # пока он True выполняем бесконечный цикл ожидания действий
        clock.tick(FPS) # Задаем отображение кадров
        for event in pygame.event.get(): # для каждого события, делаем проверку
            if event.type == pygame.QUIT: # Если нажата клавиша выход
                pygame.quit() # Закрываем приложение
            if event.type == pygame.KEYUP: # Если нажата клавиша
                waiting = False # Меняем флаг на False

# Создаем объект игрок
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Наследуем свойства класса Sprite
        self.image = pygame.transform.scale(player_img, (50, 38)) # Сжимаем изображение игрока до нужных размеров
        self.image.set_colorkey(BLACK) # Убираем лишний фон возле корабля
        self.rect = self.image.get_rect() # Получаем местоположение и размеры игрока
        self.radius = 20 # Задаем радиус
        self.rect.centerx = WIDTH / 2 # Определяем центр
        self.rect.bottom = HEIGHT - 10 # Отуступ снизу
        self.speedx = 0 # Скорость по оси Х
        self.shield = 100 # Начальный параметр брони
        self.shoot_delay = 250 # Задержка выстрелов
        self.last_shot = pygame.time.get_ticks() # Отсчет времени от последнего выстрела
        self.lives = 3 # количество жизней
        self.hidden = False # параметр исчезновения самолета
        self.hide_timer = pygame.time.get_ticks() # Отсчет времени
        self.power = 1
        self.power_time = pygame.time.get_ticks() # Отсчет времени

    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME: # Считаем время действия усиления
            self.power -= 1 # Если оно меньше условий то отключаем его
            self.power_time = pygame.time.get_ticks() # обновляем отсчет времени

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000: # Проверяем условия, если корабль игрока уничтожен
            self.hidden = False # возвращаем состояние в False
            self.rect.centerx = WIDTH / 2 # Задаем координаты
            self.rect.bottom = HEIGHT - 10 # Задаем координаты

        self.speedx = 0 # Задаем скорость движения
        keystate = pygame.key.get_pressed() # Получаем состояние "нажатости" клавиш на клавиатуре
        if keystate[pygame.K_LEFT]: self.speedx = -8 # Меняем скорость движения при нажатии клавиши
        if keystate[pygame.K_RIGHT]: self.speedx = 8 # Меняем скорость движения при нажатии клавиши
        if keystate[pygame.K_SPACE]: self.shoot() # Функция стрельбы при нажатии
        self.rect.x += self.speedx # Изменяем значение координаты по оси Х
        if self.rect.right > WIDTH: self.rect.right = WIDTH # Проверка чтобы не выходить за пределы экрана
        if self.rect.left < 0: self.rect.left = 0 # Проверка чтобы не выходить за пределы экрана

    def powerup(self):
        self.power += 1 # Увеличиваем усиление
        self.power_time = pygame.time.get_ticks() # Обновляем время отсчета

    def shoot(self):
        now = pygame.time.get_ticks() # Отсчет времени
        if now - self.last_shot > self.shoot_delay: # Проверяем задержку выстрела, если соотвествует условиям то
            self.last_shot = now # Обновляем время
            if self.power == 1: # Если усиления нет
                bullet = Bullet(self.rect.centerx, self.rect.top) # Задаем пулю
                all_sprites.add(bullet) # Добавляем объект пуля в группу все объекты
                bullets.add(bullet) # К пулям добавляем объект пуля
                shoot_sound.play() # Проигрываем звук выстрела
            if self.power >= 2: # Если действует уселение
                bullet1 = Bullet(self.rect.left, self.rect.centery) # Создаем левую пулю
                bullet2 = Bullet(self.rect.right, self.rect.centery) # Создаем правую пулю
                all_sprites.add(bullet1) # Добавляем объект пуля в группу все объекты
                all_sprites.add(bullet2) # Добавляем объект пуля в группу все объекты
                bullets.add(bullet1) # К пулям добавляем объект пуля
                bullets.add(bullet2) # К пулям добавляем объект пуля
                shoot_sound.play() # Проигрываем звук выстрела

    def hide(self): # Функция исчезновения
        self.hidden = True # Меняем статус на True
        self.hide_timer = pygame.time.get_ticks() # Отсчет времени
        self.rect.center = (WIDTH / 2, HEIGHT + 200 ) # Перемещаем корабль за пределы экрана

# Создаем класс астеройд
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Наследуем свойства класса Sprite
        self.image_orig = random.choice(meteor_images) # Выбираем случайное изображение из астрейодов
        self.image_orig.set_colorkey(BLACK) # Убираем лишний фон вокруг изображения
        self.image = self.image_orig.copy() # Создаем копию
        self.rect = self.image.get_rect() # Получаем координаты
        self.radius = int(self.rect.width * .85 / 2) # Задаем радиус, от него будет считать ущерб по кораблю
        self.rect.x = random.randrange(WIDTH - self.rect.width) # Задаем случайную величину Х
        self.rect.y = random.randrange(-150, -100) # Задаем случайную величину Y
        self.speedy = random.randrange(1, 8) # Задаем случайную скорость по оси Y
        self.speedx = random.randrange(-3, 3) # Задаем случайную скорость по оси Х
        self.rot = 0 # Значение вращения
        self.rot_speed = random.randrange(-8, 8) # Скорость вращения
        self.last_update = pygame.time.get_ticks() # Отсчет времени

    def rotate(self): # Функция вращения астреойда
        now = pygame.time.get_ticks() # Отсчет времени
        if now - self.last_update > 50: # Проверяем время с последнего обновления
            self.last_update = now # обновляем значение
            self.rot = (self.rot + self.rot_speed) % 360  # Задаем вращение, полный оборот
            new_image = pygame.transform.rotate(self.image_orig, self.rot) # Трансформирует изображение во вращающийся объект
            old_center = self.rect.center # Получаем текущее положение центра
            self.image = new_image # Обновляем переменную image
            self.rect = self.image.get_rect() # Получаем новое положение
            self.rect.center = old_center # Обновляем координату центра

    def update(self):
        self.rotate() # активируем функцию вращения
        self.rect.x += self.speedx # Меняем координаты по Х
        self.rect.y += self.speedy # Меняем координаты по Y
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20: # Если выходим за пределы
            self.rect.x = random.randrange(WIDTH - self.rect.width) # то меняем координаты Х
            self.rect.y = random.randrange(-100, -40) # меняем координаты Y
            self.speedy = random.randrange(1, 8) # задаем скорость

# Создаем объект снаряд
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) # Наследуем свойства класса Sprite
        self.image = bullet_img # Задаем значение image
        self.image.set_colorkey(BLACK) # Убираем лишний фон вокруг изображения
        self.rect = self.image.get_rect() # Получаем координаты
        self.rect.bottom = y # Задаем значение координат от корабля
        self.rect.centerx = x # Задаем значение координат от корабля
        self.speedy = -10 # Задаем скорость снаряда

    def update(self):
        self.rect.y += self.speedy # Увеличиваем значение координаты на скорость
        if self.rect.bottom < 0: # Когда снаряд выходит за рамки экрана
            self.kill() # Удаляем его

# Создаем объект усиления
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self) # Наследуем свойства класса Sprite
        self.type = random.choice(['shield', 'gun']) # Делаем случайный выбор усиления
        self.image = powerup_images[self.type] # задаем image усиление
        self.image.set_colorkey(BLACK) # Убираем лишний фон вокруг изображения
        self.rect = self.image.get_rect() # Получаем координаты
        self.rect.center = center # Присваиваем значение центра
        self.speedy = 2 # Задаем скорость

    def update(self):
        self.rect.y += self.speedy # Меняем координату
        if self.rect.top > HEIGHT: # Если выходит за рамки экрана
            self.kill() # Удаляем

# Создаем объект взрыв
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self) # Наследуем свойства класса Sprite
        self.size = size # Задаем размер
        self.image = explosion_anim[self.size][0] # Задаем image
        self.rect = self.image.get_rect() # Получаем координаты
        self.rect.center = center # Присваиваем значение центра
        self.frame = 0 # Количество кадров
        self.last_update = pygame.time.get_ticks() # Отсчет времени
        self.frame_rate = 50 # Задаем скорость анимации

    def update(self):
        now = pygame.time.get_ticks() # Отсчет времени
        if now - self.last_update > self.frame_rate: # Если условия не выполняются
            self.last_update = now # обновляем время
            self.frame += 1 # Увеличиваем начальное значение frame
            if self.frame == len(explosion_anim[self.size]): # Если вся анимация закончилась
                self.kill() # Удаляем объект
            else:
                center = self.rect.center # Если нет, то обновляем центр
                self.image = explosion_anim[self.size][self.frame] # Берем следующий кадр
                self.rect = self.image.get_rect() # Получаем координаты
                self.rect.center = center # Присваиваем значение центра


background = pygame.image.load(path.join(img_dir, "9810.png")).convert() # Загружаем изображение фона
background_rect = background.get_rect() # Получаем его координаты
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert() # Загружаем изображение корабля
player_mini_img = pygame.transform.scale(player_img, (25, 19)) # Изменяем размер для показателя жизней
player_mini_img.set_colorkey(BLACK) # Убираем лишний фон
bullet_img = pygame.image.load(path.join(img_dir, "laserRed16.png")).convert() # Загружаем изображение снаряда
meteor_images = [] # Здесь будем хранить изображения астеройдов
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png', 'meteorBrown_med1.png',
               'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert()) # Добавляем все астеройды в список

explosion_anim = {} # Создаем словарь для взрывов
explosion_anim['lg'] = [] # Большие взрывы
explosion_anim['sm'] = [] # Маленькие взрывы
explosion_anim['player'] = [] # Взрыв корабля игрока
for i in range(9): # Проходимся по всей анимации
    filename = 'regularExplosion0{}.png'.format(i) # Меняем название в цикле
    img = pygame.image.load(path.join(img_dir, filename)).convert() # Загружаем изображение
    img.set_colorkey(BLACK) # Убираем лишний фон
    img_lg = pygame.transform.scale(img, (75, 75)) # Меняем размер изображения
    explosion_anim['lg'].append(img_lg) # Добавляем по ключу lg большие взрывы
    img_sm = pygame.transform.scale(img, (32, 32)) # Меняем размер изображения
    explosion_anim['sm'].append(img_sm) # Добавляем по ключу маленькие взрывы
    filename = 'sonicExplosion0{}.png'.format(i) # Меняем название файла в цикле
    img = pygame.image.load(path.join(img_dir, filename)).convert() # Загружаем изображение
    img.set_colorkey(BLACK) # Убираем лишний фон
    explosion_anim['player'].append(img) # Добавляем по ключу взрывы корабля
powerup_images = {} # здесь будем хранить изображения усилений
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert() # Загружаем изображение щита
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert() # Загружаем изображение молнии


shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav')) # Звук выстрела
expl_sounds = [] # Здесь храним звук взрывов
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd))) # Загружаем звуки

# Запуск игрового процесса
game_over = True # Задаем флаг конца игры
running = True # Задаем флаг
while running: # Пока игра запущенна
    if game_over: # Изначально выполняем условие
        show_go_screen() # Запускаем функцию отрисовки экрана
        game_over = False # Меняем значение
        all_sprites = pygame.sprite.Group() # Добавляем все движущиеся объекты в группу
        mobs = pygame.sprite.Group() # Группа для астеройдов
        bullets = pygame.sprite.Group() # Группа для снарядов
        powerups = pygame.sprite.Group() # Группа для усилений
        player = Player() # Функция создания игрока
        all_sprites.add(player) # Добавляем игрока в группу всех объектов
        for i in range(8): # Создаем астеройды
            newmob()
        score = 0 # начальное значение очков

    clock.tick(FPS) # Задаем количество кадров
    for event in pygame.event.get(): # Для каждого собатия
        if event.type == pygame.QUIT: # Проверяем условие
            running = False # Меняем значение

    all_sprites.update() # Обновляем состояние всех движущихся объектов

    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) # Задаем столкновения объектов
    for hit in hits: # При каждом столкновении
        score += 50 - hit.radius # Считаем количество очков
        random.choice(expl_sounds).play() # выбираем случайно звук взрыва и проигрываем его
        expl = Explosion(hit.rect.center, 'lg') # Запускаем анимацию взрыва
        all_sprites.add(expl) # Добавляем взрыв в группу объектов
        if random.random() > 0.9: # Если случаное число больше 0.9 то
            pow = Pow(hit.rect.center) # Создаем усиление
            all_sprites.add(pow) # Добавляем в группу объъектов
            powerups.add(pow) # Добавляем в группу усилений
        newmob() # Создаем новый астеройд

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle) # Задаем столкновения объектов
    for hit in hits: # При каждом столкновении
        player.shield -= hit.radius * 2 # Отнимаем значения от щита при столкновении с астеройдом
        expl = Explosion(hit.rect.center, 'sm') # Запускаем анимацию взрыва
        all_sprites.add(expl) # Добавляем взрыв в группу объектов
        newmob() # Создаем новый астеройд
        if player.shield <= 0: # Если значения щита меньше 0
            death_explosion = Explosion(player.rect.center, 'player') # Создаем анимацию взрыва коробля
            all_sprites.add(death_explosion) # Добавляем в группу объъектов
            player.hide() # Запускаем функцию исчезновения корабля
            player.lives -= 1 # Уменьшаем количество жизней на 1
            player.shield = 100 # Восстанавливаем значения щита

    hits = pygame.sprite.spritecollide(player, powerups, True) # Задаем столкновения объектов
    for hit in hits: # При каждом столкновении
        if hit.type == 'shield': # Если усиление это щит то
            player.shield += random.randrange(10, 30) # Увеличиваем значение брони от 10 до 30
            if player.shield >= 100: # Если больше 100
                player.shield = 100 # то приравниваем к максимальному
        if hit.type == 'gun': # Если усиление для оружия
            player.powerup() # То запускаем функцию усиления


    if player.lives == 0 and not death_explosion.alive(): # Если жизни закончились и анимация взрыва корабля закончилась
        game_over = True # Возвращаем конец игры

    screen.fill(BLACK) # Заполняем экран черным цветом
    screen.blit(background, background_rect) # Отображаем поверхность
    all_sprites.draw(screen) # Рисуем все объекты на поверхности
    draw_text(screen, str(score), 18, WIDTH / 2, 10) # Отрисовываем текст с отображением очков
    draw_shield_bar(screen, 5, 5, player.shield) # Отрисовываем полоску брони
    draw_lives(screen, WIDTH - 100, 5, player.lives,
               player_mini_img) # Отрисовываем количество жизней и мини иконки
    pygame.display.flip() # Отображаем все на экране

pygame.quit() # Выходим из игры