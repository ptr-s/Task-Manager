import tkinter as tk
from tkinter import ttk
#import tkcalendar as tkc
#import datetime as dt

def callback_entry(sv):
    task = sv.get()
    if task:
        add_button.config(state=tk.NORMAL)
    else:
        add_button.config(state=tk.DISABLED)

def add_task():
    task = ("", entry_task.get())
    if task[1]:
        task_list.insert('', tk.END, values=task)

def update_task():
    new_task_value = entry_task.get()
    if new_task_value:
        selected_tasks = task_list.selection()
        for i in selected_tasks:
            old_task = task_list.item(i, 'values')
            task = (old_task[0], new_task_value)
            task_list.item(i, value=task)

def delete_task():
    selected_tasks = task_list.selection()
    for i in selected_tasks:
        task_list.delete(i)

def delete_task_event(event):
    delete_task()

def entry_task_return_key_event(event):
    add_task()

def task_selected(event):
    selected_tasks = task_list.selection()
    if selected_tasks:
        delete_button.config(state=tk.NORMAL)
        update_button.config(state=tk.NORMAL)
    else:
        delete_button.config(state=tk.DISABLED)
        update_button.config(state=tk.DISABLED)
    entry_task.delete(0, tk.END)
    if len(selected_tasks) == 1:
        task = task_list.item(selected_tasks[0], 'values')
        entry_task.insert(0, task[1])

def task_state_change(event):
    selected_tasks = task_list.selection()
    for i in selected_tasks:
        task = task_list.item(i, 'values')
        if task[0]:
            state = ""
            tag = ""
        else:
            state = "\u2714" # check = "\u2713" "\u2714" u"\u2705 "
            tag = "checked"
        task_list.item(i, tags=tag, value=(state, task[1]))


main_window = tk.Tk()
main_window.title("Менеджер задач")
main_window.iconphoto(False, tk.PhotoImage(file="icons/tasks_list.png"))
main_window.wm_minsize(width=395, height=200)
main_window.geometry("395x500")


# Task manage
frame_task = tk.LabelFrame(main_window, text="Введите вашу задачу: ")
frame_task.pack(side=tk.TOP, anchor=tk.NW, fill=tk.X)

# Task Data
frame_task_data = tk.Frame(frame_task)
frame_task_data.pack(side=tk.TOP, anchor=tk.NW, fill=tk.X)

sv = tk.StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: callback_entry(sv))
entry_task = tk.Entry(frame_task, bg="paleturquoise1", textvariable=sv)
entry_task.bind("<Return>", entry_task_return_key_event)
entry_task.pack(padx=10, pady=5, side=tk.TOP, anchor=tk.NW, fill=tk.X)
"""
# Task Dates
frame_task_dates = tk.Frame(frame_task)
frame_task_dates.pack(pady=5, side=tk.TOP, anchor=tk.NW, fill=tk.X)
"""
# Task Action
frame_task_action = tk.Frame(frame_task)
frame_task_action.pack(side=tk.TOP, anchor=tk.NW, fill=tk.X)

image_add = tk.PhotoImage(file="icons/add.png")
add_button = tk.Button(frame_task_action, image=image_add, text="Добавить", compound="left",
                       command=add_task, state=tk.DISABLED)
add_button.pack(padx=5, pady=5, side=tk.LEFT)

image_update = tk.PhotoImage(file="icons/pencil.png")
update_button = tk.Button(frame_task_action, image=image_update, text="Обновить", compound="left",
                          command=update_task, state=tk.DISABLED)
update_button.pack(padx=5, pady=5, side=tk.LEFT)

image_delete = tk.PhotoImage(file="icons/trash.png")
delete_button = tk.Button(frame_task_action, image=image_delete, text="Удалить",
                          compound="left", command=delete_task, state=tk.DISABLED)
delete_button.pack(padx=5, pady=5, side=tk.LEFT)

# Task List
frame_task_list = tk.Frame(main_window)
frame_task_list.pack(fill=tk.BOTH, expand = True)

style = ttk.Style(frame_task_list)
style.configure("Treeview", background="moccasin", fieldbackground="moccasin")
columns = ('state', 'task')
task_list = ttk.Treeview(frame_task_list, columns=columns, show='headings')
# darkolivegreen1 - darkolivegreen4,  palegreen-(152,251,152) / palegreen4-(84,139,84) darkolivegreen4 olivedrab4
task_list.tag_configure(tagname="checked", background="palegreen")
task_list.bind("<<TreeviewSelect>>", task_selected)
task_list.bind("<Return>", task_state_change)
task_list.bind("<space>", task_state_change)
task_list.bind("<Double-Button-1>", task_state_change)
task_list.bind("<Delete>", delete_task_event)

# headings
task_list.heading(columns[0], text='', anchor=tk.CENTER)
task_list.heading(columns[1], text='Задача', anchor=tk.W)
task_list.column(columns[0], width=24, anchor=tk.CENTER, stretch=False)
task_list.column(columns[1], anchor=tk.W, stretch=True)

# add a scrollbar
scrollbar = ttk.Scrollbar(frame_task_list, orient=tk.VERTICAL, command=task_list.yview)
task_list.config(yscroll=scrollbar.set)

task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand = True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

tk.mainloop()
