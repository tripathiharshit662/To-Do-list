from tkinter import *
from tkinter import messagebox, simpledialog
import sqlite3 as sql

def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        tasks.append(task_string)
        the_cursor.execute('insert into tasks values (?)', (task_string,))
        list_update()
        task_field.delete(0, 'end')

def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

def delete_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            the_cursor.execute('delete from tasks where title = ?', (the_value,))
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')
    if message_box == True:
        while(len(tasks) != 0):
            tasks.pop()
        the_cursor.execute('delete from tasks')
        list_update()

def clear_list():
    task_listbox.delete(0, 'end')

def close():
    print(tasks)
    guiWindow.destroy()

def retrieve_database():
    while(len(tasks) != 0):
        tasks.pop()
    for row in the_cursor.execute('select title from tasks'):
        tasks.append(row[0])

def update_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if (the_value in tasks):
            new_task = simpledialog.askstring("Update Task", "Edit the selected task:", initialvalue=the_value)
            if new_task:
                index = tasks.index(the_value)
                tasks[index] = new_task
                list_update()
                the_cursor.execute('update tasks set title = ? where title = ?', (new_task, the_value))
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Update.')

if __name__ == "__main__":
    guiWindow = Tk()
    guiWindow.title("To-Do List")
    guiWindow.geometry("665x400+550+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#FFC0CB")  

    the_connection = sql.connect('listOfTasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('create table if not exists tasks (title text)')

    tasks = []

    functions_frame = Frame(guiWindow, bg="#FFC0CB")
    functions_frame.pack(side="top", expand=True, fill="both")

    task_label = Label(functions_frame, text="TO-DO-LIST \n Enter the Task Title:",
                       font=("Times New Roman", "13", "bold"),  
                       background="#FFC0CB",
                       foreground="#FF6103")
    task_label.place(x=20, y=30)

    task_field = Entry(functions_frame,
                       font=("Times New Roman", "14"),  
                       width=42,
                       foreground="black",
                       background="white")
    task_field.place(x=180, y=30)

    add_button = Button(functions_frame,
                        text="Add",
                        width=15,
                        bg='#ADD8E6', font=("Times New Roman", "14", "bold"), 
                        command=add_task)
    del_button = Button(functions_frame,
                        text="Remove",
                        width=15,
                        bg='#ADD8E6', font=("Times New Roman", "14", "bold"),  
                        command=delete_task)
    del_all_button = Button(functions_frame,
                            text="Delete All",
                            width=15,
                            font=("Times New Roman", "14", "bold"),
                            bg='#ADD8E6',  
                            command=delete_all_tasks)
    update_button = Button(functions_frame,
                           text="Update",
                           width=15,
                           font=("Times New Roman", "14", "bold"),  
                           bg='#ADD8E6', 
                           command=update_task)
    exit_button = Button(functions_frame,
                         text="Exit",  
                         width=15,  
                         bg='#ADD8E6', font=("Times New Roman", "14", "bold"),  
                         command=close)

    task_listbox = Listbox(functions_frame,
                           width=55,
                           height=11,
                           font=("Times New Roman", "12", "bold"),  
                           selectmode='SINGLE',
                           background="WHITE",
                           foreground="BLACK",
                           selectbackground="#FF8C00",
                           selectforeground="BLACK")
    task_listbox.place(x=17, y=140)

    add_button.place(x=504, y=80)
    del_button.place(x=504, y=130)
    update_button.place(x=504, y=180)
    del_all_button.place(x=504, y=230)
    exit_button.place(x=504, y=330)

    retrieve_database()
    list_update()
    guiWindow.mainloop()
    the_connection.commit()
    the_cursor.close()