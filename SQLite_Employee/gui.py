import customtkinter
from tkinter import *
from tkinter import ttk, Label
import tkinter as tk
from tkinter import messagebox
import main
import pyodbc as odb
import csv


def create_window():
    app=customtkinter.CTk()
    app.title("Employee Management System")
    app.geometry("1200x800")
    app.config(bg="#091030")
    app.resizable(False,False)

    font1=('Arial',20,'bold')
    font2=('Arial',16,'bold')
    font3=('Arial',12,'bold')
    font4=('Times',20,'bold')

    def add_to_treeview():
        employees=main.fetch_employees()
        tree.delete(*tree.get_children())
        for employee in employees:
            tree.insert('',END,values=employee)


    def show_employee_info():
        employee_id_str = int(id_entry.get())
        if not employee_id_str:
            messagebox.showerror('ERROR','Please enter ID')
        else:
            try:
                employee_id=int(employee_id_str)
                employee=main.get_employee_by_id(employee_id)
                if employee:
                    name_label.configure(text="NAME : " + employee[1])
                    role_label.configure(text="ROLE : " + employee[2])
                    gender_label.configure(text="GENDER: " + employee[3])
                    status_label.configure(text="STATUS: " + employee[4])
                    date_of_birth_label.configure(text="DATE: " + employee[5])

                else:
                    name_label.configure(text="Employee not found")
            except ValueError:
                 messagebox.showerror('Error', 'Invalid ID. Please enter a valid integer')
                 
    def search_info():
        root = Tk()
        root.title("Employee Finder")
        root.geometry("400x300")

        id_label = Label(root, text="Enter ID:")
        id_label.pack()

        id_entry = Entry(root)
        id_entry.pack()

        search_button = Button(root, text="Search", command=show_employee_info)
        search_button.pack()

        name_label = Label(root, text="Name:")
        name_label.pack()

        role_label = Label(root, text="Role:")
        role_label.pack()

        gender_label=Label(root,text="Gender:")
        gender_label.pack()

        status_label=Label(root,text="Status:")
        status_label.pack()

        date_of_birth_label=Label(root,text="Date_Of_Birth:")
        date_of_birth_label.pack()

    def insert():
        id=id_entry.get()
        name=name_entry.get()
        role=role_entry.get()
        gender=variable1.get()
        status=status_entry.get()
        date_of_birth=date_of_birth_entry.get()
        if not(id and name and role and gender and status and date_of_birth):
            messagebox.showerror('Error','Butun bosluklari doldurun!')
        elif not (id.isdigit() and len(id) == 5):
            messagebox.showerror('Error', 'ID 5 basamakli bir tam sayi olmalidir!')    
        elif main.id_exists(id):
            messagebox.showerror('Error','Bu kimlikte birisi var!')
        else:
            main.insert_employee(id,name,role,gender,status,date_of_birth)
            add_to_treeview()
            messagebox.showinfo('Okey','Veri basariyla eklendi!')


    def clear(*clicked):
        if clicked:
            tree.selection_remove(tree.focus())
        id_entry.delete(0,END)
        name_entry.delete(0,END)
        role_entry.delete(0,END)
        variable1.set('Male')
        status_entry.delete(0,END)
        date_of_birth_entry.delete(0,END)

    def display_data(event):
        selected_item=tree.focus()
        if selected_item:
            row=tree.item(selected_item)['values']
            clear()
            id_entry.insert(0,row[0])
            name_entry.insert(0,row[1])
            role_entry.insert(0,row[2])
            variable1.set(row[3])
            status_entry.insert(0,row[4])
            date_of_birth_entry.insert(0,row[5])
        else:
            pass
    
    def update():
        selected_item=tree.focus()
        if not selected_item:
            messagebox.showerror('Error','Güncellemek istedigini sec!')
        else:
            id=id_entry.get()
            name=name_entry.get()
            role=role_entry.get()
            gender=variable1.get()
            status=status_entry.get()
            date_of_birth=date_of_birth_entry.get()
            main.update_employee(name,role,gender,status,date_of_birth,id)
            add_to_treeview()
            clear()
            messagebox.showinfo('Okey','Veri guncellendi!')

    def delete():
        selected_item=tree.focus()
        if not selected_item:
            messagebox.showerror('Error','Silmek istedigini sec!')
        else:
            id=id_entry.get()
            main.delete_employee(id)
            add_to_treeview()
            clear()
            messagebox.showinfo('Okey','Veri basariyla silindi!')


    id_label=customtkinter.CTkLabel(app,font=font1,text="ID: ",text_color="#ff0000",bg_color="#091030")
    id_label.place(x=20,y=20)

    id_entry=customtkinter.CTkEntry(app,font=font1,text_color="#000000",border_width=2,border_color="#000000",width=180)
    id_entry.place(x=100,y=20)

    name_label = customtkinter.CTkLabel(app, font=font2, text="NAME: ", text_color="#ff0000", bg_color="#091030")
    name_label.place(x=20, y=60)

    name_entry=customtkinter.CTkEntry(app,font=font1,text_color="#000000",border_width=2,border_color="#000000",width=195)
    name_entry.place(x=100,y=60)

    role_label = customtkinter.CTkLabel(app, font=font2, text="ROLE: ", text_color="#ff0000", bg_color="#091030")
    role_label.place(x=20, y=100)

    role_entry = customtkinter.CTkEntry(app,font=font1,text_color="#000000",border_width=2,border_color="#000000",width=180)
    role_entry.place(x=100, y=100)

    gender_label = customtkinter.CTkLabel(app, font=font2, text="GENDER: ", text_color="#ff0000", bg_color="#091030")
    gender_label.place(x=20, y=140)

    options=['Male','Female']
    variable1=StringVar()
    
    gender_options= customtkinter.CTkComboBox(app,font=font2,text_color="#071208",variable=variable1,width=180,values=options,state="readonly")
    gender_options.set('Male')
    gender_options.place(x=100,y=140)

    status_label=customtkinter.CTkLabel(app,font=font2,text="STATUS: ", text_color="#ff0000",bg_color="#091030")
    status_label.place(x=20 ,y=180 )

    status_entry=customtkinter.CTkEntry(app,font=font2,text_color="#000000",border_color="#000000",border_width=2,width=180)
    status_entry.place(x=100 , y= 180)

    date_of_birth_label=customtkinter.CTkLabel(app,font=font2,text="DateOfBirth: ",text_color="#ff0000",bg_color="#091030")
    date_of_birth_label.place(x=20,y=220)

    date_of_birth_entry=customtkinter.CTkEntry(app,font=font2,text_color="#000000",border_color="#000000",border_width=2,width=170)
    date_of_birth_entry.place(x=115,y=220)

    add_button=customtkinter.CTkButton(app,command=insert,text="ADD EMPLOYEE",font=font2,fg_color="#20e312",hover_color="#0505f2",cursor="hand2",width=260)
    add_button.place(x=20,y=340)

    clear_button=customtkinter.CTkButton(app,command=lambda:clear(True),text="NEW EMPLOYEE",font=font2,fg_color="#adadad",hover_color="#0505f2",cursor="hand2",width=260)
    clear_button.place(x=400,y=380)

    del_button=customtkinter.CTkButton(app,command=delete,text="DELETE EMPLOYEE",font=font2,fg_color="#f20505",hover_color="#0505f2",cursor="hand2",width=260)
    del_button.place(x=20,y=380)

    updt_button=customtkinter.CTkButton(app,command=update,text="UPDATE EMPLOYEE",font=font2,fg_color="#adadad",hover_color="#0505f2",cursor="hand2",width=260)
    updt_button.place(x=800,y=380)
    
    search_button=customtkinter.CTkButton(app,command=search_info,text="SEARCH EMPLOYEE",font=font2,fg_color="#0400ff",hover_color="#ffffff",cursor="hand2",width=260)
    search_button.place(x=20,y=300)

    style=ttk.Style(app)
    style.theme_use('clam')
    style.configure('Treeview',font=font2,foreground='#ff0000',background='#4aeaf0',fieldbackground='#515157')
    style.map('Treeview',background=[('selected','1A8FD2')])
    tree=ttk.Treeview(app,height=16)
    tree['columns'] =('ID','NAME','ROLE','GENDER','STATUS','DATE_OF_BIRTH')
    tree.column('#0',width=0,stretch=tk.NO)
    tree.column('ID',anchor=tk.CENTER,width=140)
    tree.column('NAME',anchor=tk.CENTER,width=140)
    tree.column('ROLE',anchor=tk.CENTER,width=140)
    tree.column('GENDER',anchor=tk.CENTER,width=140)
    tree.column('STATUS',anchor=tk.CENTER,width=140)
    tree.column('DATE_OF_BIRTH',anchor=tk.CENTER,width=140)
    tree.heading('ID',text='ID')
    tree.heading('NAME',text='NAME')
    tree.heading('ROLE',text='ROLE')
    tree.heading('GENDER',text='GENDER')
    tree.heading('STATUS',text='STATUS')
    tree.heading('DATE_OF_BIRTH',text='DATE_OF_BIRTH')
    tree.place(x=315,y=20)

    tree.bind('<ButtonRelease>',display_data)
    add_to_treeview()

    app.mainloop()


if __name__ == "__main__":
    create_window()
