from tkinter import *
from random import *
import time

#константы
map_width = 20
map_height = 20
TILE = 40 #размер блока (фиксированный)
WIDTH = map_width*TILE  #ширина и длина игрового пространства, меняется в зависимости от кол-ва блоков
HEIGHT = map_height*TILE #10- минимум
FPS = 60 #кол-во кадров игры
SPEED = 4
E_SPEED = 3
objects = [] #хранит все структуры
enemies = []

#удобный выход
def closing():
	tk.destroy()

tk = Tk()
tk.protocol("WM_DELETE_WINDOW", closing)
tk.geometry('600x800')
tk.title("Танчики")
tk.resizable(0, 0)

#определение размеров монитора для центрирования окна программы
monitor_h, monitor_w = tk.winfo_screenheight(), tk.winfo_screenwidth()

class Enemy:
	def __init__(self, x, y):
		#координаты движения игрока
		enemies.append(self)
		self.x = x
		self.y = y
		
		#начальное направление движения
		self.rand = random()
		if self.rand <= 0.25:
			self.vy = E_SPEED
			self.vx = 0
		elif self.rand <= 0.5:
			self.vy = -E_SPEED
			self.vx = 0
		elif self.rand <= 0.75:
			self.vx = E_SPEED
			self.vy = 0
		elif self.rand <= 1:
			self.vx = -E_SPEED
			self.vy = 0
		
		#установка изображения танка для игрока
		self.enemy_img = game_sc.create_image(self.x, self.y, anchor=NW, image=enemy)
	
	def change_dir(self):
		'''функция для случайной смены 
		направления вражеского танка'''
		self.rand = random()
		if self.rand <= 0.25:
			self.vy = E_SPEED
			self.vx = 0
		elif self.rand <= 0.5:
			self.vy = -E_SPEED
			self.vx = 0
		elif self.rand <= 0.75:
			self.vx = E_SPEED
			self.vy = 0
		elif self.rand <= 1:
			self.vx = -E_SPEED
			self.vy = 0
		
		game_sc.after(randint(3000, 5000), self.change_dir)
	
	def ch_dir(self, old_x, old_y):
		'''функция для смены направления
		вражеского танка при столкновениях'''
		#возвращаем на старые координаты
		self.x = old_x
		self.y = old_y
		#перегенерим направление
		self.rand = random()
		if self.rand <= 0.25:
			self.vy = E_SPEED
			self.vx = 0
		elif self.rand <= 0.5:
			self.vy = -E_SPEED
			self.vx = 0
		elif self.rand <= 0.75:
			self.vx = E_SPEED
			self.vy = 0
		elif self.rand <= 1:
			self.vx = -E_SPEED
			self.vy = 0
	
	def update(self):
		#записываем начальные координаты
		old_x = self.x
		old_y = self.y
		
		#обеспечение постоянного движения
		self.y += self.vy
		self.x += self.vx
		
		#проверка на столкновение со стенами
		#в таком случае, враг поменяет (перегенерируют) свое направление
		if (self.x + TILE + E_SPEED >= WIDTH) or (self.x - E_SPEED <= 0) or (self.y + 
			TILE + E_SPEED >= HEIGHT) or (self.y - E_SPEED <= 0):
			#меняем направление
			self.ch_dir(old_x, old_y)

		#проверка столкновения с объектами
		for obj in objects:
			obj_coord = game_sc.coords(obj.rect)
			if (obj_coord[0] - TILE < self.x) and (obj_coord[0] + TILE > self.x) and (obj_coord[1] - TILE < self.y) and (obj_coord[1] + TILE > self.y):
				#меняем направление
				self.ch_dir(old_x, old_y)
		
		#проверка столкновения с другими танками
		#for obj in enemies:
		#	enemy_coord = game_sc.coords(obj.enemy_img)
		#	if (enemy_coord[0] - TILE < self.x) and (enemy_coord[0] + TILE > self.x) and (enemy_coord[1] - TILE < self.y) and (enemy_coord[1] + TILE > self.y):
		#		#меняем направление
		#		self.ch_dir(old_x, old_y)
		
		#проверка столкновения с игроком
		if (player.x - TILE < self.x) and (player.x + TILE > self.x) and (player.y - TILE < self.y) and (player.y + TILE > self.y):
			#перегенерим направление
			self.ch_dir(old_x, old_y)
		
		#отрисовка врага на новом месте
		game_sc.coords(self.enemy_img, self.x, self.y)

class Tank:
	def __init__(self, x, y):
		'''конструктор класса, создает игрока - танк
		с начальными параметрами:
		-x, y - начальные координаты (а в дальнейшем просто координаты)
		-vx, vy - скорости по осям (нужны для плавного передвижения игрока)'''
		#координаты игрока
		self.x = x
		self.y = y
		#возможность движения
		self.vx = 0
		self.vy = 0
		#установка изображения танка для игрока
		self.player_img = game_sc.create_image(self.x, self.y, anchor=NW, image=tank)
	
	def move(self, event):
		'''управление движением игрока с помощью
		стрелок, зажатие определенной кнопки
		перемещает игрока только в одну из 4 сторон'''
		if event.keysym == 'Left':
			self.vx = -SPEED
			self.vy = 0
		elif event.keysym == 'Right':
			self.vx = SPEED
			self.vy = 0
		elif event.keysym == 'Up':
			self.vy = -SPEED
			self.vx = 0
		elif event.keysym == 'Down':
			self.vy = SPEED
			self.vx = 0
	
	def update(self):
		'''перемещение и логика
		столкновений игрока'''
		#записываем координаты для возможности
		#возвращения игрока при столкновении
		old_x = self.x
		old_y = self.y
		
		#постоянное изменение скорости (для меньшей зависимости от нажатия клавиш)
		player.x += player.vx
		player.y += player.vy
		
		#проверка столкновения игрока с краями поля
		if self.x + TILE >= WIDTH:
			self.x = old_x
		if self.x <= 0:
			self.x = old_x
		if self.y + TILE >= HEIGHT:
			self.y = old_y
		if self.y <= 0:
			self.y = old_y
		
		#проверка на столкновение игрока с объектами
		for obj in objects:
			obj_coord = game_sc.coords(obj.rect)
			if (obj_coord[0] - TILE < self.x) and (obj_coord[0] + TILE > self.x) and (obj_coord[1] - TILE < self.y) and (obj_coord[1] + TILE > self.y):
				self.x = old_x
				self.y = old_y
		
		#проверка столкновения игрока с вражескими танками
		for _ in enemies:
			if (_.x - TILE < self.x) and (_.x + TILE > self.x) and (_.y - TILE < self.y) and (_.y + TILE > self.y):
				self.x = old_x
				self.y = old_y
		
		#перемещение игрока (его изображение)
		game_sc.coords(player.player_img, self.x, self.y)

class Block:
	def __init__(self, model, x, y):
		'''класс для создания структур в виде кирпичных стен,
		воды и неломаемых стен.'''
		objects.append(self)
		self.rect = game_sc.create_rectangle(x - 1, y - 1, x+TILE, y+TILE, outline = 'black')
		self.model = model
		self.x = x
		self.y = y
		
	def draw(self):
		game_sc.create_image(self.x, self.y, anchor=NW, image=self.model)

#раздел загрузки изображений
menu_img = PhotoImage(file="images/menu.png")
brick = PhotoImage(file="images/brick.png")
armor = PhotoImage(file="images/armor.png")
tank = PhotoImage(file="images/tank.png")
enemy = PhotoImage(file="images/enemy.png")

#################################
##Загрузка игровой карты из файла###
#################################

#чтение карты из файла
map_file = open('default_map.txt', 'r')
#Расчет размера поля
map_height = 0
map_width = 0

#Считаем размеры поля
for line in map_file:
	map_height += 1
	map_width = len(line) - 1

#перенос каретки в начало файла для
#повторного чтения
map_file.seek(0)

#меняем разрешение экрана под игровую карту
WIDTH = map_width*TILE
HEIGHT = map_height*TILE

#меняе окно
tk.geometry(f'{WIDTH + 4}x{HEIGHT + 2*TILE + 4}+{int(monitor_w//2 - WIDTH//2)}+{monitor_h//2 - HEIGHT//2}')
#интерфейс
interface = Canvas(tk, width=WIDTH, height=2 * TILE, bg = 'gray')
interface.place(x=0, y=0)
#игровое окно
game_sc = Canvas(tk, width=WIDTH, height=HEIGHT, bg = 'khaki')
game_sc.place(x=0, y=2 * TILE)

#создаем текст
interface.create_text(50, 30, text="Счёт:", font=("Comic Sans MS", 25), fill="black")
title_score = 0

#строим карту
for col in range(0, map_height):
	for row in range(0, map_width + 1):
		element = map_file.read(1)
		if element == '%':
			Block(brick, row*TILE + 1, col*TILE +1)
		elif element == '#':
			Block(armor, row*TILE + 1, col*TILE + 1)
		elif element == '@':
			player = Tank(row*TILE + 1, col*TILE + 1)

map_file.close()
##############################

#отрисовка блоков
for obj in objects:
	obj.draw()

#создаем 5 врагов
for k in range(1, 5):
	rand_pos_x = choice([100, WIDTH - 100])
	rand_pos_y = choice([100, HEIGHT - 100])
	Enemy(rand_pos_x, rand_pos_y)

for _ in enemies:
	game_sc.after(3000, _.change_dir)

#управление через клавиши
tk.bind("<Key>", player.move)

def game():
	for _ in enemies:
		_.update()
	
	player.update()
	
	game_sc.update()
	tk.after(15, game)
	
game()
	
tk.mainloop()
