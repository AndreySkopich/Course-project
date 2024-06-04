from tkinter import *
from config import *
from game import *
from about import *
from game import *
from map_editor import *

#создание окна меню программы
tk = Tk()
tk.title("Танчики")
tk.resizable(0, 0)
#определение размеров монитора для центрирования окна программы
monitor_h, monitor_w = tk.winfo_screenheight(), tk.winfo_screenwidth()
tk.geometry(f'800x600+{int(monitor_w//2 - 400)}+{monitor_h//2 - 300}')

menu_image = PhotoImage(file = 'images/menu.png') 

def already_exist(event):
	'''функция предназначена для отслеживания,
		чтобы запретить запуск одного окна дважды'''
	global next
	if event.widget != tk:
		next = True

#проверка на закрытие окна 
tk.bind_all("<Destroy>", already_exist)

######меню#################
canvas = Canvas(tk, height = 600, width = 800)
tk.geometry(f'800x600+{monitor_w//2 - 400}+{monitor_h//2 - 300}')
image = canvas.create_image(0, 0, anchor='nw',image=menu_image)
#создание кнопок для меню
menu_but_1 = Button(canvas, text = "Играть", command = main, width = "40", height = "2", bg = "white").place(x = 280, y = 400)
menu_but_2 = Button(canvas, text = "Редактор карты", command = size, width = "40", height = "2", bg = "white").place(x = 280, y = 450)
menu_but_3 = Button(canvas, text = "Об игре", width = "40", command = about, height = "2", bg = "white").place(x = 280, y = 500)
menu_but_4 = Button(canvas, text = "Выход", command = exit, width = "40", height = "2", bg = "white").place(x = 280, y = 550)

canvas.pack()

tk.mainloop()
