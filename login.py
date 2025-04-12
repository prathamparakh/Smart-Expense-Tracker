import tkinter as tk
from tkinter import messagebox
import os
import json

class LoginSystem:
    def __init__(self):
        self.users = {
            "admin": "admin123",
            "user": "password"
        }
        self.load_users()
        
    def load_users(self):
        """Load users from a JSON file if it exists"""
        try:
            if os.path.exists("users.json"):
                with open("users.json", "r") as f:
                    self.users = json.load(f)
        except Exception as e:
            print(f"Error loading users: {e}")
    
    def save_users(self):
        """Save users to a JSON file"""
        try:
            with open("users.json", "w") as f:
                json.dump(self.users, f)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def authenticate(self, username, password):
        """Check if username and password match"""
        if username in self.users and self.users[username] == password:
            return True
        return False
    
    def register_user(self, username, password):
        """Register a new user"""
        if username in self.users:
            return False
        self.users[username] = password
        self.save_users()
        return True

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.login_system = LoginSystem()
        self.on_login_success = on_login_success
        
        self.root.title("Login - Expense Tracker")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="EXPENSE TRACKER LOGIN",
            font=("Arial", 16, "bold"),
            bg="#f0f0f0",
            fg="#333333",
            pady=10
        )
        title_label.pack(fill=tk.X)
        
        # Login frame
        login_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.RIDGE, bd=2)
        login_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Username
        tk.Label(
            login_frame,
            text="Username:",
            font=("Arial", 12),
            bg="#ffffff",
            anchor=tk.W,
            pady=5,
            padx=10
        ).pack(fill=tk.X)
        
        self.username_entry = tk.Entry(login_frame, font=("Arial", 12), width=30)
        self.username_entry.pack(padx=10, pady=5)
        
        # Password
        tk.Label(
            login_frame,
            text="Password:",
            font=("Arial", 12),
            bg="#ffffff",
            anchor=tk.W,
            pady=5,
            padx=10
        ).pack(fill=tk.X)
        
        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), width=30, show="*")
        self.password_entry.pack(padx=10, pady=5)
        
        # Buttons
        button_frame = tk.Frame(login_frame, bg="#ffffff")
        button_frame.pack(fill=tk.X, pady=15, padx=10)
        
        login_btn = tk.Button(
            button_frame,
            text="Login",
            command=self.login,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            padx=15,
            pady=5,
            width=10
        )
        login_btn.pack(side=tk.LEFT, padx=5)
        
        register_btn = tk.Button(
            button_frame,
            text="Register",
            command=self.register,
            font=("Arial", 12),
            bg="#2196F3",
            fg="white",
            padx=15,
            pady=5,
            width=10
        )
        register_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = tk.Button(
            button_frame,
            text="Exit",
            command=self.root.destroy,
            font=("Arial", 12),
            bg="#f44336",
            fg="white",
            padx=15,
            pady=5,
            width=10
        )
        exit_btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_bar = tk.Label(
            main_frame, 
            text="Please login to continue", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Login Error", "Username and password are required")
            return
        
        if self.login_system.authenticate(username, password):
            self.status_bar.config(text=f"Login successful! Welcome, {username}")
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            self.on_login_success(username)
        else:
            self.status_bar.config(text="Invalid username or password")
            messagebox.showerror("Login Error", "Invalid username or password")
    
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Registration Error", "Username and password are required")
            return
        
        if len(password) < 6:
            messagebox.showerror("Registration Error", "Password must be at least 6 characters")
            return
        
        if self.login_system.register_user(username, password):
            self.status_bar.config(text=f"User {username} registered successfully")
            messagebox.showinfo("Registration Successful", f"User {username} registered successfully. You may now log in.")
        else:
            self.status_bar.config(text=f"Username {username} already exists")
            messagebox.showerror("Registration Error", f"Username {username} already exists")