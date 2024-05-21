from tkinter import *
from config import *

def map_editor():
	
	def is_creating():
		map_width=entry_1.get()
		map_height=entry_2.get()
		
		creator_2 = Toplevel()
		creator_2.title("Редактор")
		creator_2.resizable(0, 0)
		#сохраняем выбранные значения
		creator_2.geometry(f'{WIDTH}x{HEIGHT}+{monitor_w//2 - WIDTH//2}+{monitor_h//2 - HEIGHT//2}')
		
		creator_2.mainloop()
	
	creator = Toplevel()
	creator.title("Редактор")
	creator.resizable(0, 0)
	monitor_h, monitor_w = creator.winfo_screenheight(), creator.winfo_screenwidth()
	creator.geometry(f'330x150+{int(monitor_w//2 - 400)}+{monitor_h//2 - 300}')
	label=Label(creator, text="Выберите размер поля в блоках или оставьте по умолчанию").place(relx=0.5, anchor=N)
	
	Label(creator, text="Ширина в блоках:").place(relx=0.0, rely=0.4, anchor=W)
	Label(creator, text="Высота в блоках:").place(relx=0.0, rely=0.6, anchor=W)
	
	width_entry = IntVar() 
	width_entry.set(map_width) 

	height_entry = IntVar() 
	height_entry.set(map_height) 

	entry_1 = Entry(creator, textvariable=width_entry)
	entry_1.place(relx=0.3, rely=0.4, anchor=W)

	entry_2 = Entry(creator, textvariable=height_entry)
	entry_2.place(relx=0.3, rely=0.6, anchor=W)
	
	Btn=Button(creator, text="Применить", command=is_creating).place(relx=0.9, rely=0.9, anchor=SE)
	
	creator.mainloop()


