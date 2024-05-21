from tkinter import *

def about():
	about_sc = Toplevel()
	about_sc.title("Об игре")
	about_sc.resizable(0, 0)
	
	monitor_h, monitor_w = about_sc.winfo_screenheight(), about_sc.winfo_screenwidth()
	about_sc.geometry(f'400x300+{int(monitor_w//2 - 400)}+{monitor_h//2 - 300}')
	
	about_1 = Label(about_sc, text="Игра \"Taнчики\"\n", font=("Arial", 14, 'bold')).place(relx=0.5, rely=0.0, anchor=N)
	Label(about_sc, text="---------------------------------------", font=("Arial", 14), fg="gray").place(relx=0.5, rely=0.1, anchor=N)
	about_2 = Label(about_sc, text="Управление", font=("Arial", 14, 'bold')).place(relx=0.5, rely=0.2, anchor=N)
	about_3 = Label(about_sc, text="Стрелочки - перемещение,", font=("Arial", 14)).place(relx=0.0, rely=0.4, anchor=W)
	about_4 = Label(about_sc, text="Пробел - стрельба.", font=("Arial", 14)).place(relx=0.0, rely=0.5, anchor=W)
	Label(about_sc, text="---------------------------------------", font=("Arial", 14), fg="gray").place(relx=0.5, rely=0.7, anchor=N)
	about_5 = Label(about_sc, text="Работу выполнил:", font=("Arial", 14, 'bold')).place(relx=0.0, rely=0.9, anchor=SW)
	about_6 = Label(about_sc, text="студент 5.205-1 группы Скопич А. П.", font=("Arial", 14)).place(relx=0.0, rely=1, anchor=SW)
	
	about_sc.mainloop()
