import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Function to connect to the MySQL database
def connect_to_db():
    global db
    db = mysql.connector.connect(
        host="0.0.0.0",
        user="root",
        password="enter password",
        database="database_name"
    )

# Function to add a new record to the database
def add_record():
    cursor = db.cursor()
    data = (entry_name.get(), entry_age.get())
    cursor.execute("INSERT INTO table_name (name, age) VALUES (%s, %s)", data)
    db.commit()
    cursor.close()
    messagebox.showinfo("Info", "Record added successfully")
    view_records()

def view_records():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM table_name")
    records = cursor.fetchall()
    for record in treeview.get_children():
        treeview.delete(record)
    
    # Get column names from the cursor description
    column_names = [desc[0] for desc in cursor.description]

    # Configure Treeview based on the extracted column names
    treeview["columns"] = column_names
    for col_name in column_names:
        treeview.heading(col_name, text=col_name)
        treeview.column(col_name, width=100)  # Adjust the width as needed
    
    for record in records:
        treeview.insert("", "end", values=record)
    cursor.close()

# Create the GUI
root = Tk()
root.title("Database GUI")

# Labels Fields
label_subject = Label(root, text="Subject")
label_course = Label(root, text="Course")
label_crn = Label(root, text="CRN")

# Entry Fields
entry_subject = Entry(root)
entry_course = Entry(root)
entry_crn = Entry(root)

# Buttons
button_add = Button(root, text="Add Record", command=add_record)
button_view = Button(root, text="View Records", command=view_records)

# Grid layout for labels (top left)
label_subject.grid(row=0, column=0, sticky="w")
label_course.grid(row=1, column=0, sticky="w")
label_crn.grid(row=2, column=0, sticky="w")

# Entries (top left)
entry_subject.grid(row=0, column=1, sticky="w")
entry_course.grid(row=1, column=1, sticky="w")
entry_crn.grid(row=2, column=1, sticky="w")

# Buttons (bottom left)
button_add.grid(row=3, column=0, sticky="w")
button_view.grid(row=3, column=1, sticky="w")

# Treeview (bottom right)
treeview = ttk.Treeview(root, columns=("Subject", "Course", "CRN"), show="headings")
treeview.heading("Subject", text="Subject")
treeview.heading("Course", text="Course")
treeview.heading("CRN", text="CRN")
treeview.grid(row=4, column=0, columnspan=2, sticky="nsew")

# Configure column and row weights to make the table and columns expand with the window
root.columnconfigure(1, weight=1)
root.rowconfigure(4, weight=1)

# Connection to DB
connect_to_db()
root.mainloop()