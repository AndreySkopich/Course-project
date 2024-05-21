def is_creating(creator):
	map_width=entry_1.get()
	map_height=entry_2.get()
	
	creator = Toplevel()
	creator.title("Редактор")
	creator.resizable(0, 0)
	#сохраняем выбранные значения
	creator.geometry(f'{map_width*TILE}x{map_height*TILE}')
