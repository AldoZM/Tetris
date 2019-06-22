import pygame
import random
 
 
pygame.font.init()
 

# Variables Globales
s_width = 800
s_height = 700
play_width = 300  
play_height = 600
block_size = 30
 
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
 
 
# Formato de las figuras 
 
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T] # Los tipos de fijugas que se emplean 
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)] #Los colores que se utilizan para las figuras  

# indice 0 - 6 representan la formas (se ve desde el 0 al 6 porque se ve como un arreglo)
 
 
class Piece(object): # Aqui se crea la pieza para el juego
    
    rows = 20  # x filas
    columns = 10  # y columnas   
    
    def __init__(self, column, row, shape):#Esta funcion es para saber si se esta importando o esta ejecutando el archivo que estamos tomando
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # numero del 1 al 3
 
# Aqui se almacena la imformacion para cada pieza que se utiliza en el juego

def create_grid(locked_positions={}): # En "locked_positions" contiene una dirreccion de dos cosas caundo cae y el color que pose 

# Aqui se delcara la funcion para clrear las cuadriculas o mejor dicho los cuadros que se ven


    grid = [[(0,0,0) for x in range(10)] for x in range(20)]
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid
 
 
def convert_shape_format(shape): # Aqui se eliminas los espacios facios que se reprentan por "..." y ya se empieza a tomar en cuenta los 0 para que la maquina los pueda interpretar
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)

        #Aqui empieza la depuracion de los "..."

        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
 
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
 
    return positions
 
 
def valid_space(shape, grid):# En esta funciona hacemos que se nos pueda validar los espacios que la fijura que estamos moviendo pueda encajar en la rejilla o en la cuadricula que estamos 

    
    #Aqui es para ver si en la posicion que esta es aceptable
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)
    #Aqui es para saber si la esta ocupada o no la casilla  
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
 
    return True
 
 
def check_lost(positions):# Esta funcion checa contantemente si el jugador pierde por aver llegado a la cima
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False
 
 
def get_shape():
    global shapes, shape_colors # Mandamos a llamavar las variables globales 
 
    return Piece(5, 0, random.choice(shapes)) # Ceamos piezas al azar para soltarlo en la pantalla 
 
 
def draw_text_middle(text, size, color, surface): #Esta función nos ayudará a mostrar el texto en el centro de la pantalla y se usará para cuando creemos un menú principal y una pantalla final para nuestro juego.

    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
 
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))
 
 
def draw_grid(surface, row, col): #Esta funcion simplemente dibuja la lineas de la cuadricula del area del juego 
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # Aqui se crean la linias de forma horizontal 
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # Aqui se crean la linias de forma Vertical
 
 
def clear_rows(grid, locked): #Lo que hace esta funcion es limpiar la fila cuando esta llena 
    
    # hay que ver si la fila está despejada el turno cada otra fila arriba abajo abajo
 
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # Añade la posicion para eliminar la linea de bloques

            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
 
 
def draw_next_shape(shape, surface):#Aqui es donde nos mostrara la siguiente figura que estara aun lado de la ventana
    font = pygame.font.SysFont('comicsans', 30) #Tipo de letra que se usa y el tamaño
    label = font.render('Sig. Pieza', 1, (255,255,255)) #Lo palabara y el color que se aplica 
 
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
 
    surface.blit(label, (sx + 10, sy- 30))
 
 
def draw_window(surface):#Aqui sirve para el diseño de como lo vamos a ver nosotros 
    surface.fill((0,0,0))
    # Titulo de TETRIS
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('TETRIS', 1, (255,255,255))
 
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)
 
    # Se dibuja el borde de las rejillas 
    draw_grid(surface, 20, 10)
    # Se le pone el color ROSA a la rejilla para que se vea el limite 
    pygame.draw.rect(surface, (255, 0, 255), (top_left_x, top_left_y, play_width, play_height), 5)
    # pygame.display.update()
 
 
def main(): # En esta funcion es donde se define algunas de las variables y luego se pasa al loop while
    global grid
 
    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)
 
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    #Un "loop" para que el juego siga corriendo mientras lo juegas 
    while run:
        fall_speed = 0.27
 
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
 
        # Codigo de la pieza callendo
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
 
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                #Aqui se utiliza ya las teclas para mover las figuras 

                #Aqui se mueve la figura a la izquierda
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
 
                #Aqui se mueve la figura a la derecha
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # La rotacion de la figura
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
 
                if event.key == pygame.K_DOWN:
                    # Mover la pieza hacia abajo o recorrerlo mas rapido
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
 
                if event.key == pygame.K_SPACE:
                   #Aqui cuando precionas la barra espacidora se recorre por completo 
                   while valid_space(current_piece, grid):
                       current_piece.y += 1
                   current_piece.y -= 1
                   print(convert_shape_format(current_piece))  # todo fix
        #Actualiza la pocicion de la pieza dependiendo donde el jugador quiere moverlo
        shape_pos = convert_shape_format(current_piece)
 
        # Añade color a la  pieza a la cuadricula
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
 
        # Si la pieza llega a golpear la parte interior de la cuadricula
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
 
            clear_rows(grid, locked_positions)
 
        draw_window(win)
        draw_next_shape(next_piece, win)
        pygame.display.update()
 
        # Checa si el jugador perdio para cambiar una variable importante
        if check_lost(locked_positions):
            run = False
    #Aqui se muestra el texto cuando el jugador a perdido 
    draw_text_middle("Has perdido...  :(", 40, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(2000)
 
 
def main_menu():

    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle('¡¡¡APACHURA CUALQUIER TECLA!!!', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
 
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()
 
#Aqui es donde se habre la ventana o lo que nos permite visualizar la ventana  
win = pygame.display.set_mode((s_width, s_height))
#Aqui es donde nos permite tambien agregarle un titulo al frente del lado superior de la ventana 
pygame.display.set_caption('SUPER TETRIZ BROS')
 
main_menu()  # start game
