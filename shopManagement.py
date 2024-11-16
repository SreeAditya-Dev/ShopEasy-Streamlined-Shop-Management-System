#Importing the required modules
import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import matplotlib.pyplot as plt
from datetime import datetime
from tkinter import Label, Entry, Button, Frame, Canvas, Scrollbar
import mysql.connector
from PIL import Image, ImageTk, ImageDraw
import time
from datetime import datetime


#Connecting to the database and creating table
db=mysql.connector.connect(user="root",passwd="admin",host="localhost") 
 
my_cursor=db.cursor() #getting the cursor object
my_cursor.execute("CREATE DATABASE IF NOT EXISTS Shop") #creating the database named library

db=mysql.connector.connect(user="root",passwd="admin",host="localhost",database='Shop') 
my_cursor=db.cursor()
#query to create a table products
query="CREATE TABLE IF NOT EXISTS products (date VARCHAR(20),prodName VARCHAR(20), prodPrice VARCHAR(50))" 
my_cursor.execute(query) #executing the query

db=mysql.connector.connect(user="root",passwd="admin",host="localhost",database='Shop') 
my_cursor=db.cursor()
#query to create a table sale
query="CREATE TABLE IF NOT EXISTS sale (custName VARCHAR(20), date VARCHAR(20),Ph bigint, Amount INTEGER )" 
my_cursor.execute(query) #executing the query

#query to create a table login
query="CREATE TABLE IF NOT EXISTS login (username varchar(20) primary key,password varchar(20) not null)" 
my_cursor.execute(query) #executing the query

def signup():
    global win_signup, username_signup, password_signup, confirmpassword_signup
    win_signup = tkinter.Toplevel(win)
    win_signup.title("Sign Up")
    win_signup.geometry("700x600")  # Set the window size to 700x600
    win_signup.configure(bg='honeydew2')

    # Heading for the Sign Up window
    signup_heading = Label(win_signup, text="Sign Up", fg='black', font=('Courier', 20, 'bold'))
    signup_heading.place(relx=0.4, rely=0.1)

    # Calculate the positions and sizes relative to the window size
    label_width = 100
    entry_width = 300
    entry_height = 30
    padding = 10  # Padding between widgets

    # Label and Entry for Username
    label1 = Label(win_signup, text="Username:", fg='black')
    label1.place(relx=0.2, rely=0.2, width=label_width)
    username_signup = Entry(win_signup)
    username_signup.place(relx=0.4, rely=0.2, width=entry_width, height=entry_height)

    # Label and Entry for Password
    label2 = Label(win_signup, text="Password:", fg='black')
    label2.place(relx=0.2, rely=0.4, width=label_width)
    password_signup = Entry(win_signup, show="*")
    password_signup.place(relx=0.4, rely=0.4, width=entry_width, height=entry_height)

    # Label and Entry for Confirm Password
    label3 = Label(win_signup, text="Confirm Password:", fg='black')
    label3.place(relx=0.2, rely=0.6, width=label_width)
    confirmpassword_signup = Entry(win_signup, show="*")
    confirmpassword_signup.place(relx=0.4, rely=0.6, width=entry_width, height=entry_height)

    # Sign Up Button
    signup_button = Button(win_signup, text="Sign Up", bg='#FF6F61', fg='black', command=register)
    signup_button.place(relx=0.35, rely=0.8, width=200, height=40)


def register():
    username = username_signup.get()
    password = password_signup.get()
    confirmpassword = confirmpassword_signup.get()

    if password == confirmpassword:
        # Connect to the database and execute a query to insert the new user
        # Replace this with your actual database connection and query
        db = mysql.connector.connect(user="root", passwd="admin", host="localhost", database='Shop')
        cursor = db.cursor()

        query = "INSERT INTO login (username, password) VALUES (%s, %s)"
        values = (username, password)

        cursor.execute(query, values)
        db.commit()

        win_signup.destroy()  # Close the sign-up window
        messagebox.showinfo("Sign Up Successful", "You can now log in with your new account.")
    else:
        messagebox.showerror("Password Mismatch", "Password and confirm password do not match.")



def logout():
    global wn
    try:
        if wn.winfo_exists():  # Check if the window exists
            wn.destroy()       # Close the main window
        home()                 # Open the login window
    except Exception as e:
        print(f"Error during logout: {e}")



def login():
    global wn
    username = username_entry.get()
    password = password_entry.get()

    try:
        # Connect to the database
        db = mysql.connector.connect(user="root", passwd="admin", host="localhost", database='Shop')
        my_cursor = db.cursor()

        query = "SELECT * FROM login WHERE username = %s AND password = %s"
        values = (username, password)
        my_cursor.execute(query, values)
        user = my_cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome, " + username)
            win.destroy()
            #Creating the main window
            wn = tkinter.Tk() 
            wn.title("SHOP EASY Management System")
            wn.configure(bg='honeydew2')

            # Get the desktop resolution
            screen_width = wn.winfo_screenwidth()
            screen_height = wn.winfo_screenheight()

            # Set the window to full screen with the desktop resolution
            wn.geometry(f"{screen_width}x{screen_height}")

            # Display the username in the top left corner
            username_label = Label(wn, text="Username: " + username, fg='grey19', bg='lime', font=('Courier', 12, 'bold'))
            username_label.place(relx=0.01, rely=0.01)

            headingFrame1 = Frame(wn, bg="snow3", bd=5)
            headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.16)
            headingLabel = Label(headingFrame1, text="Welcome to SHOP EASY Management System", fg='grey19', font=('Courier', 15, 'bold'))
            headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

            # Load and resize the logo image
            logo_image = PhotoImage(file="logo.png")  # Replace with your logo path
            logo_image = logo_image.subsample(2)
            logo_label = Label(wn, image=logo_image)
            logo_label.place(relx=0.88, rely=0.01)  # Adjust the position

            # Button to add a new product
            btn1 = Button(wn, text="Add a Product", bg='yellow', fg='black', width=20, height=2, command=addProd)
            btn1['font'] = font.Font(size=12)
            btn1.place(relx=0.4, rely=0.3)

            # Button to delete a product
            btn2 = Button(wn, text="Delete a Product", bg='pink', fg='black', width=20, height=2, command=delProd)
            btn2['font'] = font.Font(size=12)
            btn2.place(relx=0.4, rely=0.4)

            # Button to view all products
            btn3 = Button(wn, text="View Products", bg='Teal', fg='black', width=20, height=2, command=viewProds)
            btn3['font'] = font.Font(size=12)
            btn3.place(relx=0.4, rely=0.5)

            # Button to add a new sale and generate bill
            btn4 = Button(wn, text="New Customer", bg='lavender blush2', fg='black', width=20, height=2, command=newCust)
            btn4['font'] = font.Font(size=12)
            btn4.place(relx=0.4, rely=0.6)

            # Button to see the total sales
            btn5 = Button(wn, text="Total Sale", bg='lavender blush2', fg='black', width=20, height=2, command=totsale)
            btn5['font'] = font.Font(size=12)
            btn5.place(relx=0.4, rely=0.7)

            # Button to logout
            logout_button = Button(wn, text="Logout", bg='red', fg='white', width=20, height=2, command=logout)
            logout_button['font'] = font.Font(size=12)
            logout_button.place(relx=0.4, rely=0.8)


            wn.mainloop()

        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    finally:
        # Ensure the database connection is always closed
        if 'db' in locals() or 'db' in globals():
            db.close()


#Function to add the product to the database
def prodtoTable():
    #Getting the user inputs of product details from the user 
    pname= prodName.get()
    price = prodPrice.get()
    dt = date.get()
    #Connecting to the database
    db=mysql.connector.connect(user="root",passwd="admin",host="localhost",database='Shop') 
    cursor = db.cursor()
    
    #query to add the product details to the table
    query = "INSERT INTO products(date,prodName,prodPrice) VALUES(%s,%s,%s)" 
    details = (dt,pname,price)

    #Executing the query and showing the pop up message
    try:
        cursor.execute(query,details)
        db.commit()
        messagebox.showinfo('Success',"Product added successfully")
    except Exception as e:
        #print("The exception is:",e)
        messagebox.showinfo("Error","Trouble adding data into Database")
    
    wn.destroy()
#Function to get details of the product to be added
def addProd(): 
    global prodName, prodPrice, date, Canvas1,  wn
    
    #Creating the window
    wn = tkinter.Tk() 
    wn.title("SHOP EASY Management System")
    wn.configure(bg='mint cream')
    wn.minsize(width=500,height=500)
    wn.geometry("700x600")

    Canvas1 = Canvas(wn)
    Canvas1.config(bg='yellow')
    Canvas1.pack(expand=True,fill=BOTH)
    
    headingFrame1 = Frame(wn,bg='orange',bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Add a Product", fg='grey19', font=('Courier',15,'bold'))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(wn)
    labelFrame.place(relx=0.1,rely=0.4,relwidth=0.8,relheight=0.4)
        
    lable1 = Label(labelFrame, text="Date : ", fg='black')
    lable1.place(relx=0.05, rely=0.3, relheight=0.08)

    # Automatically fill the current date
    current_date = datetime.now().strftime("%d-%m-%y")
    date = Entry(labelFrame)
    date.insert(0, current_date)
    date.place(relx=0.3, rely=0.3, relwidth=0.62, relheight=0.08)
        
    # Product Name
    lable2 = Label(labelFrame,text="Product Name : ", fg='black')
    lable2.place(relx=0.05,rely=0.45, relheight=0.08)
        
    prodName = Entry(labelFrame)
    prodName.place(relx=0.3,rely=0.45, relwidth=0.62, relheight=0.08)
        
    # Product Price
    lable3 = Label(labelFrame,text="Product Price : ", fg='black')
    lable3.place(relx=0.05,rely=0.6, relheight=0.08)
        
    prodPrice = Entry(labelFrame)
    prodPrice.place(relx=0.3,rely=0.6, relwidth=0.62, relheight=0.08)
           
    #Add Button
    Btn = Button(wn,text="ADD",bg='#d1ccc0', fg='black',command=prodtoTable)
    Btn.place(relx=0.28,rely=0.85, relwidth=0.18,relheight=0.08)
    
    Quit= Button(wn,text="Quit",bg='#f7f1e3', fg='black',command=wn.destroy)
    Quit.place(relx=0.53,rely=0.85, relwidth=0.18,relheight=0.08)
    
    wn.mainloop()


#Function to remove the product from the database
def removeProd():
    #Getting the product name from the user to be removed
    name = prodName.get()
    name = name.lower()
    
    #Connecting to the database
    db=mysql.connector.connect(user="root",passwd="admin",host="localhost",database='Shop') 
    cursor = db.cursor()
    
    #Query to delete the respective product from the database
    query = "DELETE from products where LOWER(prodName) = '"+name+"'"
   #Executing the query and showing the message box
    try:
        cursor.execute(query)
        db.commit()
        #cur.execute(deleteIssue)
        #con.commit()

        messagebox.showinfo('Success',"Product Record Deleted Successfully")

    except Exception as e:
        #print("The exception is:",e)
        messagebox.showinfo("Please check Product Name")
 
    wn.destroy()
#Function to get product details from the user to be deleted
def delProd(): 

    global prodName, Canvas1,  wn
    #Creating a window
    wn = tkinter.Tk() 
    wn.title("SHOP EASY Management System")
    wn.configure(bg='mint cream')
    wn.minsize(width=500,height=500)
    wn.geometry("700x600")

    Canvas1 = Canvas(wn)
    Canvas1.config(bg="pink")
    Canvas1.pack(expand=True,fill=BOTH)
    
    headingFrame1 = Frame(wn,bg="violet",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    headingLabel = Label(headingFrame1, text="Delete Product", fg='grey19', font=('Courier',15,'bold'))
    headingLabel.place(relx=0,rely=0, relwidth=1, relheight=1)
    
    labelFrame = Frame(wn)
    labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.5)   
        
    # Product Name to Delete
    lable = Label(labelFrame,text="Product Name : ", fg='black')
    lable.place(relx=0.05,rely=0.5)
        
    prodName = Entry(labelFrame)
    prodName.place(relx=0.3,rely=0.5, relwidth=0.62)
    
    #Delete Button
    Btn = Button(wn,text="DELETE",bg='#d1ccc0', fg='black',command=removeProd)
    Btn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)
    
    Quit = Button(wn,text="Quit",bg='#f7f1e3', fg='black', command=wn.destroy)
    Quit.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)
    
    wn.mainloop()


#Function to show all the products in the database
def viewProds():
    global wn

    # Creating the window to show the products details
    wn = tkinter.Tk() 
    wn.title("SHOP EASY Management System")
    wn.configure(bg='mint cream')
    wn.minsize(width=700, height=500)

    # Get the desktop resolution
    screen_width = wn.winfo_screenwidth()
    screen_height = wn.winfo_screenheight()

    wn.geometry(f"{screen_width}x{screen_height}")

    Canvas1 = Canvas(wn)
    Canvas1.config(bg="teal")
    Canvas1.pack(expand=True, fill=tkinter.BOTH)

    headingFrame1 = Frame(wn, bg='light green', bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = Label(headingFrame1, text="View Products", fg='black', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    canvasFrame = Frame(wn)
    canvasFrame.place(relx=0.25, rely=0.25, relwidth=0.5, relheight=0.6)

    # Create a canvas and attach a scrollbar
    canvas = Canvas(canvasFrame)
    canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
    scrollbar = Scrollbar(canvasFrame, orient=tkinter.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    canvas.config(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    y = 20
    row_height = 30  # Adjust as needed

    # Connecting to the database
    db = mysql.connector.connect(user="root", passwd="admin", host="localhost", database='Shop')
    cursor = db.cursor()
    # Query to select all products from the table
    query = 'SELECT * FROM products LIMIT 50'  # Limit to 50 items

    canvas.create_text(50, 10, text="Date", font=('calibri', 11, 'bold'))
    canvas.create_text(200, 10, text="Product", font=('calibri', 11, 'bold'))
    canvas.create_text(350, 10, text="Price", font=('calibri', 11, 'bold'))
    
    # Executing the query and showing the product details
    try:
        cursor.execute(query)
        res = cursor.fetchall()

        for i in res:
            y += row_height
            canvas.create_text(50, y, text=i[0])
            canvas.create_text(200, y, text=i[1])
            canvas.create_text(350, y, text=i[2])
    except Exception as e:
        # print("The exception is:", e)
        messagebox.showinfo("Failed to fetch files from the database")

    Quit = tkinter.Button(wn, text="Quit", bg='#f7f1e3', fg='black', command=wn.destroy)
    Quit.place(relx=0.4, rely=0.9, relwidth=0.18, relheight=0.08)

    wn.mainloop()


def bill():
    global wn, date, custName, Ph, product_entries
    # Create a window
    wn = tkinter.Tk() 
    wn.title("SHOP EASY Management System")
    wn.configure(bg='lavender blush2')

    # Get the desktop resolution
    screen_width = wn.winfo_screenwidth()
    screen_height = wn.winfo_screenheight()

    wn.geometry(f"{screen_width}x{screen_height}")

    headingFrame1 = Frame(wn, bg="lavender blush2", bd=5)
    headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.16)
    headingLabel = Label(headingFrame1, text="Bill", fg='grey19', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = Frame(wn)
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    y = 0.2
    Label(labelFrame, text="%-40s%-40s%-40s%-40s" % ('Product', 'Price', 'Quantity', 'Total'),
          font=('Courier', 11, 'bold'), fg='black').place(relx=0.05, rely=0.1)

    # Getting date and customer name
    dt = date.get()
    cName = custName.get()
    Phon = Ph.get()
    totalBill = 0

    # Connecting to the database
    db = mysql.connector.connect(user="root", passwd="admin", host="localhost", database='Shop')
    cursor = db.cursor()

    # Query to select all the products
    query = 'SELECT * FROM products LIMIT 8'
    cursor.execute(query)
    res = cursor.fetchall()

    Quit = Button(wn, text="Quit", bg='#f7f1e3', fg='black', command=wn.destroy)
    Quit.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)

    # Iterate through products
    for i, product in enumerate(res):
        qty_entry = product_entries[i]
        qty = qty_entry.get()
        
        if qty and int(qty) > 0:
            qty = int(qty)
            total = qty * int(product[2])
            # Use consistent formatting with fixed-width columns
            Label(labelFrame, text="%-40s%-40s%-40s%-40s" % (product[1], product[2], qty, total), font=('Courier', 11), fg='black').place(relx=0.05, rely=y)
            totalBill += total
            y += 0.05

    # Display the total of the bill
    Label(labelFrame, text="------------------------------------------------------" + 
    "-------------------------------------------------", font=('Courier', 11), fg='black').place(relx=0.05, rely=y)
    y += 0.05

    Label(labelFrame, text="TOTAL PRICE:" + "\t\t\t\t\t\t\t\t" + str(totalBill), font=('Courier', 11, 'bold'), fg='black').place(relx=0.05, rely=y)

    query = "INSERT INTO sale(custName, date, Ph, Amount) VALUES(%s, %s, %s, %s)"
    details = (cName, dt, Phon, totalBill)
    cursor.execute(query, details)
    db.commit()

    wn.mainloop()


#Function to take the inputs form the user to generate bill    

def fetch_products_from_database():
    # Example database connection code
    db = mysql.connector.connect(user="root", passwd="admin", host="localhost", database='Shop')
    cursor = db.cursor()

    # Execute your SQL query to retrieve products
    query = 'SELECT * FROM products LIMIT 8'
    cursor.execute(query)
    res = cursor.fetchall()

    return res


def newCust():
    global wn, date, custName, Ph, product_entries

    # Create a window
    wn = tkinter.Tk()
    wn.title("SHOP EASY Management System")
    wn.configure(bg='lavender blush2')
    wn.minsize(width=500, height=500)

    # Get the desktop resolution
    screen_width = wn.winfo_screenwidth()
    screen_height = wn.winfo_screenheight()

    # Set the window to full screen with the desktop resolution
    wn.geometry(f"{screen_width}x{screen_height}")

    headingFrame1 = Frame(wn, bg="lavender blush2", bd=5)
    headingFrame1.place(relx=0.2, rely=0.05, relwidth=0.6, relheight=0.16)
    headingLabel = Label(headingFrame1, text="New Customer", fg='grey19', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    label1 = Label(wn, text="Date:", fg='black')
    label1.place(relx=0.05, rely=0.23)

    # Getting date
    date = Entry(wn)
    date.place(relx=0.3, rely=0.23, relwidth=0.62, relheight=0.04)

    # Set the default value of the date Entry field to the current date
    date.insert(0, time.strftime(" %Y-%m-%d"))
    
    
    label2 = Label(wn, text="Customer Name:", fg='black')
    label2.place(relx=0.05, rely=0.3)

    # Getting customer name
    custName = Entry(wn)
    custName.place(relx=0.3, rely=0.3, relwidth=0.62, relheight=0.04)

    # Getting customer phone number
    label3 = Label(wn, text="Phone No:", fg='black')
    label3.place(relx=0.05, rely=0.37)
    Ph = Entry(wn)
    Ph.place(relx=0.3, rely=0.37, relwidth=0.62, relheight=0.04)

    labelFrame = Frame(wn)
    labelFrame.place(relx=0.1, rely=0.42, relwidth=0.8, relheight=0.4)

    y = 0.3

    Label(labelFrame, text="%-50s%-30s%-30s" % ('Product', 'Price', 'Quantity'), font=('Courier', 11, 'bold'), fg='black').place(relx=0.05, rely=0.1)

    product_entries = []

    def populate_product_entries():
        products = fetch_products_from_database()

        for i, product in enumerate(products):
            product_name, product_price = product[1], product[2]

            Label(labelFrame, text="%-50s%-50s" % (product_name, product_price), font=('Courier', 11), fg='black').place(relx=0.05, rely=0.2 + i * 0.1)
            product_entry = Entry(labelFrame)
            product_entry.place(relx=0.6, rely=0.2 + i * 0.1, relwidth=0.2)
            product_entries.append(product_entry)

    populate_product_entries()

    # Button to generate bill
    Btn = Button(wn, text="Generate Bill", bg='#d1ccc0', fg='black', command=bill)
    Btn.place(relx=0.28, rely=0.85, relwidth=0.18, relheight=0.05)

    Quit = Button(wn, text="Quit", bg='#f7f1e3', fg='black', command=wn.destroy)
    Quit.place(relx=0.55, rely=0.85, relwidth=0.18, relheight=0.05)

    wn.mainloop()



def totsale():
    global wn, date, custName, Ph, product_entries

    wn = tkinter.Tk()
    wn.title("SHOP EASY Management System")
    wn.configure(bg='mint cream')
    wn.minsize(width=500, height=500)

    # Get the desktop resolution
    screen_width = wn.winfo_screenwidth()
    screen_height = wn.winfo_screenheight()

    wn.geometry(f"{screen_width}x{screen_height}")

    Canvas1 = tkinter.Canvas(wn)
    Canvas1.config(bg="old lace")
    Canvas1.pack(expand=True, fill=tkinter.BOTH)

    headingFrame1 = tkinter.Frame(wn, bg='old lace', bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)

    headingLabel = tkinter.Label(headingFrame1, text="TOTAL SALES", fg='black', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = tkinter.Frame(wn)
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    y = 0.25

    db = mysql.connector.connect(user="root", passwd="admin", host="localhost", database='Shop')
    cursor = db.cursor()

    query = 'SELECT * FROM sale'

    tkinter.Label(labelFrame, text="%-80s%-65s%-50s%-20s" % ('CustName', 'date', "Ph", "totalBill"),
                  font=('calibri', 11, 'bold'), fg='black').place(relx=0.07, rely=0.1)

    tkinter.Label(labelFrame, text="      ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------", fg='black').place(relx=0.05, rely=0.2)

    try:
        cursor.execute(query)
        res = cursor.fetchall()

        text = tkinter.Text(labelFrame, wrap=tkinter.WORD)
        text.place(relx=0.07, rely=y, relwidth=0.86, relheight=0.68)

        for i in res:
            text.insert(tkinter.END, "  %-30s%-30s%-20s%-20s\n" % (i[0], i[1], i[2], i[3]))

    except Exception as e:
        messagebox.showinfo("Failed to fetch files from the database")

    scrollbar = tkinter.Scrollbar(labelFrame, command=text.yview)
    scrollbar.place(relx=0.93, rely=y, relheight=0.68)
    text.config(yscrollcommand=scrollbar.set)

    def show_graph():
        # Extracting data for the line graph
        months = []
        total_sales = {}

        for i in res:
             date_str = i[1].strip()  # Remove leading and trailing spaces
             try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                month = date.strftime("%B %Y")
                if month not in months:
                    months.append(month)
                    total_sales[month] = i[3]
                else:
                     total_sales[month] += i[3]
             except ValueError as e:
                 print(f"Error parsing date: {date_str} - {e}")
        plt.figure(figsize=(8, 6))
        plt.plot(months, [total_sales[month] for month in months], marker='o', linestyle='-')
        plt.xlabel('Month')
        plt.xticks(rotation=45)
        plt.ylabel('Total Sales Amount')
        plt.title('Total Sales Line Graph')
        plt.show()

        
    tkinter.Button(wn, text="Show Graph", bg='light blue', fg='black', command=show_graph).place(relx=0.6, rely=0.9, relwidth=0.18, relheight=0.08)
    tkinter.Button(wn, text="Quit", bg='#f7f1e3', fg='black', command=wn.destroy).place(relx=0.8, rely=0.9, relwidth=0.18, relheight=0.08)

    wn.mainloop()
    


def home():
    global username_entry,password_entry,win
    # Define your login and signup functions here

    # Create the main window and set it to full screen with desktop resolution
    win = tkinter.Tk()
    win.title("SHOP EASY Management System Login")
    win.configure(bg='honeydew2')

    # Get the desktop resolution
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Set the window to full screen with the desktop resolution
    win.geometry(f"{screen_width}x{screen_height}")

    # Create a frame for the login content
    login_frame = Frame(win, bg="snow3", bd=5)
    login_frame.place(relx=0.2, rely=0.35, relwidth=0.6, relheight=0.5)

    # Heading label
    headingLabel = Label(login_frame, text="Welcome to\nSHOP EASY Management System", fg='grey19', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.2)

    # Username Entry
    username_label = Label(login_frame, text="Username:", fg="black")
    username_label.place(relx=0.2, rely=0.3)
    username_entry = Entry(login_frame)
    username_entry.place(relx=0.4, rely=0.3, relwidth=0.5, relheight=0.08)

    # Password Entry
    password_label = Label(login_frame, text="Password:", fg="black")
    password_label.place(relx=0.2, rely=0.4)
    password_entry = Entry(login_frame, show="*")
    password_entry.place(relx=0.4, rely=0.4, relwidth=0.5, relheight=0.08)

    # Login Button
    login_button = Button(login_frame, text="Login", bg="dodger blue", fg="white", command=login)
    login_button.place(relx=0.35, rely=0.6, relwidth=0.3, relheight=0.1)

    # Sign Up Button
    signup_button = Button(login_frame, text="Sign Up", bg='orange', fg='black', command=signup)
    # Adjust the placement and size of the button
    signup_button.place(relx=0.45, rely=0.8, relwidth=0.1, relheight=0.1)

    # Load and resize the circular image to be larger
    img = Image.open(r"img.jpg")
    img = img.resize((200, 200))  # Increase the size of the circular image
    mask = Image.new("L", (200, 200), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 200, 200), fill=255)
    img.putalpha(mask)
    circular_image = ImageTk.PhotoImage(img)

    # Create a label for the circular image
    image_label = Label(win, image=circular_image, bg="honeydew2")
    image_label.place(relx=0.42, rely=0.025)  # Adjust the position and size

    win.mainloop()
home()
