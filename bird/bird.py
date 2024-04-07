# Импорт необходимых модулей
from pygame import *
from random import randint

# Инициализация шрифтов
font.init()

# Определение размеров окна и других констант
WIDTH = 460  # Ширина окна
HEIGHT = 500  # Высота окна
BOTTOM = 420  # Позиция земли
TOP = 80  # Верхняя часть окна
FPS = 60  # Количество кадров в секунду

# Цвета
WHITE = (255, 255, 255)  # Белый цвет

# Создание шрифта для текста
text_font = font.SysFont('Bauhaus 93', 50)

# Создание окна
window = display.set_mode((WIDTH, HEIGHT))  # Создание окна Pygame
display.set_caption('Flappy Bird')  # Установка заголовка окна
clock = time.Clock()  # Создание объекта Clock для управления временем в игре

# Настройка прокрутки земли
ground_scroll = 0  # Начальное значение прокрутки земли
scroll_speed = 2  # Скорость прокрутки

# Управление полётом птицы и завершением игры
flying = False  # Флаг, указывающий, летит ли птица в данный момент
finish = False  # Флаг, указывающий, завершена ли игра

# Параметры труб
pipe_gap = 100  # Промежуток между трубами
pipe_frequency = 1500  # Частота появления труб
last_pipe = time.get_ticks() - pipe_frequency  # Последнее появление трубы

# Очки
score = 0  # Игровые очки
pass_pipe = False  # Флаг, указывающий, что птица прошла трубу

# Загрузка фоновой картинки и изображения земли
background = transform.scale(image.load('bg.png'), (WIDTH, BOTTOM))  # Загрузка фоновой картинки
ground_img = transform.scale(image.load('ground.png'), (480, TOP))  # Загрузка изображения земли
button_img = image.load('restart.png')  # Загрузка изображения кнопки перезапуска игры

# Функция для отрисовки текста на экране
def draw_text(text: str, font: str, text_col: tuple, x: int, y: int):
    """Отображает текст на экране."""
    img = text_font.render(text, True, text_col)  # Создание изображения текста
    window.blit(img, (x, y))  # Отображение изображения текста на экране

# Функция для сброса состояния игры
def reset_game():
    """Сбрасывает состояние игры."""
    pipe_group.empty()  # Очищает группу труб
    flappy.rect.x = 100  # Устанавливает начальное положение птицы по горизонтали
    flappy.rect.y = int(HEIGHT / 2)  # Устанавливает начальное положение птицы по вертикали
    score = 0  # Обнуляет счёт
    return score  # Возвращает счёт

# Класс для птицы
class Bird(sprite.Sprite):
    """Класс, представляющий птицу."""
    def __init__(self, x: int, y: int, w: int, h: int):
        super().__init__()  # Вызов конструктора родительского класса
        self.images = []  # Список изображений для анимации птицы
        self.index = 0  # Текущий индекс изображения в списке
        self.counter = 0  # Счётчик для анимации
        # Загрузка изображений птицы и их масштабирование
        for num in range(1, 4):
            img = transform.scale(image.load(f'bird{num}.png'), (w, h))
            self.images.append(img)
        self.image = self.images[self.index]  # Текущее изображение птицы
        self.rect = self.image.get_rect()  # Прямоугольник, описывающий птицу
        self.rect.center = [x, y]  # Центральная позиция птицы
        self.vel = 0  # Скорость птицы по вертикали
        self.clicked = False  # Флаг, указывающий, было ли сделано нажатие на кнопку мыши




    def update(self):
        """Обновляет состояние трубы."""
        if flying == True:  # Если птица летит
            self.vel += 0.2  # Увеличиваем скорость падения трубы
            if self.vel > 30:  # Если скорость превысила максимальное значение
                self.vel = 0  # Сбрасываем скорость до нуля
            if self.rect.bottom < 420:  # Если нижний край трубы ещё не достиг земли
                self.rect.y += int(self.vel)  # Перемещаем трубу вниз на значение скорости
        
        if not finish:  # Если игра не завершена
            if mouse.get_pressed()[0] == 1 and not self.clicked:  # Если было сделано нажатие кнопки мыши и оно не было сделано ранее
                self.clicked = True  # Устанавливаем флаг нажатия
                self.vel = -5  # Задаем скорость вверх для птицы
            if mouse.get_pressed()[0] == 0:  # Если кнопка мыши отпущена
                self.clicked = False  # Сбрасываем флаг нажатия

            self.counter += 1  # Увеличиваем счётчик
            flap_cooldown = 5  # Задаем интервал для смены кадров анимации

            if self.counter > flap_cooldown:  # Если прошло достаточно времени для смены кадра
                self.counter = 0  # Сбрасываем счётчик
                self.index += 1  # Увеличиваем индекс изображения
                if self.index >= len(self.images):  # Если индекс вышел за пределы списка изображений
                    self.index = 0  # Сбрасываем индекс

            self.image = self.images[self.index]  # Обновляем изображение трубы

            # Поворачиваем изображение трубы на основе скорости птицы
            self.image = transform.rotate(self.images[self.index], self.vel * -2)
        else:  # Если игра завершена
            # Поворачиваем изображение трубы на -90 градусов
            self.image = transform.rotate(self.images[self.index], -90)


# Класс для труб
class Pipe(sprite.Sprite):
    """Класс, представляющий трубу."""
    def __init__(self, x: int, y: int, w:int, h:int, position: int):
        super().__init__()  # Вызов конструктора родительского класса
        self.image = transform.scale(image.load('img/pipe.png'), (w, h))  # Загрузка изображения трубы и его масштабирование
        self.rect = self.image.get_rect()  # Прямоугольник, описывающий трубу
        
        # Определение положения трубы (вверху или внизу)
        if position == 1:  # Если труба должна быть сверху
            self.image = transform.flip(self.image, False, True)  # Переворачиваем изображение трубы
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]  # Устанавливаем позицию трубы снизу
        elif position == -1:  # Если труба должна быть снизу
            self.rect.topleft = [x, y + int(pipe_gap / 2)]  # Устанавливаем позицию трубы сверху
    
    def update(self):
        """Обновляет положение трубы."""
        self.rect.x -= scroll_speed  # Перемещаем трубу влево со скоростью прокрутки
        if self.rect.right < 0:  # Если правый край трубы выходит за пределы экрана
            self.kill()  # Удаляем трубу из группы


# Класс для кнопки
class Button():
    """Класс, представляющий кнопку."""
    def __init__(self, x: int, y: int, image: str):
        """Инициализирует кнопку."""
        self.image = image  # Загружает изображение кнопки
        self.rect = self.image.get_rect()  # Получает прямоугольник, описывающий кнопку
        self.rect.topleft = (x, y)  # Устанавливает позицию кнопки

    def draw(self):
        """Отображает кнопку и возвращает информацию о действии пользователя."""
        action = False  # Переменная для отслеживания действия пользователя
        pos = mouse.get_pos()  # Получает текущие координаты мыши
        if self.rect.collidepoint(pos):  # Если курсор мыши находится над кнопкой
            if mouse.get_pressed()[0] == 1:  # Если нажата левая кнопка мыши
                action = True  # Устанавливает флаг действия в True

        window.blit(self.image, (self.rect.x, self.rect.y))  # Отображает изображение кнопки на экране

        return action  # Возвращает информацию о действии пользователя




# Группы спрайтов
bird_group = sprite.Group()  # Группа спрайтов птицы
pipe_group = sprite.Group()  # Группа спрайтов труб

# Создание птицы и добавление её в группу
flappy = Bird(100, int(WIDTH/2), 35, 25)
bird_group.add(flappy)

# Создание кнопки
button = Button(WIDTH // 2 - 50, HEIGHT // 2 - 50, button_img)

# Основной цикл игры
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False  # Если пользователь закрыл окно, завершаем цикл
        if e.type == MOUSEBUTTONDOWN and not flying and not finish:
            flying = True  # Если пользователь нажал кнопку мыши и птица не летит и игра не завершена, начинаем полёт птицы
    
    window.blit(background, (0, 0))  # Отображаем фон

    pipe_group.draw(window)  # Отображаем трубы
    window.blit(ground_img, (ground_scroll, BOTTOM))  # Отображаем землю

    if len(pipe_group) > 0:  # Если есть активные трубы на экране
        # Проверка, прошла ли птица между трубами
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
            and bird_group.sprites()[0].rect.left < pipe_group.sprites()[0].rect.right \
            and not pass_pipe:
            pass_pipe = True  # Если птица прошла между трубами, устанавливаем флаг прохождения
        if pass_pipe:  # Если птица прошла между трубами
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:  # Если птица прошла за трубу
                score += 1  # Увеличиваем счёт
                pass_pipe = False  # Сбрасываем флаг прохождения

    
    draw_text(str(score), text_font, WHITE, int(WIDTH / 2), 20)  # Отображаем счёт

    bird_group.draw(window)  # Отображаем птицу
    bird_group.update()  # Обновляем положение птицы

    # Проверка на столкновение птицы с трубами или касание земли
    if sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        finish = True  # Если произошло столкновение с трубой или птица коснулась верхнего края экрана, завершаем игру

    if flappy.rect.bottom >= BOTTOM:  # Если птица коснулась нижнего края экрана
        finish = True  # Завершаем игру
        flying = False  # Птица перестает лететь

    if not finish and flying:  # Если игра не завершена и птица летит
        time_now = time.get_ticks()  # Получаем текущее время в миллисекундах
        if time_now - last_pipe > pipe_frequency:  # Если прошло достаточно времени для создания новой трубы
            pipe_height = randint(-50, 50)  # Генерируем случайную высоту для трубы
            btm_pipe = Pipe(WIDTH, int(HEIGHT/2) + pipe_height, 35, 250, -1)  # Создаем нижнюю трубу
            top_pipe = Pipe(WIDTH, int(HEIGHT/2) + pipe_height, 35, 250, 1)  # Создаем верхнюю трубу
            pipe_group.add(btm_pipe)  # Добавляем нижнюю трубу в группу труб
            pipe_group.add(top_pipe)  # Добавляем верхнюю трубу в группу труб
            last_pipe = time_now  # Обновляем время последнего появления трубы
        
        pipe_group.update()  # Обновляем положение труб

        ground_scroll -= scroll_speed + .3  # Прокручиваем землю
        if abs(ground_scroll) > 20:  # Если значение прокрутки земли превышает 20
            ground_scroll = 0  # Сбрасываем значение прокрутки
    
    if finish:
        if button.draw():  # Если нажата кнопка
            finish = False  # Сбрасываем флаг завершения игры
            score = reset_game()  # Сбрасываем игру

    display.update()  # Обновляем экран
    clock.tick(FPS)  # Ограничиваем частоту кадров