import re
import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk

import customtkinter
import matplotlib.pyplot as plt

import database

app=customtkinter.CTk()
app.title('Employee Management System')
app.geometry("940x450+0+0")
app.config(bg="#161C25")
app.resizable(False, False)
label=Label(app, text="EMPLOYEE MANAGEMENT SYSTEM", font=("TImes new Roman", 31, "bold"), fg='#DCE8FA', bg='#161C25')
label.place(x=0, y=0, width=1530, height=50)
font1=("Arial", 21, "bold")
font2=("calibri", 14 ,"bold")

#Functions

def validate_name(name):
    return re.match("^[A-Za-z\s]+$", name)

def addToTree():
    employees=database.fetch_employees()
    tree.delete(*tree.get_children())
    for employee in employees:
        tree.insert('', END, values=employee)
    
           
def display_data(event):
     selected_item=tree.focus()
     if selected_item:
         row=tree.item(selected_item)['values']
         clear()
         id_entry.insert(0, row[0])
         name_entry.insert(0, row[1])
         variable2.set(row[2])
         variable3.set(row[3])
         variable1.set(row[4])
     else:
         pass
        
def update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "Select an employee to Update")
    else:
        id = id_entry.get()
        name = name_entry.get().strip()
        department = variable2.get()
        role = variable3.get()
        gender = variable1.get()
        if not (id and name and department and role and gender):
            messagebox.showerror("Error", "All fields required")
        elif not validate_name(name):
            messagebox.showerror("Error", "Enter Correct Name!")
        else:
            database.update_employees(name, department, role, gender, id)
            addToTree()
            clear()
            messagebox.showinfo("Successful", "Employee Updated")
            show_graph()

def delete():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror("Error", "Select an employee to Delete!")
    else:
        id = id_entry.get()
        if not (id):
            messagebox.showerror("Error", "Select an Employee to be Deleted")
        else:
            database.delete_employees(id)
            addToTree()
            clear()
            messagebox.showinfo("Successful", "Employee Deleted Successfully")
            show_graph()           
   


def clear(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
    id_entry.delete(0, END)
    name_entry.delete(0, END)
    variable1.set("Select Gender")
    variable2.set("Select Department")
    variable3.set("Select Role")
    
    
def insert():
    id = id_entry.get()
    name = name_entry.get().strip()
    department = variable2.get()
    role = variable3.get()
    gender = variable1.get()
    
    if not (id and name and department and role and gender):
        messagebox.showerror("Error", "All fields required")
    elif not validate_name(name):
        messagebox.showerror("Error", "Oops! Name should only contain alphabets only")
    elif database.id_exists(id):
        messagebox.showerror("Error", "ID already exists")
    elif department == "Select Department" or role == "Select Role" or gender == "Select Gender":
        messagebox.showerror("Error", "Please select all fields")
    else:
        database.insert_employees(id, name, department, role, gender)
        addToTree()
        messagebox.showinfo("Successful", "Employee Added")
        show_graph()

def show_graph():
    employees = database.fetch_employees()
    department_count = {}
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    for employee in employees:
        department = employee[2]
        if department in department_count:
            department_count[department] += 1
        else:
            department_count[department] = 1
    
    # Plotting the graph for department
    plt.figure(figsize=(10, 6))
    plt.bar(department_count.keys(), department_count.values(), color=colors[:len(department_count)])
    plt.xlabel('Department', fontsize=14)
    plt.ylabel('Number of Employees', fontsize=14)
    plt.title('Employee Distribution by Department', fontsize=16)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


def role_graph():
    employees = database.fetch_employees()
    role_count = {}
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    for employee in employees:
        role = employee[3]
        if role in role_count:
            role_count[role] += 1
        else:
            role_count[role] = 1
    
    # Plotting the pie chart for role
    plt.figure(figsize=(8, 8))
    plt.pie(role_count.values(), labels=role_count.keys(), colors=colors[:len(role_count)], autopct='%1.1f%%', startangle=140)
    plt.title('Employee Distribution by Role')
    plt.axis('equal')
    plt.show()
    
def gender_graph():
    employees = database.fetch_employees()
    gender_count = {}
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    for employee in employees:
        gender = employee[4]
        if gender in gender_count:
            gender_count[gender] += 1
        else:
            gender_count[gender] = 1
    
    # Plotting the graph for gender
    plt.figure(figsize=(10, 6))
    plt.bar(gender_count.keys(), gender_count.values(), color=colors[:len(gender_count)])
    plt.xlabel('Gender', fontsize=14)
    plt.ylabel('Number of Employees', fontsize=14)
    plt.title('Employee Distribution by Gender', fontsize=16)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    
id_label=customtkinter.CTkLabel(app,font=font1, text="ID: ",text_color="white", bg_color="#161C25" )
id_label.place(x=20, y=20)
id_entry=customtkinter.CTkEntry(app, font=("saogi UI", 25, "bold"),text_color="#000",  fg_color="#fff", border_color="#0C9295", border_width=2, width=180)
id_entry.place(x=100,y=20)

name_label=customtkinter.CTkLabel(app,font=font1, text="Name: ",text_color="white", bg_color="#161C25" )
name_label.place(x=20, y=80)
name_entry = customtkinter.CTkEntry(app, font=("saogi UI", 25, "bold"), text_color="#000", fg_color="#fff", 
                                    border_color="#0C9295", border_width=2, width=180, validate="key", 
                                    validatecommand=(app.register(validate_name), '%P'))
name_entry.place(x=100,y=80)


department_label=customtkinter.CTkLabel(app,font=font1, text="Dept: ",text_color="white", bg_color="#161C25")
department_label.place(x=20, y=140)

options2= ['Software','Accounts & Finance', 'HR', 'Purchase & Sales', 'Marketing', 'Production & Logistics']
variable2=StringVar()
dept_options = customtkinter.CTkComboBox(app,width=250,height=20,  font=font1, dropdown_text_color=("#343029"), dropdown_hover_color="#11A700", dropdown_fg_color="#FFFFFF",
                                           text_color="#171827",  fg_color="#D9E4F5", border_color="black",
                                           variable=variable2, values=options2, state='readonly')
dept_options.place(x=100, y=140)


role_label=customtkinter.CTkLabel(app,font=font1, text="Role: ",text_color="white", bg_color="#161C25" )
role_label.place(x=20, y=200)
options3= ['Manager','Team Lead','Head of Dept', 'Officer', 'Owner','Director', 'Clerk', 'Developer', 'Consultant']
variable3=StringVar()
role_options = customtkinter.CTkComboBox(app, width=250,height=20, font=font1, dropdown_text_color=("#343029"), dropdown_hover_color="#11A700", dropdown_fg_color="#FFFFFF",
                                           text_color="#171827",  fg_color="#D9E4F5", border_color="black",
                                           variable=variable3, values=options3, state='readonly')
role_options.place(x=100, y=200)

gender_label=customtkinter.CTkLabel(app,font=font1, text="Gender: ",text_color="white", bg_color="#161C25" )
gender_label.place(x=20, y=260)
options= ['Male', 'Female', 'others']
variable1=StringVar()

gender_options = customtkinter.CTkComboBox(app, width=250,font=font1, dropdown_text_color=("#343029"), dropdown_hover_color="#11A700", dropdown_fg_color="#FFFFFF",
                                           text_color="#171827",  fg_color="#D9E4F5", border_color="black",
                                           variable=variable1, values=options, state='readonly')
gender_options.place(x=100, y=260)


#Buttons
addBtn = customtkinter.CTkButton(app, command=insert,font=font1,text="Add Employee", text_color="#fff", 
                                    fg_color="#161C25", hover_color="#00FF15", bg_color="#161C25",border_color="#F15704",
                                    cursor='hand2',border_width=2, width=260)
addBtn.place(x=20, y=310)

clearBtn = customtkinter.CTkButton(app, command=lambda:clear(True),font=font1 ,text_color="#fff", text="Clear", 
                                   fg_color="#161C25", bg_color="#161C25", hover_color="#FF5002", border_color="#F15704", 
                                   cursor='hand2',border_width=2, width=260)
clearBtn.place(x=20, y=400)

updateBtn = customtkinter.CTkButton(app, command=update ,font=font1,text="Update", text_color="#fff", 
                                    fg_color="#161C25", hover_color="#00850B", bg_color="#161C25",border_color="#F15704",
                                    cursor='hand2',border_width=2, width=260)
updateBtn.place(x=300, y=400)

deleteBtn = customtkinter.CTkButton(app, command=delete,font=font1,text="Delete", text_color="#fff", 
                                    fg_color="#161C25", hover_color="#FF0000", bg_color="#161C25",border_color="#F15704",
                                    cursor='hand2',border_width=2, width=260)
deleteBtn.place(x=580, y=400)

graph1 = customtkinter.CTkButton(app, command=show_graph, font=font1, text="By Department", text_color="skyblue", 
                                    fg_color="#161C25", hover_color="black", bg_color="#161C25",border_color="white",
                                    cursor='hand2',border_width=2, width=60)
graph1.place(x=380, y=310)
graph2= customtkinter.CTkButton(app, command=role_graph, font=font1, text="By Role", text_color="green", 
                                    fg_color="#161C25", hover_color="black", bg_color="#161C25",border_color="white",
                                    cursor='hand2',border_width=2, width=60)
graph2.place(x=550, y=310)
graph3= customtkinter.CTkButton(app, command=gender_graph, font=font1, text="By Gender", text_color="red", 
                                    fg_color="#161C25", hover_color="black", bg_color="#161C25",border_color="white",
                                    cursor='hand2',border_width=2, width=60)
graph3.place(x=660, y=310)

graph_label = customtkinter.CTkLabel(app, font=("Arial", 21, "bold"), text="GRAPHICAL PRESENTATION", text_color="yellow", bg_color="#161C25")
graph_label.place(x=460, y=350)

style= ttk.Style(app)
style.theme_use('clam')
style.configure('Treeview', font=font2, foreground='#fff',background='#000', fieldbackground="#313837")
style.map('Treeview', background=[('selected', '#1A8F2D')])

tree=ttk.Treeview(app, height=15)

tree['columns']=('Id', 'Name','Department', 'Role', 'Gender')
tree.column('#0', width=0, stretch=tk.NO)
tree.column("Id", anchor=tk.CENTER, width=120)
tree.column("Name", anchor=tk.CENTER, width=120)
tree.column("Department", anchor=tk.CENTER, width=120)
tree.column("Role", anchor=tk.CENTER, width=120)
tree.column("Gender", anchor=tk.CENTER, width=120)

tree.heading('Id', text='ID')
tree.heading('Name', text='NAME')
tree.heading('Department', text='DEPARTMENT')
tree.heading('Role', text='Role')
tree.heading('Gender', text='GENDER')

tree.place(x=480, y=55)

addToTree()
tree.bind('<ButtonRelease>', display_data)

app.mainloop()
