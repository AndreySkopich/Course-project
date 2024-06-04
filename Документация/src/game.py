from tkinter import *
from random import *
import time
from random import *
from config import *

def main():
	global title_score
	##Загрузка игровой карты из файла###
	#чтение карты из файла
	map_file = open('map.txt', 'r')
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
	
	root = Toplevel()
	root.title("Танчики")
	root.resizable(0, 0)
	
	class Bullet:
		def __init__(self, x, y, vx, vy, ouner):
			bullets.append(self)
			#начальные координаты
			self.x, self.y = x, y
			#задание направления
			self.vx, self.vy = vx, vy
			self.ouner = ouner
			#русуем снаряд
			self.bullet = game_sc.create_oval(self.x, self.y, self.x + 5, self.y + 5, fill='black')
		
		def update(self):
			#двигаем снаряд
			self.x += self.vx
			self.y += self.vy
			game_sc.move(self.bullet, self.vx, self.vy)
			
			#проверка столкновения стенами поля или с объектами
			if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
				game_sc.delete(self.bullet)
				bullets.remove(self)
			else:
				for obj in objects:
					if (obj.x <= self.x <= obj.x + TILE) and (obj.y <= self.y <= obj.y + TILE):
						game_sc.delete(self.bullet)
						bullets.remove(self)
						if obj.model == brick:
							game_sc.delete(obj.model)
						break
				
				#проверка на столкновение
				#с вражеским танком
				if self.ouner == 'player':
					for obj in enemies:
						if (obj.x <= self.x <= obj.x + TILE) and (obj.y <= self.y <= obj.y + TILE):
							#удаление сеарядов
							game_sc.delete(self.bullet)
							bullets.remove(self)
							obj.explosion()
							#удаление (уничтожение) танка
							enemies.remove(obj)
							game_sc.delete(obj.enemy_img)
							obj.life = False
							break
				#с игроком
				if self.ouner == 'enemy':
					if (player.x <= self.x <= player.x + TILE) and (player.y <= self.y <= player.y + TILE):
							#удаление снарядов
							game_sc.delete(self.bullet)
							bullets.remove(self)
							#удаление (уничтожение) танка
							player.lives -= 1
							lives_label['text'] =str(player.lives)
				
	class Enemy:
		def __init__(self, x, y):
			#координаты движения танков
			enemies.append(self)
			#координаты
			self.x = x
			self.y = y
			#скорости (направления)
			self.vx = 0
			self.vy = 0
			#предыдущий шаг(координаты)
			old_x = self.x
			old_y = self.y
			
			self.i=0#переменная для анимации
			
			self.life = True
			#установка изображения танка
			self.enemy_img = game_sc.create_image(self.x, self.y, anchor=NW, image=enemy[0])
			
			#начальное направление движения
			self.change_dir(old_x,old_y)
			
			#запустить циклы случайного поворота и стрельбы
			game_sc.after(randint(3000, 5000), self.rand_change_dir)
			game_sc.after(1000, self.shoot)
			
		def rand_change_dir(self):
			'''функция для случайной смены 
			направления вражеского танка'''
			if self.life == True:
				self.rand = random()
				if self.rand <= 0.25:
					game_sc.itemconfig(self.enemy_img, image=enemy[2])
					self.vy = E_SPEED
					self.vx = 0
				elif self.rand <= 0.5:
					self.vy = -E_SPEED
					self.vx = 0
					game_sc.itemconfig(self.enemy_img, image=enemy[0])
				elif self.rand <= 0.75:
					self.vx = E_SPEED
					self.vy = 0
					game_sc.itemconfig(self.enemy_img, image=enemy[1])
				elif self.rand <= 1:
					self.vx = -E_SPEED
					self.vy = 0
					game_sc.itemconfig(self.enemy_img, image=enemy[3])
					
				game_sc.after(randint(3000, 5000), self.rand_change_dir)
		
		def change_dir(self, old_x, old_y):
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
				game_sc.itemconfig(self.enemy_img, image=enemy[2])
			elif self.rand <= 0.5:
				self.vy = -E_SPEED
				self.vx = 0
				game_sc.itemconfig(self.enemy_img, image=enemy[0])
			elif self.rand <= 0.75:
				self.vx = E_SPEED
				self.vy = 0
				game_sc.itemconfig(self.enemy_img, image=enemy[1])
			elif self.rand <= 1:
				self.vx = -E_SPEED
				self.vy = 0
				game_sc.itemconfig(self.enemy_img, image=enemy[3])
		
		def shoot(self):
			'''задает для врага случайную стрельбу'''
			if self.life == True:
				if self.vx > 0:
					Bullet(self.x + TILE/2, self.y + TILE/2, B_SPEED, 0, 'enemy')
				elif self.vx < 0:
					Bullet(self.x + TILE/2, self.y + TILE/2, -B_SPEED, 0, 'enemy')
				elif self.vy > 0:
					Bullet(self.x + TILE/2, self.y + TILE/2, 0, B_SPEED, 'enemy')
				elif self.vy < 0:
					Bullet(self.x + TILE/2, self.y + TILE/2, 0, -B_SPEED, 'enemy')
					
				game_sc.after(1000, self.shoot)
			
		def explosion(self):
			'''эффект взрыва танка'''
			exp=game_sc.create_image(self.x, self.y, anchor=NW, image=bang[self.i])
			if (self.i<2):
				exp=game_sc.create_image(self.x, self.y, anchor=NW, image=bang[self.i])
				self.i+=1
				game_sc.after(100, self.explosion)
			else:
				self.i=0
				game_sc.delete(exp)
				
		
		def update(self):
			#записываем начальные координаты
			old_x = self.x
			old_y = self.y
			
			#постоянное перемещение
			self.y += self.vy
			self.x += self.vx
			
			#проверка на столкновение с краями поля
			#в таком случае, враг поменяет (перегенерируют) свое направление
			if (self.x + TILE + E_SPEED >= WIDTH) or (self.x - E_SPEED <= 0) or (self.y + 
				TILE + E_SPEED >= HEIGHT) or (self.y - E_SPEED <= 0):
				#меняем направление
				self.change_dir(old_x, old_y)
			
			#проверка на столкновение с объектами и другими танками
			for obj in enemies+objects:
				if (self!=obj):
					if (obj.x - TILE < self.x) and (obj.x + TILE > self.x) and (obj.y - TILE < self.y) and (obj.y + TILE > self.y):
						#меняем направление
						self.change_dir(old_x, old_y)
		
			#проверка столкновения с игроком
			if (player.x - TILE < self.x) and (player.x + TILE > self.x) and (player.y - TILE < self.y) and (player.y + TILE > self.y):
				#перегенерим направление
				self.change_dir(old_x, old_y)
			
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
			#направление для снаряда
			self.direct = 'up'
			self.lives = 3
			
			#время задержки и таймер для стрельбы
			self.shotTimer = 0
			self.shotDelay = 5
			
			#установка изображения танка для игрока
			self.player_img = game_sc.create_image(self.x, self.y, anchor=NW, image=tank[0])
		
		def move(self, event):
			'''управление движением игрока с помощью
			стрелок, зажатие определенной кнопки
			перемещает игрока только в одну из 4 сторон'''
			if event.keysym == 'Left':
				self.vx = -SPEED
				self.vy = 0
				self.direct = 'left'
				game_sc.itemconfig(self.player_img, image=tank[3])
			elif event.keysym == 'Right':
				self.vx = SPEED
				self.vy = 0
				self.direct = 'right'
				game_sc.itemconfig(self.player_img, image=tank[1])
			elif event.keysym == 'Up':
				self.vy = -SPEED
				self.vx = 0
				self.direct = 'up'
				game_sc.itemconfig(self.player_img, image=tank[0])
			elif event.keysym == 'Down':
				self.vy = SPEED
				self.vx = 0
				self.direct = 'down'
				game_sc.itemconfig(self.player_img, image=tank[2])
			
		def shoot(self, event):
			if event.keysym == 'space' and self.shotTimer == 0:
				#определяем скорость и направление снаряда
				if self.direct == 'up':
					Bullet(self.x + TILE/2, self.y + TILE/2, 0, -B_SPEED, 'player')
				elif self.direct == 'down':
					Bullet(self.x + TILE/2, self.y + TILE/2, 0, B_SPEED, 'player')
				elif self.direct == 'right':
					Bullet(self.x + TILE/2, self.y + TILE/2, B_SPEED, 0, 'player')
				elif self.direct == 'left':
					Bullet(self.x + TILE/2 + 1, self.y + TILE/2 + 1, -B_SPEED, 0, 'player')
				#таймер на запрет стрельбы
				self.shotTimer = self.shotDelay
				game_sc.after(fire_cooldown, cooldown)

		def stop(self, event):
			if (event.keysym == 'Up' or event.keysym == 'Down'):
				self.vy = 0
			if (event.keysym == 'Left' or event.keysym == 'Right'):
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
			
			#проверка на столкновение игрока с объектами и вражескими танками
			for obj in objects + enemies:
				if (obj.x - TILE < self.x) and (obj.x + TILE > self.x) and (obj.y - TILE < self.y) and (obj.y + TILE > self.y):
					self.x = old_x
					self.y = old_y
			
			#перемещение игрока (его изображение)
			game_sc.coords(player.player_img, self.x, self.y)

	class Block:
		def __init__(self, model, x, y):
			'''класс для создания структур в виде кирпичных стен,
			воды и неломаемых стен.'''
			objects.append(self)
			self.model = model
			self.x = x
			self.y = y
			
			#отрисовка блока на поле
			game_sc.create_image(self.x, self.y, anchor=NW, image=self.model)
	
	def spawn():
		'''Функция создает вражеский танк в случайной
		позиции на карте
		Функция ничего не принимает
		и ничего не выводит
		'''
		
		# Создаем  массив для определения занятых блоков, заполненный нулями
		mass = [[[0] for _ in range(map_height)] for _ in range(map_width)]
		
		#проходимся в поисках занятых блоков и помечаем заполненные 1
		for h in range(map_height):
			for w in range(map_width):
				block_free = True
				for obj in objects + enemies:
					if (w * TILE - TILE < obj.x < w * TILE + TILE) and (h * TILE - TILE < obj.y < h * TILE + TILE):
						block_free = False
						break
				if (block_free==True):
					mass[w][h][0] = 1 
				else:
					mass[w][h][0] = 0
		
		# Создаем список свободных позиций
		free_positions = [(w, h) for w in range(map_width) for h in range(map_height) if mass[w][h][0] == 1]

		# Выбор случайной свободной позиции из списка
		rand_pos_x, rand_pos_y = choice(free_positions)
		
		Enemy(rand_pos_x*TILE+1, rand_pos_y*TILE+1)
	
	def cooldown():
		'''функция относится к классу tank и нужна 
		для задержки выстрела
		'''
		#убавление таймеры на запрет стрельбы
		player.shotTimer=0
	
	#раздел загрузки изображений
	brick = PhotoImage(file="images/brick.png")
	armor = PhotoImage(file="images/armor.png")
	lives = PhotoImage(file="images/lives.png")
	tank = [PhotoImage(file="images/tank_up.png"),
					PhotoImage(file="images/tank_right.png"),
					PhotoImage(file="images/tank_down.png"),
					PhotoImage(file="images/tank_left.png")]		
	enemy = [PhotoImage(file="images/enemy_up.png"),
					PhotoImage(file="images/enemy_right.png"),
					PhotoImage(file="images/enemy_down.png"),
					PhotoImage(file="images/enemy_left.png")]
	bang=[PhotoImage(file="images/bang1.png"),
					PhotoImage(file="images/bang2.png"),
					PhotoImage(file="images/bang3.png")]
	
	objects = [] #хранит все структуры на поле
	enemies = [] #хранит всех врагов на поле
	bullets = [] #хранит все летящие снаряды

	#определение размера и центрирование окна
	monitor_h, monitor_w = root.winfo_screenheight(), root.winfo_screenwidth()
	root.geometry(f'{WIDTH + 4}x{HEIGHT + 2*TILE + 4}+{int(monitor_w//2 - WIDTH//2)}+{monitor_h//2 - HEIGHT//2}')

	#игровое окно
	game_sc = Canvas(root, width=WIDTH, height=HEIGHT, bg = 'khaki')
	game_sc.place(x=0, y=2 * TILE)

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
	#################################

	#########ИНТЕРФЕЙС##############
	interface = Canvas(root, width=WIDTH, height=2 * TILE, bg = 'gray')
	interface.place(x=0, y=0)

	#вывод счета
	title_score = 0
	score_label = Label(interface, bg="gray", font=("Comic Sans MS", 25), text="Счёт:" + str(title_score))
	score_label.place(x=3, y=3)
	#вывод кол-ва жизней
	interface.create_image(WIDTH - 150, 0, anchor=NW, image=lives)
	lives_label = Label(interface, bg='black', font=("Comic Sans MS", 20), text=str(player.lives), fg="white")
	lives_label.place(x=WIDTH - 105, y=8)
	#################################

	#создаем 5 начальных врагов
	for k in range(1, 5):
		spawn()

	#управление через клавиши
	root.bind_all("<Key>", player.move)
	root.bind_all("<KeyRelease>", player.stop)
	root.bind_all("<space>", player.shoot)
	
	def game():
		global title_score
		
		for obj in enemies:
			obj.update()
		
		player.update()
		
		for obj in bullets:
			obj.update()
		
		#повторная генерация танков
			if len(enemies) < 4:
				#размещение нового противника
				spawn()
				#начисление очков за уничтожение
				title_score += 100
				score_label['text'] = "Счёт:" + str(title_score)
		
		#условие продолжения игры
		if player.lives > 0:
			game_sc.after(20, game)
		else:
			#подготовка для выхода из игры
			root.unbind_all("<Key>")
			root.unbind_all("<KeyRelease>")
			for obj in objects:
				objects.remove(obj)
			for obj in bullets:
				game_sc.delete(obj.bullet)
				bullets.remove(obj)
			for obj in enemies:
				obj.life = False
				enemies.remove(obj)
				#game_sc.delete("all")
				#root.destroy()
	
	game_sc.update()
	game()

	root.mainloop()
