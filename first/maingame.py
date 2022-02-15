import pygame
pygame.font.init()
s_font = pygame.font.SysFont('Arial', 14)
num_of_cells = generation = 0
t_string1 = 'Gen: 0'
parents_define = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]  # указатели на соседей клетки
clock = pygame.time.Clock()
ss_flag = False                      # флаг старт стопа эволюции
background = (40, 40, 40)
empty = (80, 80, 80)
filed = (175, 175, 175)
text_color = (255, 255, 255)
size_colony_x = 200                 # клеток по х
size_colony_y = 200                 # клеток по y
mas = [[0]*size_colony_x for i in range(size_colony_y)]    # массив клеток
fps = 500
size_block = 10                                 # размер одной клетки
margin = 1                                      # промежуток между клетками. нужен ли?
#width = size_block*size_x_range + margin*141
width = 1400                      # ширина видимого окна в пикселях
#height = size_block*size_y_range + margin*81
height = 800                                     # высота видимого окна в пикселях
dx = (size_colony_x - width // size_block)//2
dy = (size_colony_y - height // size_block)//2
window = pygame.display.set_mode((width, height))    # откроем окно
pygame.display.set_caption('Game of Life')      # установим заголовок окна
screen = pygame.Surface((width, height))             # создаем игровой экран
work = True             # переменная игрового цикла


def parents(row, col):                  # определение числа соседей клетки
    p = 0
    for j in range(len(parents_define)):
        if mas[row+parents_define[j][0]][col+parents_define[j][1]] == 'x' or\
           mas[row+parents_define[j][0]][col+parents_define[j][1]] == 'o':
            p += 1
    return p


def change():                            # смена поколений
    global num_of_cells
    for row in range(size_colony_y):
        for col in range(size_colony_x):
            if mas[row][col] == 'o':
                mas[row][col] = ''
                num_of_cells -= 1
            if mas[row][col] == '^':
                mas[row][col] = 'x'
                num_of_cells += 1
    return


def evolution():                            # предварительный расчет поколений
    for row in range(1, size_colony_y - 1):  #
        for col in range(1, size_colony_x - 1):
            if mas[row][col] == 'x':
                if parents(row, col) < 2 or parents(row, col) > 3:
                    mas[row][col] = 'o'
            else:
                if parents(row, col) == 3:
                    mas[row][col] = '^'
    return


while work:
    for e in pygame.event.get():                # обработка событий
        if e.type == pygame.QUIT:               # на закрытие окна
            work = False
            ''' обработка управления'''
        elif e.type == pygame.MOUSEBUTTONDOWN:  # колесико для масштаба
            if e.button == 5:
                if size_block > 2:
                    size_block -= 1
            elif e.button == 4:
                if size_block < 50:
                    size_block += 1
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:         # пробелом запускаем / останавливаем процесс
                ss_flag = not ss_flag
            if e.key == pygame.K_RETURN:        # только один шаг
                evolution()
                change()
                if num_of_cells:            # если колония жива считаем поколения
                    generation += 1
                else:
                    generation = 0              # иначе обнуляем
    pressed = pygame.mouse.get_pressed()        # берем событие мыша
    x_mouse, y_mouse = pygame.mouse.get_pos()   # запоминаем координаты мыша
    if x_mouse <= 4 and dx > 1:                 # если курсор на краю то сдвигаем видимое окно
        dx -= 2
    if x_mouse >= width - 5 and dx < size_colony_x - width // size_block + 13:
        dx += 2
    if y_mouse <= 4 and dy > 1:
        dy -= 2
    if y_mouse >= height - 5 and dy < size_colony_y - height // size_block + 8:
        dy += 2
    if pressed[0]:                              # нажали левую кн - ставим клетки
        x_col = x_mouse // (size_block + margin)
        y_row = y_mouse // (size_block + margin)
        if y_row+dy < size_colony_y and x_col+dx < size_colony_x and \
                mas[y_row+dy][x_col+dx] != 'x':   # проверяем клик за пределами поля и лишние клики
            mas[y_row+dy][x_col+dx] = 'x'                 # записываем "занято" в нужный индекс массива
            num_of_cells += 1
    if pressed[1]:                              # нажали среднюю кн - все инициализируем
        dx = (size_colony_x - width // size_block) // 2
        dy = (size_colony_y - height // size_block) // 2
        size_block = 10
        num_of_cells = 0
        generation = 0
        ss_flag = False
        mas = [[0] * size_colony_x for i in range(size_colony_y)]
    if pressed[2]:                              # нажали правую кн - стираем клетки
        x_col = x_mouse // (size_block + margin)
        y_row = y_mouse // (size_block + margin)
        if y_row + dy < size_colony_y and x_col + dx < size_colony_x and\
                mas[y_row+dy][x_col+dx] == 'x':   # проверяем клик за пределами поля и лишние клики
            mas[y_row+dy][x_col+dx] = ''                  # записываем "пусто" в нужный индекс массива
            num_of_cells -= 1
        ''' преобразования массива клеток в процессе эволюции'''
    if ss_flag:
        evolution()     # посчитали след поколение
        change()        # сменили его
        if num_of_cells > 0:
            generation += 1
        else:
            generation = 0
            ss_flag = False
    screen.fill(background)                     # закрашиваем экран
    ''' рисуем поле'''
    for row_ in range(dy, size_colony_y):  # отрисовываем массив клеток
        for col_ in range(dx, size_colony_x):
            if mas[row_][col_] == 'x':    # если "занято" то рисуем "живую" клетку
                color = filed
            else:                       # иначе рисуем "пустую" клетку
                color = empty
            x = (col_*size_block + (col_ + 1) * margin) - (dx*size_block+dx*margin)
            y = (row_*size_block + (row_ + 1) * margin) - (dy*size_block+dy*margin)
            if x < width and y < height:        # если не вышли из видимого окна
                pygame.draw.rect(screen, color, (x, y, size_block, size_block))
    t_string = 'Cells: ' + str(num_of_cells)
    if num_of_cells > 0:
        t_string1 = 'Gen: ' + str(generation)
    textsurface = s_font.render(t_string, False, text_color)
    textsurface1 = s_font.render(t_string1, False, text_color)

    clock.tick(fps)             # замедляем
    window.blit(screen, (0, 0))
    window.blit(textsurface, (0, 0))
    window.blit(textsurface1, (0, 15))
    pygame.display.flip()
