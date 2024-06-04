from tkinter import *
from config import *
from tkinter import messagebox

def size():
	
	def editor(width, height):
		global map_width, map_height
		
		map_width=width
		map_height=height
		
		WIDTH=map_width*TILE
		HEIGHT=map_height*TILE
		
		xwin=monitor_w // 2 - WIDTH // 2
		ywin=monitor_h // 2 - HEIGHT // 2
		
		creator.destroy()
		
		editor = Toplevel()
		editor.title("Редактор карты")
		editor.resizable(0, 0)
		#сохраняем выбранные значения
		editor.geometry(f'{map_width*TILE}x{map_height*TILE+TILE*2}+{xwin}+{ywin}')
		
		#игровое окно
		game_sc = Canvas(editor, width=WIDTH, height=HEIGHT, bg = 'khaki')
		game_sc.place(x=0, y=2 * TILE)

		#########ИНТЕРФЕЙС##############
		interface = Canvas(editor, width=WIDTH, height=2 * TILE, bg = 'gray')
		interface.place(x=0, y=0)
		#################################
		
		global saved
		saved = 0

		def get_texture(event):
			global selected_texture
			selected_texture[0] = all_textures[all_texture_buttons[event.widget]]
			selected_texture[1] = all_texture_buttons[event.widget]
			show_selected_texture.config(image=selected_texture[0])

		def paint(event):
			global selected_texture,map_buttons
			event.widget.config(image=selected_texture[0])
			map_buttons[event.widget][2] = selected_texture[1]

		def save_map():
			'''функция для сохранения созданной карты,
			выполняеся после нажатия кнопки save
			'''
			global saved
			saved+=1
			
			flag=0
			#проверка на наличие только 1 танка
			for i in range(map_height):
				for j in range(map_width):
					for n in map_buttons.values():
						if n[0]==i and n[1]==j and n[2]=='@':
							flag+=1
			
			if flag!=1:
				messagebox.showinfo("Прерывание сохранения", "Карта не сохранена. На поле должен быть ровно один танк.", parent=editor)
			else:
				#процесс сохранения сохданной карты
				txt = open("map.txt","w")
				
				for i in range(map_height):
					for j in range(map_width):
						for n in map_buttons.values():
							if n[0]==i and n[1]==j:
								txt.write(n[2])
					txt.write("\n")
				
				txt.close()

		def fill():
			global map_buttons
			for i in map_buttons:
				i.config(image=selected_texture[0])
				map_buttons[i][2]=selected_texture[1]

		def from_file_load():
			'''функция загружает уже созданную карту
			в режиме редактирования.
			выполняется после нажатия кнопки "Загрузить текущую"
			'''
			global map_width, map_height
			
			#этап определения размера карты
			temp_height = 0
			temp_width = 0
			#Считаем размеры поля
			txt = open("map.txt","r")
			for line in txt:
				temp_height += 1
			temp_width = len(line) - 1
			txt.close()
			
			if ((temp_height==map_height) and (temp_width==map_width)):
				#меняем разрешение экрана под игровую карту
				WIDTH = map_width*TILE
				HEIGHT = map_height*TILE	
				
				txt = open("map.txt","r")
				
				for i in range(map_width):
					for j in range(map_height):
						element = txt.read(1)
						if element=='\n': #проверка на символ переноса
							element = txt.read(1)
						for n in map_buttons.keys():
							if map_buttons[n][0]==i and map_buttons[n][1]==j:
								n.config(image=all_textures[element])
								map_buttons[n][2] = element
								
				txt.close()
			else:
				map_width=temp_width
				map_height=temp_height
				
				editor.destroy()
				editor(map_width, map_height)
				
		
		brick = PhotoImage(file="images/brick.png")
		armor = PhotoImage(file="images/armor.png")
		empty=PhotoImage(file="images/empty.png")
		tank = PhotoImage(file="images/tank_up.png")
		
		all_textures = {'.':empty,'%':brick, '#':armor, '@':tank}
		
		cnt=0
		all_texture_buttons = {}
		#создание кнопок для выбора блоков
		for i in all_textures.keys():
			texture_button = Button(interface, image=all_textures[i])
			texture_button.place(x=16+cnt*(TILE+16), y=16)
			all_texture_buttons[texture_button] = i
			cnt+=1
			texture_button.bind('<Button-1>', get_texture)
		
		global selected_texture
		selected_texture=[empty,'.']
		global map_buttons
		map_buttons = {}
		
		#заполнение карты пустыми блоками для редактирования
		for i in range(map_height):
			for j in range(map_width):
				map_button = Button(game_sc,image=empty, width=26, height=26, bg = 'khaki')
				map_button.bind('<Button-1>',paint)
				map_buttons[map_button] = [i, j, '.']
				map_button.grid(row=i, column=j)
				
		show_selected_texture = Button(interface, image=empty, command=fill)
		show_selected_texture.place(x=WIDTH-6*TILE, y=16)
		
		save_in_file_button = Button(interface,text="Сохранить изменения",command = save_map)
		save_in_file_button.place(x=WIDTH-4*TILE, y= 6)
		
		load_from_file_button = Button(interface,text="Загрузить текущую",command=from_file_load)
		load_from_file_button.place(x=WIDTH-4*TILE, y= 38)
		
		editor.mainloop()
	
	creator = Toplevel()
	creator.title("Настройка размеров")
	creator.resizable(0, 0)
	monitor_h, monitor_w = creator.winfo_screenheight(), creator.winfo_screenwidth()
	creator.geometry(f'330x150+{int(monitor_w//2 - 400)}+{monitor_h//2 - 300}')
	label=Label(creator, text="Выберите размер поля в блоках или оставьте по умолчанию").place(relx=0.5, anchor=N)
	
	Label(creator, text="Ширина в блоках:").place(relx=0.0, rely=0.4, anchor=W)
	Label(creator, text="Высота в блоках:").place(relx=0.0, rely=0.6, anchor=W)
	
	width_entry = IntVar() 
	width_entry.set(20) 

	height_entry = IntVar() 
	height_entry.set(20) 

	entry_1 = Entry(creator, width=5, textvariable=width_entry)
	entry_1.place(relx=0.3, rely=0.4, anchor=W)

	entry_2 = Entry(creator, width=5, textvariable=height_entry)
	entry_2.place(relx=0.3, rely=0.6, anchor=W)
	
	Btn=Button(creator, text="Применить", command=lambda: editor(int(entry_1.get()), int(entry_2.get()))).place(relx=0.9, rely=0.9, anchor=SE)
	
	creator.mainloop()


