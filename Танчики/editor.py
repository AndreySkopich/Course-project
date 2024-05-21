from tkinter import *
from config import *

editor = Tk()
editor.title("Редактор")
editor.resizable(0, 0)
#сохраняем выбранные значения
monitor_h, monitor_w = editor.winfo_screenheight(), editor.winfo_screenwidth()
editor.geometry(f'{WIDTH}x{HEIGHT}+{monitor_w//2 - WIDTH//2}+{monitor_h//2 - HEIGHT//2}')

#игровое окно
game_sc = Canvas(editor, width=WIDTH, height=HEIGHT, bg = 'khaki')
game_sc.place(x=0, y=2 * TILE)

#########ИНТЕРФЕЙС##############
interface = Canvas(editor, width=WIDTH, height=2 * TILE, bg = 'gray')
interface.place(x=0, y=0)
#################################



editor.mainloop()
