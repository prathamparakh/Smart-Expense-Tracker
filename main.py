#!/usr/bin/env python3
"""
Main entry point for the Smart Personal Expense Tracker application
"""
import tkinter as tk
from login import LoginWindow
from gui_app import ExpenseTrackerGUI

def main():
    """
    Main function that starts the expense tracker with login
    """
    print("Starting Smart Personal Expense Tracker...")
    
    root = tk.Tk()
    
    def on_login_success(username): 
        # Close login window
        for widget in root.winfo_children():
            widget.destroy()
        
        # Start the main application
        print(f"User {username} logged in successfully. Starting application...")
        app = ExpenseTrackerGUI(root, username)  # Pass username
        
        # Update window title with username
        root.title(f"Smart Personal Expense Tracker - {username}")
    
    # Start with login window
    login_window = LoginWindow(root, on_login_success)
    
    root.mainloop()

if __name__ == "__main__":
    main()