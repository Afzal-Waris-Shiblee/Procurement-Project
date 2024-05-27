from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import sqlite3
import pandas as pd

# Connect to the SQLite database
connection = sqlite3.connect('Procurement.db')
cursor = connection.cursor()

#-------------------------Table Creation Section----------------------------------------------------
# Create the 'supplier' table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS supplier(
        supplier_code INTEGER PRIMARY KEY AUTOINCREMENT,
        supplier_name VARCHAR(70),
        contact_person VARCHAR(50),  
        address VARCHAR(100),
        tel_no VARCHAR(10),
        email VARCHAR(30),
        payment_term VARCHAR CHECK (payment_term IN ('15 Days','30 Days','60 Days','Advance','Cash Payment'))
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS supplier_p(
        supplier_code INTEGER PRIMARY KEY AUTOINCREMENT,
        supplier_name VARCHAR(70),
        contact_person VARCHAR(50),  
        address VARCHAR(100),
        tel_no VARCHAR(10),
        email VARCHAR(30),
        type VARCHAR CHECK (type IN ('Containers','Cartons','Stickers','Others')),
        payment_term VARCHAR CHECK (payment_term IN ('15 Days','30 Days','60 Days','Advance','Cash Payment'))
    )
''')

# Create the 'Item' table for raw material
cursor.execute('''
    CREATE TABLE IF NOT EXISTS item (
        item_code INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name VARCHAR(60),
        category VARCHAR CHECK (category IN ('RM')),
        item_type VARCHAR CONSTRAINT check_item_type CHECK(item_type IN ('RM Local','RM Import'))
   
                 )
''')

# Create the 'Item' table for raw material
cursor.execute('''
    CREATE TABLE IF NOT EXISTS item_p (
        item_code INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name VARCHAR(60),
        category VARCHAR CHECK (category IN ('Master Ctn','Inner Ctn','Stickers','Tin','Bottle','Container','Other')),
        finished_good VARCHAR(60)
   
                 )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS price (
        paf_no TEXT,
        app_date DATE,
        supplier_code TEXT,
        supplier_name TEXT,
        item_code TEXT,
        item_name TEXT,
        Category TEXT CHECK (Category IN ('RM')),
        origin TEXT,
        Current_rate REAL,
        payment_term TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS price_p (
        paf_no TEXT,
        app_date DATE,
        supplier_code TEXT,
        supplier_name TEXT,
        item_code TEXT,
        item_name TEXT,
        Category TEXT CHECK (Category IN ('Master Ctn','Inner Ctn','Stickers','Tin','Bottle','Container','Other')),
        unit TEXT CHECK (unit IN ('Pcs','Kg','Meter','Roll')),
        Current_rate REAL,
        payment_term TEXT
    )
''')

connection.commit()


#-----------------------------Raw Material Supplier Add Records  ------------------------------------------------------
def insert_record():

    connection = sqlite3.connect('Procurement.db')
    cursor = connection.cursor()

    # Root Window for Insert Supplier Record
    root = Tk()
    root.title('My Window')
    root.geometry('800x600+300+50')
    root.configure(bg='#CD5C5C')
    mainhead = Label(root, text="PERIDOT PRODUCTS PVT LTD", font=("Arial", 20), bg='black', fg='white')
    mainhead.place(x=150, y=20)
    subhead = Label(root, text="SUPPLIER INSERT RECORD", font=("Arial", 15), bg='black',fg='white')
    subhead.place(x=225, y=80)

    #Label and Enteries for supplier Records

    l1 = Label(root, text='Enter Supplier Name', font=("Arial", 12), fg='black', bg='#CD5C5C')
    l1.place(x=120, y=150, anchor=W)
    supplier_name_entry = Entry(root)
    supplier_name_entry.place(x=380, y=140, width=200, height=20)

    l2 = Label(root, text='Contact Person', font=("Arial", 12), fg='black', bg='#CD5C5C')
    l2.place(x=120, y=175, anchor=W)
    contact_person_entry = Entry(root)
    contact_person_entry.place(x=380, y=165, width=200, height=20)


    l3 = Label(root, text='Address', font=("Arial", 12), fg='black', bg='#CD5C5C')
    l3.place(x=120, y=200, anchor=W)
    address_entry = Entry(root)
    address_entry.place(x=380, y=190, width=300, height=20)

    l5 = Label(root, text='Enter Tel No.', font=("Arial", 12), fg='black', bg='#CD5C5C')
    l5.place(x=120, y=250, anchor=W)
    tel_entry = Entry(root)
    tel_entry.place(x=380, y=240, width=200, height=20)

    l6 = Label(root, text='Enter Email Address.', font=("Arial", 12), fg='black', bg='#CD5C5C')
    l6.place(x=120, y=275, anchor=W)
    email_entry = Entry(root)
    email_entry.place(x=380, y=265, width=200, height=20)

    l7 = Label(root, text='Enter Payment Term', font=("Arial", 12), fg='black', bg='#CD5C5C')
    l7.place(x=120, y=300, anchor=W)
    payterm_combobox = ttk.Combobox(root, values=['15 Days', '30 Days', '60 Days', 'Advance', 'Cash Payment'])
    payterm_combobox.place(x=380, y=290, width=200, height=20)

    # Getting values of Insert supplier record

    def supp_insert_record():
        enter_supplier_name = supplier_name_entry.get()
        enter_contact_person = contact_person_entry.get()
        enter_address = address_entry.get()
        enter_tel_no = tel_entry.get()
        enter_email = email_entry.get()
        enter_payment_term = payterm_combobox.get()

    # Supplier Data Insert in Sqlite Database
        #try:
        cursor.execute("INSERT INTO supplier (supplier_name,contact_person,address,tel_no,email,payment_term) VALUES (?,?,?,?,?,?)",
                           (enter_supplier_name, enter_contact_person,enter_address, enter_tel_no, enter_email, enter_payment_term))
        connection.commit()
        status_label.config(text='Record Sucessfully Inserted')    
            #messagebox.showinfo("Success", "Record inserted successfully.")
        #except sqlite3.IntegrityError:
         #   messagebox.showerror("Error", "Supplier with the same name already exists.")

    # Return to Main Menu Funtion
    def return_to_main_menu():
            root.destroy()
            #main_menu()
     
    # Insert Record Button
    insert_button = Button(root, text="Insert Record", command=supp_insert_record)
    insert_button.place(x=250, y=350)

    status_label = Label(root, text="",bg="#CD5C5C")
    status_label.place(x=250,y=450)

    return_button = Button(root, text="Click Here to return to Main Menu",bg='yellow', command=return_to_main_menu)
    return_button.place(x=250, y=500)

    root.mainloop()

    #-------------------------------------------Packing Material Supplier Add Records-------------------------------------------------------

def insert_record_p():

    connection = sqlite3.connect('Procurement.db')
    cursor = connection.cursor()

    # Root Window for Insert Supplier Record
    root = Tk()
    root.title('My Window')
    root.geometry('800x600+300+50')
    root.configure(bg='#CD5C5C')
    mainhead = Label(root, text="PERIDOT PRODUCTS PVT LTD", font=("Arial", 20), bg='black', fg='white')
    mainhead.place(x=150, y=20)
    subhead = Label(root, text="PACKING MATERIAL SUPPLIER INSERT RECORD", font=("Arial", 15), bg='black',fg='white')
    subhead.place(x=225, y=80)

        #Label and Enteries for supplier Records

    l1 = Label(root, text='Enter Supplier Name', font=("Arial", 12), fg='black', bg='#CD5C5C')
    l1.place(x=120, y=150, anchor=W)
    supplier_name_entry = Entry(root)
    supplier_name_entry.place(x=380, y=140, width=200, height=20)

    l2 = Label(root, text='Contact Person', font=("Arial", 12), fg='black', bg='#CD5C5C')
    l2.place(x=120, y=175, anchor=W)
    contact_person_entry = Entry(root)
    contact_person_entry.place(x=380, y=165, width=200, height=20)


    l3 = Label(root, text='Address', font=("Arial", 12), fg='black', bg='#CD5C5C')
    l3.place(x=120, y=200, anchor=W)
    address_entry = Entry(root)
    address_entry.place(x=380, y=190, width=300, height=20)

    l5 = Label(root, text='Enter Tel No.', font=("Arial", 12), fg='black', bg='#CD5C5C')
    l5.place(x=120, y=250, anchor=W)
    tel_entry = Entry(root)
    tel_entry.place(x=380, y=240, width=200, height=20)

    l6 = Label(root, text='Enter Email Address.', font=("Arial", 12), fg='black', bg='#CD5C5C')
    l6.place(x=120, y=275, anchor=W)
    email_entry = Entry(root)
    email_entry.place(x=380, y=265, width=200, height=20)

    l6 = Label(root, text='Enter Supplier Type', font=("Arial", 12), fg='black', bg='#CD5C5C')
    l6.place(x=120, y=300, anchor=W)
    type_comobox = ttk.Combobox  (root, values=['Containers','Cartons','Stickers','Others'])
    type_comobox.place(x=380, y=290, width=200, height=20)

    l7 = Label(root, text='Enter Payment Term', font=("Arial", 12), fg='black', bg='#CD5C5C')
    l7.place(x=120, y=325, anchor=W)
    payterm_combobox = ttk.Combobox(root, values=['15 Days', '30 Days', '60 Days', 'Advance', 'Cash Payment'])
    payterm_combobox.place(x=380, y=315, width=200, height=20)

    # Getting values of Insert supplier record

    def supplier_insert_record_p():
        enter_supplier_name = supplier_name_entry.get()
        enter_contact_person = contact_person_entry.get()
        enter_address = address_entry.get()
        enter_tel_no = tel_entry.get()
        enter_email = email_entry.get()
        enter_type = type_comobox.get()
        enter_payment_term = payterm_combobox.get()

    #   Supplier Data Insert in Sqlite Database
        #try:
        cursor.execute("INSERT INTO supplier_p (supplier_name,contact_person,address,tel_no,email,type,payment_term) VALUES (?,?,?,?,?,?,?)",
                           (enter_supplier_name, enter_contact_person,enter_address, enter_tel_no, enter_email, enter_type,enter_payment_term))
        connection.commit()
        status_label.config(text='Record Sucessfully Inserted')    
            #messagebox.showinfo("Success", "Record inserted successfully.")
        #except sqlite3.IntegrityError:
         #   messagebox.showerror("Error", "Supplier with the same name already exists.")

    # Return to Main Menu Funtion
    def return_to_main_menu():
            root.destroy()
            #main_menu()
     
    # Insert Record Button
    
    insert_button = Button(root, text="Insert Record", command=supplier_insert_record_p)
    insert_button.place(x=250, y=350)

    status_label = Label(root, text="",bg="#CD5C5C")
    status_label.place(x=250,y=450)

    return_button = Button(root, text="Click Here to return to Main Menu",bg='yellow', command=return_to_main_menu)
    return_button.place(x=250, y=500)

    root.mainloop()


#------------------------------  Display Supplier Records--------------------------------------------
def display_suppliers():
    connection = sqlite3.connect('Procurement.db')
    cursor = connection.cursor()


    # Fetch all records from the 'supplier' table
    cursor.execute("SELECT * FROM supplier")
    records = cursor.fetchall()

    # Create a new window for displaying records
    root = Tk()
    root.title('My Window')
    root.geometry('3000x2000')
    root.title ('Supplier Records')
    root.configure(background='red')      
 
    # Heading of Supplier Record Report
    l1=Label(root,text='Supplier Code',font=("Areal",10),fg='Black',bg='red')
    l1.place(x=10,y=20,anchor=W)
    l2=Label(root,text='Supplier Name',font=("Areal",10),fg='black',bg='red')
    l2.place(x=150,y=20,anchor=W)
    l3=Label(root,text='Contact Person',font=("Areal",10),fg='black',bg='red')
    l3.place(x=400,y=20,anchor=W)
    l3=Label(root,text='Address',font=("Areal",10),fg='black',bg='red')
    l3.place(x=600,y=20,anchor=W)
    l3=Label(root,text='Tel No',font=("Areal",10),fg='black',bg='red')
    l3.place(x=900,y=20,anchor=W)
    l3=Label(root,text='Email',font=("Areal",10),fg='black',bg='red')
    l3.place(x=1050,y=20,anchor=W)
    l3=Label(root,text='Payment Term',font=("Areal",10),fg='black',bg='red')
    l3.place(x=1150,y=20,anchor=W)

    # Loop for display all data of suppliers
    n=40
    for record in records:

        l3=Label(root,text=record[0],font=("Areal",10),fg='white',bg='red')
        l3.place(x=20,y=n)
        l3=Label(root,text=record[1],font=("Areal",10),fg='white',bg='red')
        l3.place(x=150,y=n,anchor=W)
        l3=Label(root,text=record[2],font=("Areal",10),fg='white',bg='red')
        l3.place(x=400,y=n,anchor=W)
        l3=Label(root,text=record[3],font=("Areal",10),fg='white',bg='red')
        l3.place(x=550,y=n,anchor=W)
        l3=Label(root,text=record[4],font=("Areal",10),fg='white',bg='red')
        l3.place(x=900,y=n,anchor=W)
        l3=Label(root,text=record[5],font=("Areal",10),fg='white',bg='red')
        l3.place(x=1050,y=n,anchor=W)
        l3=Label(root,text=record[6],font=("Areal",10),fg='white',bg='red')
        l3.place(x=1150,y=n,anchor=W)
        #l3=Label(root,text=record[7],font=("Areal",10),fg='white',bg='red')
        #l3.place(x=1150,y=n,anchor=W)
        n=n+30

       

                
    # If no records are found
    if not records:
        no_records_label = Label(root, text="No records found.")
        no_records_label.pack()

    return_button = tk.Button(root, text="Click to return Main Menu",bg='yellow', command=lambda: return_to_main_menu(root))
    return_button.place(x=400,y=n)

def return_to_main_menu(root):
        root.destroy()

connection.close()
#------------------------------------------Raw Material Supplier Record display with Treeview-------------------------------------------------
def display_suppliers_2():
    connection = sqlite3.connect('Procurement.db')
    cursor = connection.cursor()
    

    # Query to fetch data without supplier address
    #cursor.execute('SELECT supplier_code, supplier_name, contact_person, tel_no, email, payment_term FROM supplier')

    cursor.execute('SELECT * FROM supplier ORDER BY supplier_name')
    #cursor.execute('SELECT * FROM supplier')
    query=cursor.fetchall()

  
    
    root = tk.Tk()
    root.title("Supplier DISPLAY AREA")
    root.geometry('1400x750+1+50')
    root.configure(background='#CD5C5C')
    # Create a Treeview widget
    style = ttk.Style()

    # Configure the Treeview style
    style.configure("Treeview",
                background="#CD5C5C",  # Background color for cells
                fieldbackground="#DE3163",  # Field background color for cells
                foreground="white",  # Foreground color for text
                borderwidth=1,
                relief="solid"
                
                )

    # Configure the heading style
    style.configure("Treeview.Heading",
                background="#CD5C5C",  # Background color for headings
                foreground="black",  # Foreground color for heading text
                borderwidth=1,
                relief="solid"
                )

    tree = ttk.Treeview(root, style="Treeview")
    tree["columns"] = ["supplier_code", "supplier_name", "contact_person","address", "tel_no","email","payment_term"]
    tree["show"] = "headings"
    tree.heading("supplier_code", text="Supplier Code")
    tree.heading("supplier_name", text="Supplier Name")
    tree.heading("contact_person", text="Contact Person")
    tree.heading("address", text="Supplier Address")
    tree.heading("tel_no", text="Tel No.")
    tree.heading("email", text="Email")
    tree.heading("payment_term", text="Payment Term")

    tree.column('supplier_code', anchor='center',width=50)
    tree.column('supplier_name', anchor='w',width=200)
    tree.column('contact_person', anchor='w',width=100)
    tree.column('address', anchor='w',width=500)
    tree.column('tel_no', anchor='center',width=100)
    tree.column('email', anchor='w',width=150)
    tree.column('payment_term', anchor='center',width=100)
    
    # Define colors for alternate rows
    colors = ['#DE3163', '#CD5C5C']

    # Insert data into the Treeview and apply background colors
    for i, row in enumerate(query):
        color = colors[i % 2]  # Alternate colors
        tree.insert("", "end", values=row, tags=('colored',))
        tree.tag_configure('colored', background=color)
        tree.tag_configure('colored', foreground='white')

     # Pack the Treeview widget and increase the height
    tree.pack(expand=True, fill=tk.BOTH)

    #for row in query:
     #   tree.insert("", "end", values=row)


# Pack the Treeview widget
    tree.pack()

    return_button = tk.Button(root, text="Click to return Main Menu",bg='yellow',command=lambda: return_to_main_menu(root))
    return_button.pack(pady=50)

def return_to_main_menu(root):
        root.destroy()

#---------------------------------------------Packing Material Supplier Display Records ------------------------------------------------

def display_suppliers_p():
    connection = sqlite3.connect('Procurement.db')
    cursor = connection.cursor()
    

    # Query to fetch data without supplier address
    #cursor.execute('SELECT supplier_code, supplier_name, contact_person, tel_no, email, payment_term FROM supplier')

    cursor.execute('SELECT * FROM supplier_p ORDER BY supplier_name')
    #cursor.execute('SELECT * FROM supplier')
    query=cursor.fetchall()

  
    
    root = tk.Tk()
    root.title("Supplier DISPLAY AREA")
    root.geometry('1400x750+1+50')
    root.configure(background='#008080')
    # Create a Treeview widget
    

    style = ttk.Style(root)
    style.theme_use("clam")  # Use 'clam' theme
    style.configure("Treeview",

                    background="#008080",

                    foreground="white"  # Foreground color
    
                    
                    )
    
    tree = ttk.Treeview(root, style="Treeview", height= 30)  # Adjust the height as needed


    
    tree = ttk.Treeview(root, style="Treeview")
    tree["columns"] = ["supplier_code", "supplier_name", "contact_person","address", "tel_no","email","type","payment_term"]
    tree["show"] = "headings"
    tree.heading("supplier_code", text="Supplier Code")
    tree.heading("supplier_name", text="Supplier Name")
    tree.heading("contact_person", text="Contact Person")
    tree.heading("address", text="Supplier Address")
    tree.heading("tel_no", text="Tel No.")
    tree.heading("email", text="Email")
    tree.heading("type", text="Type")
    tree.heading("payment_term", text="Payment Term")

    tree.column('supplier_code', anchor='center',width=50)
    tree.column('supplier_name', anchor='w',width=200)
    tree.column('contact_person', anchor='w',width=100)
    tree.column('address', anchor='w',width=500)
    tree.column('tel_no', anchor='center',width=100)
    tree.column('email', anchor='w',width=150)
    tree.column('type', anchor='w',width=75)
    tree.column('payment_term', anchor='center',width=100)


    
    tree['height'] = 30

    # Insert data into the Treeview and apply background colors

    for index, row in enumerate(query): 
        tree.insert("", "end", values=row)  # Insert the entire tuple directly
          
            
        tree.pack()
    

    return_button = tk.Button(root, text="Click to return Main Menu",bg='yellow',command=lambda: return_to_main_menu(root))
    return_button.pack(pady=50)

def return_to_main_menu(root):
        root.destroy()

#-------------------------------------Raw Suppliers Delete Record --------------------------------------------------------------------
def delete_window():
    # Root window for Delete Record for suppliers
    root=Tk()
    root.title('Supplier Deletion Record')
    root.geometry("600x600+400+50")
    root.configure(bg="#CD5C5C")

    # Input supplier code for deletion
    linpt = Label(root, text='Enter Supplier Code for Delete', bg="#CD5C5C", fg='white', font=("Arial", 12))
    linpt.place(x=200, y=50)
    entry_supplier_code = Entry(root, width=10)
    entry_supplier_code.place(x=280, y=100)
    btn_show_detail = Button(root, text='Supplier Detail', command=lambda: show_supplier_detail())
    btn_show_detail.place(x=200, y=200)

    def show_supplier_detail():
        supplier_code = entry_supplier_code.get()

        connection = sqlite3.connect('Procurement.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM supplier WHERE supplier_code = ?', (supplier_code,))
        existing_item = cursor.fetchone()

        if existing_item:
            detail_supplier_window = Toplevel(root)
            detail_supplier_window.title(" Supplier Detail")
            detail_supplier_window.geometry("420x210+450+350")
            detail_supplier_window.configure(bg='black')

            fields = ["Supplier Code", "Supplier Name", "Contact Person","Address",  "Tel No", "Email", "Payment Term"]
            for i, field in enumerate(fields):
                label_price = Label(detail_supplier_window,text=f"{field} : {existing_item[i]}", bg='black',fg='white',anchor=tk.W,padx=10)
                label_price.grid(row=i,column=0,sticky='w')

                confirm_p_button = Button(detail_supplier_window,text='Click to confirm of Deletion',command=lambda: delete_supplier_data())
                confirm_p_button.place(x=190,y=180)

                status_label = Label(root, text='')
                status_label.place(x=100, y=150)
          
            def delete_supplier_data():
                supplier_code = entry_supplier_code.get()

                connection = sqlite3.connect('Procurement.db')
                cursor = connection.cursor()

                cursor.execute('DELETE FROM supplier WHERE supplier_code = ?', (supplier_code,))
                connection.commit()
        
                entry_supplier_code.delete(0, END)

                status_label.config(text='Record Sucessfully Deleted')

    return_button = Button(root, text="Click Here to return to Main Menu",bg='yellow', command=lambda:return_to_main_menu(root))
    #return_button_p2 = Button(root,text= 'Click to Return Main Menu', command=lambda:return_to_main_menu(root))
    return_button.place(x=250,y=540)

def return_to_main_menu(root):
    root.destroy()

#-------------------------------------------Packing Material Supplier Delete Records---------------------------------------------------------

def delete_supplier_p():
    # Root window for Delete Record for suppliers
    root=Tk()
    root.title('Supplier Deletion Record')
    root.geometry("600x600+400+50")
    root.configure(bg="#CD5C5C")

    # Input supplier code for deletion
    linpt = Label(root, text='Enter Supplier Code for Delete', bg="#CD5C5C", fg='white', font=("Arial", 12))
    linpt.place(x=200, y=50)
    entry_supplier_code = Entry(root, width=10)
    entry_supplier_code.place(x=280, y=100)
    btn_show_detail = Button(root, text='Supplier Detail', command=lambda: show_supplier_detail())
    btn_show_detail.place(x=200, y=200)

    def show_supplier_detail():
        supplier_code = entry_supplier_code.get()

        connection = sqlite3.connect('Procurement.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM supplier_p WHERE supplier_code = ?', (supplier_code,))
        existing_item = cursor.fetchone()

        if existing_item:
            detail_supplier_window = Toplevel(root)
            detail_supplier_window.title(" Supplier Detail")
            detail_supplier_window.geometry("500x210+450+350")
            detail_supplier_window.configure(bg='black')

            fields = ["Supplier Code   ", "Supplier Name  ", "Contact Person ","Address              ",  "Telephone No   ", "Email Address   ","Supplier Type    ","Payment Term  "]
            for i, field in enumerate(fields):
                label_heading = Label(detail_supplier_window,text=field, bg='black',fg='white',anchor=tk.W,padx=10)
                label_heading.grid(row=i,column=0,sticky='w')

                label_value = Label(detail_supplier_window,text=f" ------ : {existing_item[i]}", bg='black',fg='red',anchor=tk.W,padx=10)
                label_value.grid(row=i,column=1,sticky='w')

                confirm_p_button = Button(detail_supplier_window,text='Click to confirm of Deletion',command=lambda: delete_supplier_data())
                confirm_p_button.place(x=190,y=180)

                status_label = Label(root, text='')
                status_label.place(x=100, y=150)
          
            def delete_supplier_data():
                supplier_code = entry_supplier_code.get()

                connection = sqlite3.connect('Procurement.db')
                cursor = connection.cursor()

                cursor.execute('DELETE FROM supplier_p WHERE supplier_code = ?', (supplier_code,))
                connection.commit()
        
                entry_supplier_code.delete(0, END)

                status_label.config(text='Record Sucessfully Deleted')

    return_button = Button(root, text="Click Here to return to Main Menu",bg='yellow', command=lambda:return_to_main_menu(root))
    #return_button_p2 = Button(root,text= 'Click to Return Main Menu', command=lambda:return_to_main_menu(root))
    return_button.place(x=250,y=540)

def return_to_main_menu(root):
    root.destroy()

#-------------------------------------Particular RM Supplier Price list--------------------------------------------------------------
def particular_supplier():
    def display_supplier_records(event):
        # Clear the previous records from the treeview
        clear_treeview()

        selected_supplier = item2_combobox.get()

        # Connect to the SQLite database
        conn = sqlite3.connect('Procurement.db')

        # Query to fetch the latest records for the selected supplier
        
        query = """
            
            SELECT paf_no, app_date, supplier_code, item_code, item_name, origin, Current_rate, payment_term
            FROM price
            WHERE supplier_name = ? 
            AND (item_code, paf_no) IN (SELECT item_code, MAX(paf_no) FROM price WHERE supplier_name = ? GROUP BY item_code)
            """

        # Execute the query
        cursor = conn.cursor()
        cursor.execute(query, (selected_supplier, selected_supplier))

        # Fetch all records for the selected supplier
        supplier_records = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Insert records into the treeview
        for record in supplier_records:
            tree.insert("", "end", values=record)

    def clear_treeview():
        # Clear the previous records from the treeview
        for record in tree.get_children():
            tree.delete(record)

    root = tk.Tk()
    root.geometry('1200x600')
    root.title("PARTICULAR SUPPLIER PRICE LIST")
    root.configure(bg="#CD5C5C")

    item_label = tk.Label(root, text="Select Supplier:", bg='black', fg='white', font=('Arial', 12))
    item_label.pack(pady=10)

    # Connect to the SQLite database
    conn = sqlite3.connect('Procurement.db')

    # Query to fetch distinct supplier names from the 'price' table
    query = "SELECT DISTINCT supplier_name FROM price"

    # Execute the query
    cursor = conn.cursor()
    cursor.execute(query)

    # Fetch all the supplier names and store them in supplier_names variable
    supplier_names = sorted([row[0] for row in cursor.fetchall()])

    # Close the database connection
    conn.close()

    

    # Create a combobox for selecting supplier
    item2_combobox = ttk.Combobox(root, values=supplier_names, state="readonly", width=50)
    item2_combobox.pack(pady=10)

    

    #style = ttk.Style()
    style = ttk.Style(root)
    style.theme_use("clam")  # Use 'clam' theme
    style.configure("Treeview",height=50,
                    background="#008080",  # Background color
                    fieldbackground="#008080",
                    foreground="white"  # Foreground color
                    )

    tree = ttk.Treeview(root, style="Treeview", height=30)  # Adjust the height as needed

    # Create a treeview to display the records
    tree = ttk.Treeview(root, columns=("PAF No", "App Date", "Supplier Code", "Item Code", "Item Name", "Origin", "Current Rate", "Payment Term"), show="headings")
    tree.pack(pady=10)

    # Set column headings
    tree.heading("PAF No", text="PAF No")
    tree.heading("App Date", text="App Date")
    tree.heading("Supplier Code", text="Supplier Code")
    tree.heading("Item Code", text="Item Code")
    tree.heading("Item Name", text="Item Name")
    tree.heading("Origin", text="Origin")
    tree.heading("Current Rate", text="Current Rate")
    tree.heading("Payment Term", text="Payment Term")

    # Set column widths
    tree.column("PAF No", width=100, anchor='center')
    tree.column("App Date", width=100, anchor='center')
    tree.column("Supplier Code", width=100, anchor='center')
    tree.column("Item Code", width=100, anchor='center')
    tree.column("Item Name", width=300)
    tree.column("Origin", width=100, anchor='center')
    tree.column("Current Rate", width=100, anchor='center')
    tree.column("Payment Term", width=100, anchor='center')

    tree['height'] = 20


    # Bind the display_supplier_records function to the combobox selection event
    item2_combobox.bind("<<ComboboxSelected>>", display_supplier_records)

    

    return_button = tk.Button(root, text="Click to return Main Menu", command=lambda: return_to_main_menu(root),bg='black',fg='white')
    return_button.pack(pady=10)

    root.mainloop()

#-----------------------------------------Particular PM Supplier Price List-------------------------------------------------------
def particular_supplier_p():
    def display_supplier_records_p(event):
        # Clear the previous records from the treeview
        clear_treeview()

        selected_supplier = supplier2_combobox.get()

        # Connect to the SQLite database
        conn = sqlite3.connect('Procurement.db')

        # Query to fetch the latest records for the selected supplier
        
        query = """
            
            SELECT paf_no, app_date, supplier_code, item_code, item_name, Category,unit, Current_rate, payment_term
            FROM price_p
            WHERE supplier_name = ? 
            AND (item_code, paf_no) IN (SELECT item_code, MAX(paf_no) FROM price_p WHERE supplier_name = ? GROUP BY item_code)
            """

        # Execute the query
        cursor = conn.cursor()
        cursor.execute(query, (selected_supplier, selected_supplier))

        # Fetch all records for the selected supplier
        supplier_records = cursor.fetchall()

        # Close the database connection
        conn.close()

        # Insert records into the treeview
        for record in supplier_records:
            tree.insert("", "end", values=record)

    def clear_treeview():
        # Clear the previous records from the treeview
        for record in tree.get_children():
            tree.delete(record)

    root = tk.Tk()
    root.geometry('1200x600')
    root.title("PARTICULAR PACKING MATERIAL SUPPLIER PRICE LIST")
    root.configure(bg="#CD5C5C")

    item_label = tk.Label(root, text="Select Supplier:", bg='black', fg='white', font=('Arial', 12))
    item_label.pack(pady=10)

    # Connect to the SQLite database
    conn = sqlite3.connect('Procurement.db')

    # Query to fetch distinct supplier names from the 'price' table
    query1 = "SELECT DISTINCT supplier_name FROM price_P"

    # Execute the query
    cursor = conn.cursor()
    cursor.execute(query1)

    # Fetch all the supplier names and store them in supplier_names1 variable
    supplier_names1 = sorted([row[0] for row in cursor.fetchall()])

    # Close the database connection
    conn.close()

    

    # Create a combobox for selecting supplier
    supplier2_combobox = ttk.Combobox(root, values=supplier_names1,  width=50)
    supplier2_combobox.pack(pady=10)

    

    #style = ttk.Style()
    style = ttk.Style(root)
    style.theme_use("clam")  # Use 'clam' theme
    style.configure("Treeview",height=50,
                    background="#008080",  # Background color
                    fieldbackground="#008080",
                    foreground="white"  # Foreground color
                    )

    tree = ttk.Treeview(root, style="Treeview", height=30)  # Adjust the height as needed

    # Create a treeview to display the records
    tree = ttk.Treeview(root, columns=("PAF No", "App Date", "Supplier Code", "Item Code", "Item Name", "Category","Unit", "Current Rate", "Payment Term"), show="headings")
    tree.pack(pady=10)

    # Set column headings
    tree.heading("PAF No", text="PAF No")
    tree.heading("App Date", text="App Date")
    tree.heading("Supplier Code", text="Supplier Code")
    tree.heading("Item Code", text="Item Code")
    tree.heading("Item Name", text="Item Name")
    tree.heading("Category", text="Category")
    tree.heading("Unit", text="Unit")
    tree.heading("Current Rate", text="Current Rate")
    tree.heading("Payment Term", text="Payment Term")

    # Set column widths
    tree.column("PAF No", width=100, anchor='center')
    tree.column("App Date", width=100, anchor='center')
    tree.column("Supplier Code", width=100, anchor='center')
    tree.column("Item Code", width=100, anchor='center')
    tree.column("Item Name", width=300)
    tree.column("Category",width=100)
    tree.column("Unit", width=50)
    tree.column("Current Rate", width=100, anchor='center')
    tree.column("Payment Term", width=100, anchor='center')

    tree['height'] = 20


    # Bind the display_supplier_records function to the combobox selection event
    supplier2_combobox.bind("<<ComboboxSelected>>", display_supplier_records_p)

    

    return_button = tk.Button(root, text="Click to return Main Menu", command=lambda: return_to_main_menu(root),bg='black',fg='white')
    return_button.pack(pady=10)

    root.mainloop()


# ---------------------------------Raw Material Inventory Add Records-----------------------------------------------
def insert_Item_record():
    root = Tk()
    root.geometry('800x600+300+50')
    root.configure(bg='#CD5C5C')
    mainhead = Label(root, text="PERIDOT PRODUCTS PVT LTD", font=("Arial", 20), bg='black', fg='white')
    mainhead.place(x=200, y=20)
    subhead = Label(root, text="INVENTORY INSERT RECORD", font=("Arial", 15), bg='black', fg='white')
    subhead.place(x=240, y=80)
    root.title("Insert Raw / Packing Material ")


    item_name_label = Label(root, text='Enter Inventory Name', font=("Arial", 12), fg='black', bg='#CD5C5C')
    item_name_label.place(x=120, y=150, anchor=W)
    item_name_entry = Entry(root)
    item_name_entry.place(x=300, y=140, width=400, height=20)

    category_label = Label(root, text='Enter Category', font=("Arial", 12), fg='black', bg='#CD5C5C')
    category_label.place(x=120, y=200, anchor=W)
    category_combobox = ttk.Combobox(root,values=['RM'])
    category_combobox.place(x=300, y=195, width=200, height=20)

    item_type_label = Label(root, text='Enter Item Type', font=("Arial", 12), fg='black', bg='#CD5C5C')
    item_type_label.place(x=120, y=250, anchor=W)
    item_type_combobox = ttk.Combobox(root, values=['RM Local','RM Import'])
    item_type_combobox.place(x=300, y=245, width=200, height=20)

    def insert_Item_record2():
    # Get values from the entry fields
    
        entered_item_name = item_name_entry.get()
        selected_category = category_combobox.get()
        selected_item_type = item_type_combobox.get()

    # Connect to the SQLite database
        conn = sqlite3.connect('Procurement.db')  
        cursor = conn.cursor()

    # Insert record into the 'item' table
        cursor.execute("INSERT INTO item (item_name, category,item_type) VALUES (?, ?, ?)",
                   ( entered_item_name, selected_category,selected_item_type))
    
        conn.commit()

        #conn.close()

    # Update the status label
        status_label.config(text="Record inserted successfully!")

    def return_to_main_menu():
            root.destroy()

    insert_button1 = Button(root, text="Insert Record", command=insert_Item_record2)
    insert_button1.place(x=300,y=295)

    return_button = Button(root, text="Click Here to return to Main Menu",bg='yellow', command=return_to_main_menu)
    return_button.place(x=250, y=400)

    status_label = Label(root, text="")
    status_label.place(x=250,y=350)

# Start the Tkinter event loop
    root.mainloop()

#--------------------------------------------Packing Material Inventory Add Records---------------------------------------------------
def insert_Item_record_p():
    root = Tk()
    root.geometry('800x600+300+50')
    root.configure(bg='#CD5C5C')
    mainhead = Label(root, text="PERIDOT PRODUCTS PVT LTD", font=("Arial", 20), bg='black', fg='white')
    mainhead.place(x=200, y=20)
    subhead = Label(root, text="INVENTORY INSERT RECORD", font=("Arial", 15), bg='black', fg='white')
    subhead.place(x=240, y=80)
    root.title("Insert Raw / Packing Material ")


    item_name_label = Label(root, text='Enter Inventory Name', font=("Arial", 12), fg='black', bg='#CD5C5C')
    item_name_label.place(x=120, y=150, anchor=W)
    item_name_entry = Entry(root)
    item_name_entry.place(x=300, y=140, width=400, height=20)

    category_label = Label(root, text='Enter Category', font=("Arial", 12), fg='black', bg='#CD5C5C')
    category_label.place(x=120, y=200, anchor=W)
    category_combobox = ttk.Combobox(root,values=['Master Ctn','Inner Ctn','Stickers','Tin','Bottle','Container','Other'])
    category_combobox.place(x=300, y=195, width=200, height=20)

    finished_good_label = Label(root, text='Used in Finished Good', font=("Arial", 12), fg='black', bg='#CD5C5C')
    finished_good_label.place(x=120, y=250, anchor=W)
    finished_good_entry = Entry(root)
    finished_good_entry.place(x=300, y=245, width=200, height=20)

    def insert_Item_record2():
    # Get values from the entry fields
    
        entered_item_name = item_name_entry.get()
        selected_category = category_combobox.get()
        selected_finished_good = finished_good_entry.get()

    # Connect to the SQLite database
        conn = sqlite3.connect('Procurement.db')  
        cursor = conn.cursor()

    # Insert record into the 'item' table
        cursor.execute("INSERT INTO item_p (item_name, category,finished_good) VALUES (?, ?, ?)",
                   ( entered_item_name, selected_category,selected_finished_good))
    
        conn.commit()

        #conn.close()

    # Update the status label
        status_label.config(text="Record inserted successfully!")

    def return_to_main_menu():
            root.destroy()

    insert_button1 = Button(root, text="Insert Record", command=insert_Item_record2)
    insert_button1.place(x=300,y=295)

    return_button = Button(root, text="Click Here to return to Main Menu",bg='yellow', command=return_to_main_menu)
    return_button.place(x=250, y=400)

    status_label = Label(root, text="")
    status_label.place(x=250,y=350)

# Start the Tkinter event loop
    root.mainloop()

#--------------------------------Display All Inventory Raw Material Inventoy---------------------------------------

def Item_display_records():
    # Connect to the SQLite database
    conn = sqlite3.connect('Procurement.db')
    cursor = conn.cursor()


    # Query to fetch data from the 'price' table
    cursor.execute('SELECT * FROM item')
    query=cursor.fetchall()



    # Close the database connection
    conn.close()
    
    root = tk.Tk()
    root.title("INVENTORY DISPLAY AREA")
    root.geometry('800x500+300+50')
    root.configure(background='#CD5C5C')
    # Create a Treeview widget
    style = ttk.Style()

    # Configure the Treeview style
    style.configure("Treeview",
                background="#CD5C5C",  # Background color for cells
                fieldbackground="#DE3163",  # Field background color for cells
                foreground="white",  # Foreground color for text
                borderwidth=1,
                relief="solid"
                
                )

    # Configure the heading style
    style.configure("Treeview.Heading",
                background="#CD5C5C",  # Background color for headings
                foreground="black",  # Foreground color for heading text
                borderwidth=1,
                relief="solid"
                )

    tree = ttk.Treeview(root, style="Treeview")
    tree["columns"] = ["item_code", "item_name", "category", "item_type"]
    tree["show"] = "headings"
    tree.heading("item_code", text="Item Code")
    tree.heading("item_name", text="Item Name")
    tree.heading("category", text="Category")
    tree.heading("item_type", text="Item Type")


    tree.column('item_code', anchor='center',width=100)
    tree.column('item_name', anchor='w',width=400)
    tree.column('category', anchor='center',width=100)
    tree.column('item_type', anchor='center',width=100)
    
    # Define colors for alternate rows
    colors = ['#DE3163', '#CD5C5C']

    # Insert data into the Treeview and apply background colors
    for i, row in enumerate(query):
        color = colors[i % 2]  # Alternate colors
        tree.insert("", "end", values=row, tags=('colored',))
        tree.tag_configure('colored', background=color)
        tree.tag_configure('colored', foreground='white')

     # Pack the Treeview widget and increase the height
    tree.pack(expand=True, fill=tk.BOTH)

    #for row in query:
     #   tree.insert("", "end", values=row)


# Pack the Treeview widget
    tree.pack()

    return_button = tk.Button(root, text="Click to return Main Menu",bg='yellow',command=lambda: return_to_main_menu(root))
    return_button.pack(pady=10)

def return_to_main_menu(root):
        root.destroy()


#-------------------------------------------Packing Material Inventory Display all Records -----------------------------------------------------------------
def Item_display_records_p():
    # Connect to the SQLite database
    conn = sqlite3.connect('Procurement.db')
    cursor = conn.cursor()


    # Query to fetch data from the 'price' table
    cursor.execute('SELECT * FROM item_p')
    # cursor.execute('SELECT * FROM item_p ORDER BY item_name ASC')
    query=cursor.fetchall()



    # Close the database connection
    conn.close()
    
    root = tk.Tk()
    root.title("INVENTORY DISPLAY AREA")
    root.geometry('1000x500+100+50')
    root.configure(background='#008080')
    # Create a Treeview widget
        

    style = ttk.Style(root)
    style.theme_use("clam")  # Use 'clam' theme
    style.configure("Treeview",

                    background="#008080",

                    foreground="white"  # Foreground color
    
                    
                    )



    

    tree = ttk.Treeview(root, style="Treeview")
    tree["columns"] = ["item_code", "item_name", "category", "finished_good"]
    tree["show"] = "headings"
    tree.heading("item_code", text="Item Code")
    tree.heading("item_name", text="Item Name")
    tree.heading("category", text="Category")
    tree.heading("finished_good", text="Finished Good")


    tree.column('item_code', anchor='center',width=100)
    tree.column('item_name', anchor='w',width=400)
    tree.column('category', anchor='center',width=100)
    tree.column('finished_good', anchor='w',width=400)
    
    tree['height'] = 20
    

    # Insert data into the Treeview and apply background colors

    for index, row in enumerate(query): 
        tree.insert("", "end", values=row)  # Insert the entire tuple directly
        #tree.insert("", "end", values=[""])  # Add an empty row


           
    
        tree.pack()



    return_button = tk.Button(root, text="Click to return Main Menu",bg='yellow',command=lambda: return_to_main_menu(root))
    return_button.pack(pady=5)

def return_to_main_menu(root):
        root.destroy()
#-------------------------------------------Raw Material inventory Deletion Record Code------------------------------------------------------

def Delete_item_window():
    root = tk.Tk()
    root.title ('Item Deletion Record')
    root.geometry("600x600+400+50")
    root.configure(bg="#CD5C5C")

    linpt = Label(root,text='Enter Item Code for Delete',bg="#CD5C5C",fg='white',font=("Areal",12))
    linpt.place(x=200,y=50)
    entry_item_code=ttk.Entry(root,width=10)
    entry_item_code.place(x=280,y=100)
    btn_show_detailI = Button(root, text='Item  Detail', command=lambda: show_item_detail())
    btn_show_detailI.place(x=200, y=200) 

    def show_item_detail():
        item_code = entry_item_code.get()

        connection = sqlite3.connect('Procurement.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM item WHERE item_code = ?', (item_code,))
        existing_item = cursor.fetchone()

        if existing_item:
            detail_window = Toplevel(root)
            detail_window.title("Raw / Packing Material Detail")
            detail_window.geometry('420x210+450+350')
            detail_window.configure(bg='black')

            fields = ["Item Code", "Item Name", "Category", "Item Type"]
            for i, field in enumerate(fields):
                label=Label(detail_window,text=f"{field}:{existing_item[i]}",bg='black',fg='white',anchor=tk.W,padx=10)
                label.grid(row=i,column=0,sticky='w')

                confirm_buttonI = Button(detail_window, text="Confirm Deletion",command=lambda: delete_inv_item())
                confirm_buttonI.place(x=190,y=180)

                status_label = Label(root, text='')
                status_label.place(x=100, y=150)

            def delete_inv_item():
                item_code = entry_item_code.get()

                connection = sqlite3.connect('Procurement.db')
                cursor = connection.cursor()

                cursor.execute('DELETE FROM item WHERE item_code = ?',(item_code,))
                connection.commit()
        
                entry_item_code.delete(0, END)

                status_label.config(text='Record Sucessfully Deleted')

    return_button_I2 = Button(root,text= 'Click to Return Main Menu',bg='yellow', command=lambda:return_to_main_menu(root))
    return_button_I2.place(x=200,y=540)

    root.mainloop()

def return_to_main_menu(root):
    root.destroy()    
    
#------------------------------------------Packing Material Inventory Delete Records-------------------------------------------------------------------

def Delete_item_p():
    root = tk.Tk()
    root.title ('Item Deletion Record')
    root.geometry("600x600+400+50")
    root.configure(bg="#CD5C5C")

    linpt = Label(root,text='Enter Item Code for Delete',bg="#CD5C5C",fg='white',font=("Areal",12))
    linpt.place(x=200,y=50)
    entry_item_code=ttk.Entry(root,width=10)
    entry_item_code.place(x=280,y=100)
    btn_show_detailI = Button(root, text='Item  Detail', command=lambda: show_item_detail())
    btn_show_detailI.place(x=200, y=200) 

    def show_item_detail():
        item_code = entry_item_code.get()

        connection = sqlite3.connect('Procurement.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM item_p WHERE item_code = ?', (item_code,))
        existing_item = cursor.fetchone()

        if existing_item:
            detail_window = Toplevel(root)
            detail_window.title("Raw / Packing Material Detail")
            detail_window.geometry('420x210+450+350')
            detail_window.configure(bg='black')

            fields = ["Item Code", "Item Name", "Category", "Finished Good"]
            for i, field in enumerate(fields):
                label=Label(detail_window,text=f"{field}:{existing_item[i]}",bg='black',fg='white',anchor=tk.W,padx=10)
                label.grid(row=i,column=0,sticky='w')

                confirm_buttonI = Button(detail_window, text="Confirm Deletion",command=lambda: delete_inv_item())
                confirm_buttonI.place(x=190,y=180)

                status_label = Label(root, text='')
                status_label.place(x=100, y=150)

            def delete_inv_item():
                item_code = entry_item_code.get()

                connection = sqlite3.connect('Procurement.db')
                cursor = connection.cursor()

                cursor.execute('DELETE FROM item_p WHERE item_code = ?',(item_code,))
                connection.commit()
        
                entry_item_code.delete(0, END)

                status_label.config(text='Record Sucessfully Deleted')

    return_button_I2 = Button(root,text= 'Click to Return Main Menu',bg='yellow', command=lambda:return_to_main_menu(root))
    return_button_I2.place(x=200,y=540)

    root.mainloop()

def return_to_main_menu(root):
    root.destroy()        

#------------------------------------Raw Material Pirce Add Record-------------------------------------------------------
def return_to_main_menu(root):
    root.destroy()


def Price_insert_menu():
    def insert_Price_record():
        # Get values from the entry fields
        entered_paf_no = paf_no_entry.get()
        entered_app_date = app_date_entry.get()
        selected_supplier_code = supplier_code_combobox.get()
        selected_supplier = supplier_combobox.get()
        selected_item_code = item_code_combobox.get()
        selected_item_name = item_name_combobox.get()
        selected_category = Category_combobox.get()
        selected_orign = origin_entry.get()
        entered_current_rate = current_rate_entry.get()
        selected_payment_term = payment_term_combobox.get()

        # Connect to the SQLite database
        conn = sqlite3.connect('Procurement.db')  
        cursor = conn.cursor()

        # Insert record into the price table
        cursor.execute("INSERT INTO price (paf_no, app_date, Supplier_Code, supplier_name, item_code, item_name, Category,origin, Current_rate,payment_term) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?,?)",
                       (entered_paf_no, entered_app_date,selected_supplier_code, selected_supplier, selected_item_code, selected_item_name, selected_category,selected_orign, entered_current_rate,selected_payment_term))
        conn.commit()

        conn.close()

        # Update the status label
        status_label.config(text="Record inserted successfully!")

    def fetch_suppliers():
        # Connect to the SQLite database
        conn = sqlite3.connect('Procurement.db')  
        cursor = conn.cursor()

        # Fetch data from the supplier table
        cursor.execute("SELECT DISTINCT supplier_name,supplier_code,payment_term FROM supplier")
        supplier_data = sorted(cursor.fetchall())

        # Update the supplier_combobox with fetched data
        supplier_combobox['values'] = [supp[0] for supp in supplier_data]
        supplier_code_combobox['values'] = [supp[1] for supp in supplier_data]
        payment_term_combobox['values'] = [supp[2] for supp in supplier_data]


    def on_supplier_code_selected(event):
        selected_supplier = supplier_combobox.get()

        # Connect to the SQLite database
        conn = sqlite3.connect('Procurement.db')
        cursor = conn.cursor()

        # Fetch the supplier name based on the selected supplier code
        cursor.execute('SELECT supplier_code,payment_term FROM supplier WHERE supplier_name = ?', (selected_supplier,))
        result = cursor.fetchone()

        conn.close()

        # Check if a result was found
        if result:
            supplier_code,payment_term = result
            supplier_code_combobox.set(supplier_code)
            payment_term_combobox.set(payment_term)

           
        else:
            print(f"No supplier found for code {selected_supplier}")

    def fetch_items():
        # Connect to the SQLite database
        conn = sqlite3.connect('Procurement.db')  
        cursor = conn.cursor()

        # Fetch data from the item table
        cursor.execute("SELECT DISTINCT item_name, item_code FROM item")
        item_data = sorted(cursor.fetchall())

        # Update the item_code_combobox and item_name_combobox with fetched data
        item_name_combobox['values'] = [item[0] for item in item_data]
        item_code_combobox['values'] = [item[1] for item in item_data]

    def on_item_code_selected(event):
        selected_item_name = item_name_combobox.get()

        # Connect to the SQLite database
        conn = sqlite3.connect('Procurement.db')
        cursor = conn.cursor()

        # Fetch the supplier name based on the selected supplier code
        cursor.execute('SELECT item_code FROM item WHERE item_name = ?', (selected_item_name,))
        result2 = cursor.fetchone()

        conn.close()

        # Check if a result was found
        if result2:
            item_code = result2[0]
            item_code_combobox.set(item_code)
        else:
            print(f"No supplier found for code {selected_item_name}")  

    window = tk.Tk()
    window.title("Data Entry")
    window.geometry('800x600+300+50')
    window.configure(bg='#CD5C5C')
    mainhead = tk.Label(window, text="PERIDOT PRODUCTS PVT LTD", font=("Arial", 20), bg='black', fg='white')
    mainhead.place(x=200, y=20)
    subhead = tk.Label(window, text="PRICE INSERT RECORD", font=("Arial", 15), bg='black', fg='white')
    subhead.place(x=240, y=80)
    window.title("Prince Insert Area")

    paf_no_label = tk.Label(window, text="PAF No:",font=("Arial",12),fg='black',bg='#CD5C5C')
    paf_no_label.place (x=100, y=130, anchor='w')

    paf_no_entry = tk.Entry(window)
    paf_no_entry.place(x=300,y=120, width= 50, height=20)

    app_date_label = tk.Label(window, text="PAF Approval Date:",font=("Arial",12),fg='black',bg='#CD5C5C')                       
    app_date_label.place(x=100,y=160, anchor='w')
    

    app_date_entry = tk.Entry(window)
    app_date_entry.place(x=300,y=150, width= 100, height=20)
    message_label = tk.Label(window, text="Date Type in dd/mm/yyyy",font=("Arial",8),fg='white',bg='#CD5C5C')
    message_label.place (x=450, y=150)  
    


    supplier_label = tk.Label(window, text="Supplier :",font=("Arial",12),fg='black',bg='#CD5C5C')
    supplier_label.place(x=100,y=190, anchor='w')

    supplier_combobox = tk.ttk.Combobox(window)
    supplier_combobox.place(x=300,y=180, width= 300, height=20)

    supplier_code_label = tk.Label(window, text="Supplier Code:",font=("Arial",12),fg='black',bg='#CD5C5C')
    supplier_code_label.place(x=100,y=220, anchor='w')

    supplier_code_combobox = tk.ttk.Combobox(window)
    supplier_code_combobox.place(x=300,y=210, width= 100, height=20)

    payment_term_label = tk.Label(window, text='Payment Term',font=("Arial",12),fg='black',bg='#CD5C5C')
    payment_term_label.place(x=100,y=250,anchor='w')

    payment_term_combobox = tk.ttk.Combobox(window)
    payment_term_combobox.place(x=300,y=250,anchor='w')

    fetch_suppliers()
    supplier_combobox.bind("<<ComboboxSelected>>", on_supplier_code_selected)

    item_name_label = tk.Label(window, text="Item Name:",font=("Arial",12),fg='black',bg='#CD5C5C')
    item_name_label.place(x=100,y=280, anchor='w')

    item_name_combobox = tk.ttk.Combobox(window)
    item_name_combobox.place(x=300,y=270, width= 300, height=20)

    item_code_label = tk.Label(window, text="Item Code:",font=("Arial",12),fg='black',bg='#CD5C5C')
    item_code_label.place(x=100,y=310, anchor='w')

    item_code_combobox = tk.ttk.Combobox(window)
    item_code_combobox.place(x=300,y=310, anchor='w',height=20)
    fetch_items()
    item_name_combobox.bind("<<ComboboxSelected>>", on_item_code_selected)

    Category_label = tk.Label(window, text="Category:",font=("Arial",12),fg='black',bg='#CD5C5C')
    Category_label.place(x=100,y=340, anchor='w')

    Category_combobox = tk.ttk.Combobox(window,values=['RM'])
    Category_combobox.place(x=300,y=338, anchor='w')

    origin_label = tk.Label(window, text="Item Origin",font=("Arial",12),fg='black',bg='#CD5C5C')
    origin_label.place(x=100,y=370, anchor='w')

    origin_entry = tk.Entry(window)
    origin_entry.place(x=300,y=370, anchor='w')


    current_rate_label = tk.Label(window, text="Current Rate:",font=("Arial",12),fg='black',bg='#CD5C5C')
    current_rate_label.place(x=100,y=400, anchor='w')

    current_rate_entry = tk.Entry(window)
    current_rate_entry.place(x=300,y=400, anchor='w')

    insert_button = tk.Button(window, text="Insert Record", command=insert_Price_record)
    insert_button.place(x=200,y=480, anchor='w')

    status_label = tk.Label(window, text="",bg='#CD5C5C')
    status_label.place(x=200,y=520)

    return_button = tk.Button(window, text="Click to return Main Menu", bg='yellow', command=lambda: return_to_main_menu(window))
    return_button.place(x=200,y=560)

    # Start the Tkinter event loop
    window.mainloop()

def main_menu():
    master = Tk()
    master.title("Main Menu")

#_____________________________________Packing Material Price Add  Records______________________________________________________________________
def return_to_main_menu(root):
    root.destroy()


def Price_insert_menu_p():
    def insert_Price_record():
        # Get values from the entry fields
        entered_paf_no = paf_no_entry.get()
        entered_app_date = app_date_entry.get()
        selected_supplier_code = supplier_code_combobox.get()
        selected_supplier = supplier_combobox.get()
        selected_item_code = item_code_combobox.get()
        selected_item_name = item_name_combobox.get()
        selected_category = Category_combobox.get()
        selected_unit = unit_combobox.get()
        entered_current_rate = current_rate_entry.get()
        selected_payment_term = payment_term_combobox.get()

        # Connect to the SQLite database
        conn = sqlite3.connect('Procurement.db')  
        cursor = conn.cursor()

        # Insert record into the price table
        cursor.execute("INSERT INTO price_p (paf_no, app_date, Supplier_Code, supplier_name, item_code, item_name, Category,unit, Current_rate,payment_term) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?,?)",
                       (entered_paf_no, entered_app_date,selected_supplier_code, selected_supplier, selected_item_code, selected_item_name, selected_category,selected_unit, entered_current_rate,selected_payment_term))
        conn.commit()

        conn.close()

        # Update the status label
        status_label.config(text="Record inserted successfully!")

    def fetch_suppliers():
        # Connect to the SQLite database
        conn = sqlite3.connect('Procurement.db')  
        cursor = conn.cursor()

        # Fetch data from the supplier table
        cursor.execute("SELECT DISTINCT supplier_name,supplier_code,payment_term FROM supplier_p")
        supplier_data = sorted(cursor.fetchall())

        # Update the supplier_combobox with fetched data
        supplier_combobox['values'] = [supp[0] for supp in supplier_data]
        supplier_code_combobox['values'] = [supp[1] for supp in supplier_data]
        payment_term_combobox['values'] = [supp[2] for supp in supplier_data]


    def on_supplier_code_selected(event):
        selected_supplier = supplier_combobox.get()

        # Connect to the SQLite database
        conn = sqlite3.connect('Procurement.db')
        cursor = conn.cursor()

        # Fetch the supplier name based on the selected supplier code
        cursor.execute('SELECT supplier_code,payment_term FROM supplier_p WHERE supplier_name = ?', (selected_supplier,))
        result = cursor.fetchone()

        conn.close()

        # Check if a result was found
        if result:
            supplier_code,payment_term = result
            supplier_code_combobox.set(supplier_code)
            payment_term_combobox.set(payment_term)

           
        else:
            print(f"No supplier found for code {selected_supplier}")

    def fetch_items():
        # Connect to the SQLite database
        conn = sqlite3.connect('Procurement.db')  
        cursor = conn.cursor()

        # Fetch data from the item table
        cursor.execute("SELECT DISTINCT item_name, item_code FROM item_p")
        item_data = sorted(cursor.fetchall())

        # Update the item_code_combobox and item_name_combobox with fetched data
        item_name_combobox['values'] = [item[0] for item in item_data]
        item_code_combobox['values'] = [item[1] for item in item_data]

    def on_item_code_selected(event):
        selected_item_name = item_name_combobox.get()

        # Connect to the SQLite database
        conn = sqlite3.connect('Procurement.db')
        cursor = conn.cursor()

        # Fetch the supplier name based on the selected supplier code
        cursor.execute('SELECT item_code FROM item_p WHERE item_name = ?', (selected_item_name,))
        result2 = cursor.fetchone()

        conn.close()

        # Check if a result was found
        if result2:
            item_code = result2[0]
            item_code_combobox.set(item_code)
        else:
            print(f"No supplier found for code {selected_item_name}")  

    window = tk.Tk()
    window.title("Data Entry")
    window.geometry('800x600+300+50')
    window.configure(bg='#CD5C5C')
    mainhead = tk.Label(window, text="PERIDOT PRODUCTS PVT LTD", font=("Arial", 20), bg='black', fg='white')
    mainhead.place(x=200, y=20)
    subhead = tk.Label(window, text="PM PRICE INSERT RECORD", font=("Arial", 15), bg='black', fg='white')
    subhead.place(x=240, y=80)
    window.title("Packing Material Insert Area")

    paf_no_label = tk.Label(window, text="PAF No:",font=("Arial",12),fg='black',bg='#CD5C5C')
    paf_no_label.place (x=100, y=130, anchor='w')

    paf_no_entry = tk.Entry(window)
    paf_no_entry.place(x=300,y=120, width= 50, height=20)

    app_date_label = tk.Label(window, text="PAF Approval Date:",font=("Arial",12),fg='black',bg='#CD5C5C')                       
    app_date_label.place(x=100,y=160, anchor='w')

    app_date_entry = tk.Entry(window)
    app_date_entry.place(x=300,y=150, width= 100, height=20)

    supplier_label = tk.Label(window, text="Supplier :",font=("Arial",12),fg='black',bg='#CD5C5C')
    supplier_label.place(x=100,y=190, anchor='w')

    supplier_combobox = tk.ttk.Combobox(window)
    supplier_combobox.place(x=300,y=180, width= 300, height=20)

    supplier_code_label = tk.Label(window, text="Supplier Code:",font=("Arial",12),fg='black',bg='#CD5C5C')
    supplier_code_label.place(x=100,y=220, anchor='w')

    supplier_code_combobox = tk.ttk.Combobox(window)
    supplier_code_combobox.place(x=300,y=210, width= 100, height=20)

    payment_term_label = tk.Label(window, text='Payment Term',font=("Arial",12),fg='black',bg='#CD5C5C')
    payment_term_label.place(x=100,y=250,anchor='w')

    payment_term_combobox = tk.ttk.Combobox(window)
    payment_term_combobox.place(x=300,y=250,anchor='w')

    fetch_suppliers()
    supplier_combobox.bind("<<ComboboxSelected>>", on_supplier_code_selected)

    item_name_label = tk.Label(window, text="Item Name:",font=("Arial",12),fg='black',bg='#CD5C5C')
    item_name_label.place(x=100,y=280, anchor='w')

    item_name_combobox = tk.ttk.Combobox(window)
    item_name_combobox.place(x=300,y=270, width= 300, height=20)

    item_code_label = tk.Label(window, text="Item Code:",font=("Arial",12),fg='black',bg='#CD5C5C')
    item_code_label.place(x=100,y=310, anchor='w')

    item_code_combobox = tk.ttk.Combobox(window)
    item_code_combobox.place(x=300,y=310, anchor='w',height=20)
    fetch_items()
    item_name_combobox.bind("<<ComboboxSelected>>", on_item_code_selected)

    Category_label = tk.Label(window, text="Category:",font=("Arial",12),fg='black',bg='#CD5C5C')
    Category_label.place(x=100,y=340, anchor='w')

    Category_combobox = tk.ttk.Combobox(window,values=['Master Ctn','Inner Ctn','Stickers','Tin','Bottle','Container','Other'])
    Category_combobox.place(x=300,y=338, anchor='w')

    unit_label = tk.Label(window, text="Item Unit",font=("Arial",12),fg='black',bg='#CD5C5C')
    unit_label.place(x=100,y=370, anchor='w')

    unit_combobox = tk.ttk.Combobox(window,values=['Pcs','Kg','Meter','Roll'])
    unit_combobox.place(x=300,y=370, anchor='w')


    current_rate_label = tk.Label(window, text="Current Rate:",font=("Arial",12),fg='black',bg='#CD5C5C')
    current_rate_label.place(x=100,y=400, anchor='w')

    current_rate_entry = tk.Entry(window)
    current_rate_entry.place(x=300,y=400, anchor='w')

    insert_button = tk.Button(window, text="Insert Record", command=insert_Price_record)
    insert_button.place(x=200,y=480, anchor='w')

    status_label = tk.Label(window, text="",bg='#CD5C5C')
    status_label.place(x=200,y=520)

    return_button = tk.Button(window, text="Click to return Main Menu", bg='yellow', command=lambda: return_to_main_menu(window))
    return_button.place(x=200,y=560)

    # Start the Tkinter event loop
    window.mainloop()

def main_menu():
    master = Tk()
    master.title("Main Menu")
   
#--------------------------------Updated  Raw Material Price List--------------------------------------------------
def return_to_main_menu(root):
    root.destroy()
    

def Update_Price_list():
    # Connect to the SQLite database
    conn = sqlite3.connect('Procurement.db')

    # Query to fetch data from the 'price' table
    query = 'SELECT * FROM price ORDER BY supplier_name'
    
    # Read the data into a DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Convert 'app_date' column to datetime with correct format
    #df['app_date'] = pd.to_datetime(df['app_date'], format='%d/%m/%Y')
    df['app_date'] = pd.to_datetime(df['app_date'], format='%d/%m/%Y').dt.strftime('%d-%m-%Y')
   
    # Sort the DataFrame based on 'supplier_name', 'item_code', and 'app_date'
    df.sort_values(by=['supplier_name', 'item_code', 'app_date'], ascending=[True, True, True], inplace=False)
    

    # Create a Tkinter window
    root = tk.Tk()
    
    root.geometry('1200x800+50+50')
    root.title("Last Item Code Prices")
    root.configure(bg='#CD5C5C')
        
    top_heading_label = tk.Label(root, text="PERIDOT PRODUCTS PVT LTD", bg='#CD5C5C', fg='white', font=('Arial', 14, 'bold'))
    top_heading_label.pack(pady=10)
    top_heading_label2 = tk.Label(root, text="RAW MATERIAL PRICE LIST", bg='#CD5C5C', fg='white', font=('Arial', 14, 'bold'))
    top_heading_label2.pack(pady=10)

    
    style = ttk.Style(root)
    style.theme_use("clam")  # Use 'clam' theme
    style.configure("Treeview",

                    background="#008080",

                    foreground="white"  # Foreground color

    
                    )
    
    tree = ttk.Treeview(root, style="Treeview", height= 30)  # Adjust the height as needed

    #tree = ttk.Treeview(root, style="Treeview")

    tree["columns"] = ["paf_no","app_date","supplier_code", "supplier_name","item_name","origin","Current_rate",'payment_term']
    tree["show"] = "headings"  
    tree.heading("paf_no", text="PAF No")
    tree.heading("app_date", text="App Date")
    tree.heading("supplier_code", text="Supplier Code")
    tree.heading("supplier_name", text="Supplier Name",anchor='w')
    #tree.heading("item_code",text='Item Code')
    tree.heading("item_name", text="Item Name",anchor='w')
    tree.heading("origin", text="Origin")
    tree.heading("Current_rate", text="Current Rate")
    tree.heading("payment_term", text="Payment Term")
    #tree.heading(text="Payment Term")

    tree.column('paf_no', anchor='center', width=50)
    tree.column('app_date', anchor='center', width=100)
    tree.column('supplier_code', anchor='center', width=100)
    tree.column('supplier_name', anchor='w', width=300)
    #tree.column('item_code', anchor='w', width=100)
    tree.column('item_name', anchor='w', width=300)
    tree.column('origin', anchor='c', width=100)
    tree.column('Current_rate', anchor='center', width=100)
    tree.column('payment_term', anchor='center', width=100)
    

   
    # Iterate over each supplier code
    for sc in df['supplier_code'].unique():
        # Filter the DataFrame for the current supplier code
        filtered_df = df[df['supplier_code'] == sc]

        # Keep only the last row for each 'item_code'
        last_rows = filtered_df.groupby('item_code').last()

        


        # Display the last row for each item in the Treeview
        for index, row in last_rows.iterrows():
            
            tree.insert("", "end", values=[row['paf_no'], row['app_date'], row['supplier_code'], row['supplier_name'],row['item_name'],row['origin'], row['Current_rate'],row['payment_term']])
            
        tree.insert("", "end", values=[""])

        tree.pack()
            
           

        
     # Pack the Treeview widget and increase the height
        

         
    
    

    return_button = tk.Button(root, text="Click to return Main Menu", command=lambda: return_to_main_menu(root),bg='black', fg='white')
    return_button.pack(pady=10)

            
    root.mainloop()

#-------------------------------------------------Updated Packing Material Price List------------------------------------------------------------------
def return_to_main_menu(root):
    root.destroy()
    

def Update_Price_list_p():
    # Connect to the SQLite database
    conn = sqlite3.connect('Procurement.db')

    # Query to fetch data from the 'price' table
    #query = 'SELECT * FROM price ORDER BY supplier_name'
    query = 'SELECT * FROM price_p'

    # Read the data into a DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Convert 'app_date' column to datetime with correct format
    #df['app_date'] = pd.to_datetime(df['app_date'], format='%d/%m/%Y')
    df['app_date'] = pd.to_datetime(df['app_date'], format='%d/%m/%Y').dt.strftime('%d-%m-%Y')
   
    # Sort the DataFrame based on 'supplier_name', 'item_code', and 'app_date'
    df.sort_values(by=['supplier_name', 'item_code', 'app_date'], ascending=[True, True, True], inplace=False)
    

    # Create a Tkinter window
    root = tk.Tk()
    
    root.geometry('1200x800+50+50')
    root.title("Last Item Code Prices")
    root.configure(bg='#CD5C5C')
        
    top_heading_label = tk.Label(root, text="PERIDOT PRODUCTS PVT LTD", bg='#CD5C5C', fg='white', font=('Arial', 14, 'bold'))
    top_heading_label.pack(pady=10)
    top_heading_label2 = tk.Label(root, text="PACKING MATERIAL PRICE LIST", bg='#CD5C5C', fg='white', font=('Arial', 14, 'bold'))
    top_heading_label2.pack(pady=10)

    
    
    
    style = ttk.Style(root)
    style.theme_use("clam")  # Use 'clam' theme
    style.configure("Treeview",

                  background="#008080",

                    foreground="white"  # Foreground color

    
                  )
    
    tree = ttk.Treeview(root, style="Treeview", height= 30)  # Adjust the height as needed

    #tree = ttk.Treeview(root, style="Treeview")

    tree["columns"] = ["paf_no","app_date","supplier_code", "supplier_name","item_name","Category","unit","Current_rate",'payment_term']
    tree["show"] = "headings"  
    tree.heading("paf_no", text="PAF No")
    tree.heading("app_date", text="App Date")
    tree.heading("supplier_code", text="Supplier Code")
    tree.heading("supplier_name", text="Supplier Name",anchor='w')
    #tree.heading("item_code",text='Item Code')
    tree.heading("item_name", text="Item Name",anchor='w')
    tree.heading("Category",text="Category",anchor='center')
    tree.heading("unit", text="Unit")
    tree.heading("Current_rate", text="Current Rate")
    tree.heading("payment_term", text="Payment Term")
    
    tree.column('paf_no', anchor='center', width=50)
    tree.column('app_date', anchor='center', width=100)
    tree.column('supplier_code', anchor='center', width=100)
    tree.column('supplier_name', anchor='w', width=300)
    #tree.column('item_code', anchor='w', width=100)
    tree.column('item_name', anchor='w', width=300)
    tree.column("Category",anchor='center',width=100)
    tree.column("unit", anchor='center',width=50)
    tree.column('Current_rate', anchor='center', width=100)
    tree.column('payment_term', anchor='center', width=100)
    

   
    # Iterate over each supplier code
    for sc in df['supplier_code'].unique():
        # Filter the DataFrame for the current supplier code
        filtered_df = df[df['supplier_code'] == sc]

        # Keep only the last row for each 'item_code'
        last_rows = filtered_df.groupby('item_code').last()

        


        # Display the last row for each item in the Treeview
        for index, row in last_rows.iterrows():
            
            tree.insert("", "end", values=[row['paf_no'], row['app_date'], row['supplier_code'], row['supplier_name'],row['item_name'],row['Category'], row['unit'],row['Current_rate'],row['payment_term']])
            
        tree.insert("", "end", values=[""])

        tree.pack()
            
           

        
     
        

         
    
    

    return_button = tk.Button(root, text="Click to return Main Menu", command=lambda: return_to_main_menu(root),bg='black', fg='white')
    return_button.pack(pady=10)

            
    root.mainloop()
#---------------------------------------------------Particular Raw Material Price List---------------------------------------------------

def return_to_main_menu(root):
    root.destroy()
    

def display_current_rates(selected_item):
    

    # Connect to the SQLite database
    conn = sqlite3.connect('Procurement.db')

    # Query to fetch data from the 'price' table
    query = f"SELECT * FROM price WHERE item_name = ? ORDER BY paf_no DESC"

    # Read the data into a DataFrame
    cursor = conn.cursor()
    cursor.execute(query, (selected_item,))
    rows = sorted(cursor.fetchall())

    # Close the database connection
    conn.close()

    if not rows:
        messagebox.showinfo("No Data", "No data available for the selected item.")
        return

    # Dictionary to store the maximum paf_no for each supplier
    max_paf_no_per_supplier = {}

    # Iterate over the rows to find the maximum paf_no for each supplier
    for row in rows:
        supplier_code = row[2]  # Supplier code is at index 2
        paf_no = int(row[0])  # Convert paf_no to integer
        max_paf_no_per_supplier[supplier_code] = max(max_paf_no_per_supplier.get(supplier_code, 0), paf_no)

    # Create a Toplevel window
    rates_window = tk.Toplevel()
    rates_window.geometry('1200x500+50+50')
    rates_window.title(f"Current Rates for {selected_item}")
    rates_window.configure(bg="#CD5C5C")

    top_heading_label = tk.Label(rates_window, text="PERIDOT PRODUCT PVT LTD", bg='black', fg='white', font=('Arial', 14, 'bold'))
    top_heading_label.pack(pady=10)
    top_heading_label2 = tk.Label(rates_window, text=f"Current Rates for {selected_item}", bg='black', fg='white', font=('Arial', 14, 'bold'))
    top_heading_label2.pack(pady=10)

    style = ttk.Style()
    style = ttk.Style(rates_window)
    style.theme_use("clam")  # Use 'clam' theme
    style.configure("Treeview",

                    background="#008080",  # Background color
                    fieldbackground="#008080",
                    foreground="white",  # Foreground color
                    borderwidth=1,
                    relief="solid"
                    )
    
    tree = ttk.Treeview(rates_window, style="Treeview", height=10)  # Adjust the height as needed

    tree["columns"] = ["paf_no", "app_date", "supplier_code", "supplier_name", "item_code", "item_name", "Category", "origin", "Current_rate", 'payment_term']
    tree["show"] = "headings"
    tree.heading("paf_no", text="PAF No")
    tree.heading("app_date", text="App Date")
    tree.heading("supplier_code", text="Supplier Code")
    tree.heading("supplier_name", text="Supplier Name", anchor='w')
    tree.heading("item_code", text="Item Code", anchor='w')
    tree.heading("item_name", text="Item Name", anchor='w')
    tree.heading("Category", text="Category", anchor='w')
    tree.heading("origin", text="Origin")
    tree.heading("Current_rate", text="Current Rate")
    tree.heading("payment_term", text="Payment Term")

    tree.column('paf_no', anchor='center', width=50)
    tree.column('app_date', anchor='center', width=80)
    tree.column('supplier_code', anchor='center', width=80)
    tree.column('supplier_name', anchor='w', width=200)
    tree.column('item_code', anchor='center', width=80)
    tree.column('item_name', anchor='w', width=200)
    tree.column('Category', anchor='w', width=80)
    tree.column('origin', anchor='c', width=100)
    tree.column('Current_rate', anchor='center', width=100)
    tree.column('payment_term', anchor='center', width=100)

    # Iterate over the rows to display the data
    for row in rows:
        supplier_code = row[2]  # Supplier code is at index 2
        paf_no = int(row[0])  # Convert paf_no to integer
        if paf_no == max_paf_no_per_supplier[supplier_code]:
            tree.insert("", "end", values=row)

    tree.pack()
    return_button = tk.Button(rates_window, text="Click to return Main Menu",command=rates_window.destroy,bg='black',fg='white')
    
    return_button.pack(pady=10)


def current_rates_menu():

    def exit_mainmenu():
        master.destroy()
    # Create a Toplevel window for item selection
    master = tk.Toplevel()
    master.geometry('400x200+500+200')
    master.title("Select Item")
    master.configure(bg="#CD5C5C")

    item_label = tk.Label(master, text="Select Item:", bg='black', fg='white', font=('Arial', 12))
    item_label.pack(pady=10)

    # Connect to the SQLite database
    conn = sqlite3.connect('Procurement.db')

    # Query to fetch distinct item names from the 'price' table
    query = "SELECT DISTINCT item_name FROM price"

    # Execute the query
    cursor = conn.cursor()
    cursor.execute(query)

    # Fetch all the item names
    items = sorted([row[0] for row in cursor.fetchall()])

    # Close the database connection
    conn.close()

    item_combobox = ttk.Combobox(master, values=items, state="readonly",width=30)
    item_combobox.pack(pady=10)

    show_button = tk.Button(master, text="Show Current Rates", command=lambda: display_current_rates(item_combobox.get()))
    show_button.pack(pady=10)

    show_button = tk.Button(master, text="Exit to Menu",  command=exit_mainmenu)
    show_button.pack(pady=20)

    master.mainloop()
#-----------------------------------------Particular Packing Material Pricelist-------------------------------------------------------
def display_current_rates_p(selected_item):
    

    # Connect to the SQLite database
    conn = sqlite3.connect('Procurement.db')

    # Query to fetch data from the 'price' table
    query = f"SELECT * FROM price_p WHERE item_name = ? ORDER BY paf_no DESC"

    # Read the data into a DataFrame
    cursor = conn.cursor()
    cursor.execute(query, (selected_item,))
    rows = sorted(cursor.fetchall())

    # Close the database connection
    conn.close()

    if not rows:
        messagebox.showinfo("No Data", "No data available for the selected item.")
        return

    # Dictionary to store the maximum paf_no for each supplier
    max_paf_no_per_supplier = {}

    # Iterate over the rows to find the maximum paf_no for each supplier
    for row in rows:
        supplier_code = row[2]  # Supplier code is at index 2
        paf_no = int(row[0])  # Convert paf_no to integer
        max_paf_no_per_supplier[supplier_code] = max(max_paf_no_per_supplier.get(supplier_code, 0), paf_no)

    # Create a Toplevel window
    rates_window = tk.Toplevel()
    rates_window.geometry('1200x500+50+50')
    rates_window.title(f"Current Rates for {selected_item}")
    rates_window.configure(bg="#CD5C5C")

    top_heading_label = tk.Label(rates_window, text="PERIDOT PRODUCT PVT LTD", bg='black', fg='white', font=('Arial', 14, 'bold'))
    top_heading_label.pack(pady=10)
    top_heading_label2 = tk.Label(rates_window, text=f"Current Rates for {selected_item}", bg='black', fg='white', font=('Arial', 14, 'bold'))
    top_heading_label2.pack(pady=10)

    style = ttk.Style()
    style = ttk.Style(rates_window)
    style.theme_use("clam")  # Use 'clam' theme
    style.configure("Treeview",

                    background="#008080",  # Background color
                    fieldbackground="#008080",
                    foreground="white",  # Foreground color
                    borderwidth=1,
                    relief="solid"
                    )
    
    tree = ttk.Treeview(rates_window, style="Treeview", height=10)  # Adjust the height as needed

    tree["columns"] = ["paf_no", "app_date", "supplier_code", "supplier_name", "item_code", "item_name", "Category", "unit", "Current_rate", 'payment_term']
    tree["show"] = "headings"
    tree.heading("paf_no", text="PAF No")
    tree.heading("app_date", text="App Date")
    tree.heading("supplier_code", text="Supplier Code")
    tree.heading("supplier_name", text="Supplier Name", anchor='w')
    tree.heading("item_code", text="Item Code", anchor='w')
    tree.heading("item_name", text="Item Name", anchor='w')
    tree.heading("Category", text="Category", anchor='w')
    tree.heading("unit", text="Unit")
    tree.heading("Current_rate", text="Current Rate")
    tree.heading("payment_term", text="Payment Term")

    tree.column('paf_no', anchor='center', width=50)
    tree.column('app_date', anchor='center', width=80)
    tree.column('supplier_code', anchor='center', width=80)
    tree.column('supplier_name', anchor='w', width=200)
    tree.column('item_code', anchor='center', width=80)
    tree.column('item_name', anchor='w', width=200)
    tree.column('Category', anchor='w', width=80)
    tree.column('unit', anchor='c', width=100)
    tree.column('Current_rate', anchor='center', width=100)
    tree.column('payment_term', anchor='center', width=100)

    # Iterate over the rows to display the data
    for row in rows:
        supplier_code = row[2]  # Supplier code is at index 2
        paf_no = int(row[0])  # Convert paf_no to integer
        if paf_no == max_paf_no_per_supplier[supplier_code]:
            tree.insert("", "end", values=row)

    tree.pack()
    return_button = tk.Button(rates_window, text="Click to return Main Menu",command=rates_window.destroy,bg='black',fg='white')
    
    return_button.pack(pady=10)


def current_rates_menu_p():

    def exit_mainmenu():
        master.destroy()
    # Create a Toplevel window for item selection
    master = tk.Toplevel()
    master.geometry('400x200+500+200')
    master.title("Select Item")
    master.configure(bg="#CD5C5C")

    item_label = tk.Label(master, text="Select Item:", bg='black', fg='white', font=('Arial', 12))
    item_label.pack(pady=10)

    # Connect to the SQLite database
    conn = sqlite3.connect('Procurement.db')

    # Query to fetch distinct item names from the 'price' table
    query = "SELECT DISTINCT item_name FROM price_p"

    # Execute the query
    cursor = conn.cursor()
    cursor.execute(query)

    # Fetch all the item names
    items = sorted([row[0] for row in cursor.fetchall()])

    # Close the database connection
    conn.close()

    item_combobox = ttk.Combobox(master, values=items, state="readonly",width=30)
    item_combobox.pack(pady=10)

    show_button = tk.Button(master, text="Show Current Rates", command=lambda: display_current_rates_p(item_combobox.get()))
    show_button.pack(pady=10)

    show_button = tk.Button(master, text="Exit to Menu",  command=exit_mainmenu)
    show_button.pack(pady=20)

    master.mainloop()
#---------------------------------------Delete Raw Material Price List Item-----------------------------------------------------------------
def Delete_Price_item_window():
    root = tk.Tk()
    root.title ('Price List Deletion Record')
    root.geometry("600x600+400+50")
    root.configure(bg="#CD5C5C")

    linpt = Label(root,text='Enter PAF No for Delete',bg="#CD5C5C",fg='white',font=("Areal",12))
    linpt.place(x=200,y=50)
    entry_paf_no=ttk.Entry(root,width=10)
    entry_paf_no.place(x=280,y=100)
    btn_show_detail = Button(root, text='Item  Detail', command=lambda: show_Price_item_detail())
    btn_show_detail.place(x=200, y=200) 

    def show_Price_item_detail():
        paf_no = entry_paf_no.get()

        connection = sqlite3.connect('Procurement.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM price WHERE paf_no = ?',(paf_no,) )
        existing_item = cursor.fetchone()

        if existing_item:
            detail_price_window = Toplevel(root)
            detail_price_window.title(" Price Item Detail")
            detail_price_window.geometry("420x210+450+350")
            detail_price_window.configure(bg='black')

            fields = ['paf_no', 'app_date', 'Supplier_Code', 'supplier_name', 'item_code', 'item_name', 'Category', 'Current_rate']
            for i, field in enumerate(fields):
                label_price = Label(detail_price_window,text=f"{field} : {existing_item[i]}", bg='black',fg='white',anchor=tk.W,padx=10)
                label_price.grid(row=i,column=0,sticky='w')

                confirm_p_button = Button(detail_price_window,text='Click to confirm of Deletion',command=lambda: delete_price_item())
                confirm_p_button.place(x=190,y=180)

                status_label = Label(root, text='')
                status_label.place(x=100, y=150)
          
            


            def delete_price_item():
                paf_no = entry_paf_no.get()

                connection = sqlite3.connect('Procurement.db')
                cursor = connection.cursor()

                cursor.execute('DELETE FROM price WHERE paf_no = ?',(paf_no,) )
                connection.commit()
        
                entry_paf_no.delete(0, END)

                status_label.config(text='Record Sucessfully Deleted',bg='#CD5C5C')
                status_label.place(x=200,y=520)

    return_button_p2 = Button(root,text= 'Click to Return Main Menu',bg='yellow', command=lambda:return_to_main_menu(root))
    return_button_p2.place(x=200,y=540)

def return_to_main_menu(root):
    root.destroy()
#------------------------------------Delete Packing Material  Price List item------------------------------------------------------------------------
def Delete_Price_item_p():
    root = tk.Tk()
    root.title ('Price List Deletion Record')
    root.geometry("600x600+400+50")
    root.configure(bg="#CD5C5C")

    linpt = Label(root,text='Enter PAF No for Delete',bg="#CD5C5C",fg='white',font=("Areal",12))
    linpt.place(x=200,y=50)
    entry_paf_no=ttk.Entry(root,width=10)
    entry_paf_no.place(x=280,y=100)
    btn_show_detail = Button(root, text='Item  Detail', command=lambda: show_Price_item_detail())
    btn_show_detail.place(x=200, y=200) 

    def show_Price_item_detail():
        paf_no = entry_paf_no.get()

        connection = sqlite3.connect('Procurement.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM price_p WHERE paf_no = ?',(paf_no,) )
        existing_item = cursor.fetchone()

        if existing_item:
            detail_price_window = Toplevel(root)
            detail_price_window.title(" Price Item Detail")
            detail_price_window.geometry("420x210+450+350")
            detail_price_window.configure(bg='black')

            fields = ['paf_no', 'app_date', 'Supplier_Code', 'supplier_name', 'item_code', 'item_name', 'Category','unit' 'Current_rate','payment_term']
            for i, field in enumerate(fields):
                label_price = Label(detail_price_window,text=f"{field} : {existing_item[i]}", bg='black',fg='white',anchor=tk.W,padx=10)
                label_price.grid(row=i,column=0,sticky='w')

                confirm_p_button = Button(detail_price_window,text='Click to confirm of Deletion',command=lambda: delete_price_item())
                confirm_p_button.place(x=190,y=180)

                status_label = Label(root, text='')
                status_label.place(x=100, y=150)
          
            


            def delete_price_item():
                paf_no = entry_paf_no.get()

                connection = sqlite3.connect('Procurement.db')
                cursor = connection.cursor()

                cursor.execute('DELETE FROM price_p WHERE paf_no = ?',(paf_no,) )
                connection.commit()
        
                entry_paf_no.delete(0, END)

                status_label.config(text='Record Sucessfully Deleted',bg='#CD5C5C')
                status_label.place(x=200,y=520)

    return_button_p2 = Button(root,text= 'Click to Return Main Menu',bg='yellow', command=lambda:return_to_main_menu(root))
    return_button_p2.place(x=200,y=540)

def return_to_main_menu(root):
    root.destroy()
#------------------------------------------------Main Menu--------------------------------------------------------------------------

def main_menu():
    def exit_mainmenu():
        master.destroy()
    master = Tk()
    master.title("Main Menu")
    master.geometry("1000x600+150+0")
    f1 = Frame(master, bg='black', width=1000, height=100)
    f1.place(x=0, y=0)
    l1 = Label(master, text='PERIDOT PRODUCTS PVT LTD', font=("Arial", 20), fg='white', bg='black')
    l1.place(x=300, y=10)
    l2 = Label(master, text='PROCUREMENT MAIN MENU', font=("Arial", 15), fg='white', bg='black')
    l2.place(x=360, y=50)
    f2 = Frame(master, bg='#CD5C5C', width=333, height=500)
    f2.place(x=0, y=105)
    lsupp = Label(master, text='Supplier Section', font=("Arial", 15), fg='white', bg='#CD5C5C')
    lsupp.place(x=73, y=130)
    f3 = Frame(master, bg='#CD5C5C', width=333, height=500)
    f3.place(x=335, y=105)
    litem = Label(master, text='Inventory Section', font=("Arial", 15), fg='white', bg='#CD5C5C')
    litem.place(x=430, y=130)
    f4 = Frame(master, bg='#CD5C5C', width=333, height=500)
    f4.place(x=670, y=105)
    litem = Label(master, text='Price Section', font=("Arial", 15), fg='white', bg='#CD5C5C')
    litem.place(x=760, y=130)
    
    #--------------------------------- Main Menu Buttons-------------------------------------------------------------------------
    # Supplier Buttons
    insert_button = Button(master, text="1. Add RM Supplier", command=insert_record,width=20,anchor='w',bg='black',fg='white')
    insert_button.place(x=78, y=200)
    insert_button = Button(master, text="2. Add PM Supplier", command=insert_record_p,width=20,anchor='w',bg='black',fg='white')
    insert_button.place(x=78, y=250)
    insert_button = Button(master, text="3. Display RM Suppliers ",command=display_suppliers_2,width=20,anchor='w',bg='black',fg='white')
    insert_button.place(x=78, y=300)
    insert_button = Button(master, text="4. Display PM Suppliers",command=display_suppliers_p,width=20,anchor='w',bg='black',fg='white')
    insert_button.place(x=78, y=350)
    insert_button = Button(master, text="5. Delete RM Record",command=delete_window,width=20,anchor='w',bg='black',fg='white')
    insert_button.place(x=78, y=400)
    insert_button = Button(master, text="6. Delete PM Record",command=delete_supplier_p,width=20,anchor='w',bg='black',fg='white')
    insert_button.place(x=78, y=450)
    insert_button4 = Button(master, text="7. Particular RM Supplier", command=particular_supplier,width=20,anchor='w',bg='black',fg='white')
    insert_button4.place(x=78, y=500)
    insert_button4 = Button(master, text="8. Particular PM Supplier", command=particular_supplier_p,width=20,anchor='w',bg='black',fg='white')
    insert_button4.place(x=78, y=550)



    # Item Buttons
    insert_button4 = Button(master, text="1. Add RM Inventory", command=insert_Item_record,width=20,anchor='w',bg='black',fg='white')
    insert_button4.place(x=420, y=200)
    insert_button4 = Button(master, text="2. Add PM Inventory", command=insert_Item_record_p,width=20,anchor='w',bg='black',fg='white')
    insert_button4.place(x=420, y=250)

    insert_button4 = Button(master, text="3. Display RM Inventory", command=Item_display_records,width=20,anchor='w',bg='black',fg='white')
    insert_button4.place(x=420, y=300)

    insert_button4 = Button(master, text="4. Display PM Inventory", command=Item_display_records_p,width=20,anchor='w',bg='black',fg='white')
    insert_button4.place(x=420, y=350)
   
    insert_button4 = Button(master, text="5. Delete RM Inventory", command=Delete_item_window,width=20,anchor='w',bg='black',fg='white')
    insert_button4.place(x=420, y=400)

    insert_button4 = Button(master, text="6. Delete PM Inventory", command=Delete_item_p,width=20,anchor='w',bg='black',fg='white')
    insert_button4.place(x=420, y=450)
    
    # Price Buttons
    insert_button = Button(master, text="1. Add RM Price Record",command=Price_insert_menu, width=20,anchor='w',bg='black',fg='white')
    insert_button.place(x=750, y=200)
    insert_button = Button(master, text="2. Add PM Price Record",command=Price_insert_menu_p, width=20,anchor='w',bg='black',fg='white')
    insert_button.place(x=750, y=250)
    display_button = Button(master, text="3. RM Update Price List", command=Update_Price_list,width=20,anchor='w',bg='black',fg='white')
    display_button.place(x=750, y=300)
    display_button = Button(master, text="4. PM Update Price List", command=Update_Price_list_p,width=20,anchor='w',bg='black',fg='white')
    display_button.place(x=750, y=350)
    insert_button4 = Button(master, text="5. Delete RM Price List", command=Delete_Price_item_window,width=20,anchor='w',bg='black',fg='white')
    insert_button4.place(x=750, y=400)
    insert_button4 = Button(master, text="6. Delete PM Price List", command=Delete_Price_item_p,width=20,anchor='w',bg='black',fg='white')
    insert_button4.place(x=750, y=450)
    insert_button4 = Button(master, text="7. Particular RM Price List", command=current_rates_menu,width=20,anchor='w',bg='black',fg='white')
    insert_button4.place(x=750, y=500)
    insert_button4 = Button(master, text="8. Particular PM Price List", command=current_rates_menu_p,width=20,anchor='w',bg='black',fg='white')
    insert_button4.place(x=750, y=550)

    insert_button4 = Button(master, text="Exit Form Program", command=exit_mainmenu,width=20,anchor='c',bg='#CD5C5C',fg='yellow')
    insert_button4.place(x=400, y=550)



    # command=Price_insert_menu


    master.mainloop()

main_menu()

    