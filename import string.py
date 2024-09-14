import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3

# Initialize the database and create the table if it doesn't exist
def init_db():
    with sqlite3.connect("users.db") as db:
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
        db.commit()

# Password Generator GUI class
class PasswordGeneratorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title('Password Generator')
        self.master.geometry('660x500')
        self.master.config(bg='#FF8000')
        self.master.resizable(False, False)

        # Variables
        self.username = StringVar()
        self.password_length = IntVar()
        self.generated_password = StringVar()

        # Layout
        self.create_widgets()

    def create_widgets(self):
        Label(self.master, text=":PASSWORD GENERATOR:", fg='darkblue', bg='#FF8000', font='arial 20 bold underline').grid(row=0, column=1, pady=(20, 10))

        Label(self.master, text="Enter User Name: ", font='times 15 bold', bg='#FF8000', fg='darkblue').grid(row=1, column=0, padx=20, pady=10, sticky=E)
        Entry(self.master, textvariable=self.username, font='times 15', bd=6, relief='ridge').grid(row=1, column=1, padx=20, pady=10)

        Label(self.master, text="Enter Password Length: ", font='times 15 bold', bg='#FF8000', fg='darkblue').grid(row=2, column=0, padx=20, pady=10, sticky=E)
        Entry(self.master, textvariable=self.password_length, font='times 15', bd=6, relief='ridge').grid(row=2, column=1, padx=20, pady=10)

        Label(self.master, text="Generated Password: ", font='times 15 bold', bg='#FF8000', fg='darkblue').grid(row=3, column=0, padx=20, pady=10, sticky=E)
        Entry(self.master, textvariable=self.generated_password, font='times 15', bd=6, relief='ridge', fg='#DC143C').grid(row=3, column=1, padx=20, pady=10)

        Button(self.master, text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1, font='Verdana 15 bold', fg='#68228B', bg='#BCEE68', command=self.generate_password).grid(row=4, column=1, pady=10)
        Button(self.master, text="ACCEPT", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.accept_fields).grid(row=5, column=1, pady=10)
        Button(self.master, text="RESET", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.reset_fields).grid(row=6, column=1, pady=10)

    def generate_password(self):
        username = self.username.get()
        length = self.password_length.get()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty")
            return
        if not username.isalpha():
            messagebox.showerror("Error", "Username must only contain letters")
            return
        if length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return

        characters = string.ascii_letters + string.digits + "@#%&()\"?!"
        password = ''.join(random.choice(characters) for _ in range(length))
        self.generated_password.set(password)

    def accept_fields(self):
        username = self.username.get()
        password = self.generated_password.get()

        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE Username = ?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "This username already exists! Please use another username.")
            else:
                cursor.execute("INSERT INTO users (Username, GeneratedPassword) VALUES (?, ?)", (username, password))
                db.commit()
                messagebox.showinfo("Success", "Password generated and saved successfully")

    def reset_fields(self):
        self.username.set("")
        self.password_length.set(0)
        self.generated_password.set("")

# Main function to run the application
if __name__ == '__main__':
    init_db()
    root = Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()
