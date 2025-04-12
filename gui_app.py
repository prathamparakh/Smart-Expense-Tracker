import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
import os
from models.transaction import Transaction
# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the expense tracker components
from expense_tracker import ExpenseTracker

class ExpenseTrackerGUI:
    def __init__(self, root, username=None):
        self.root = root
        self.root.title("Smart Personal Expense Tracker")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")

        # Create the expense tracker backend
        self.tracker = ExpenseTracker()
        
        # Update current user's name if username is provided
        if username:
            self.tracker.current_user.name = username

        # Create the main frame
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create header
        self.header_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.header_frame.pack(fill=tk.X, pady=(0, 20))

        self.title_label = tk.Label(
            self.header_frame, 
            text="SMART PERSONAL EXPENSE TRACKER", 
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        self.title_label.pack(side=tk.LEFT)

        # Create budget summary frame
        self.summary_frame = tk.Frame(self.main_frame, bg="#ffffff", relief=tk.RIDGE, bd=2)
        self.summary_frame.pack(fill=tk.X, pady=(0, 20))

        self.user_name = tk.Label(
            self.summary_frame,
            text=f"User: {self.tracker.current_user.name}",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            fg="#333333",
            padx=10,
            pady=10
        )
        self.user_name.grid(row=0, column=0, sticky=tk.W)

        self.total_budget = tk.Label(
            self.summary_frame,
            text=f"Total Budget: ${self.tracker.current_user.total_budget:.2f}",
            font=("Arial", 12),
            bg="#ffffff",
            padx=10,
            pady=5
        )
        self.total_budget.grid(row=1, column=0, sticky=tk.W)

        self.total_spent = tk.Label(
            self.summary_frame,
            text=f"Total Spent: ${self.tracker.current_user.get_total_spent():.2f}",
            font=("Arial", 12),
            bg="#ffffff",
            padx=10,
            pady=5
        )
        self.total_spent.grid(row=2, column=0, sticky=tk.W)

        self.remaining_budget = tk.Label(
            self.summary_frame,
            text=f"Remaining Budget: ${self.tracker.current_user.get_remaining_budget():.2f}",
            font=("Arial", 12),
            bg="#ffffff",
            padx=10,
            pady=5
        )
        self.remaining_budget.grid(row=3, column=0, sticky=tk.W)

        # Add logout button
        self.logout_btn = tk.Button(
            self.summary_frame,
            text="Logout",
            command=self.logout,
            font=("Arial", 10),
            bg="#f44336",
            fg="white",
            padx=10,
            pady=5
        )
        self.logout_btn.grid(row=0, column=1, sticky=tk.E, padx=10)

        # Create buttons frame
        self.button_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.button_frame.pack(fill=tk.X, pady=(0, 20))

        button_style = {
            "font": ("Arial", 11),
            "bg": "#4CAF50",
            "fg": "white",
            "padx": 15,
            "pady": 8,
            "width": 25,
            "relief": tk.RAISED,
            "bd": 1
        }

        self.view_btn = tk.Button(
            self.button_frame,
            text="View All Transactions",
            command=self.view_all_transactions,
            **button_style
        )
        self.view_btn.grid(row=0, column=0, padx=5, pady=5)

        self.budget_btn = tk.Button(
            self.button_frame,
            text="View Budget Summary",
            command=self.view_budget_summary,
            **button_style
        )
        self.budget_btn.grid(row=0, column=1, padx=5, pady=5)

        self.unusual_btn = tk.Button(
            self.button_frame,
            text="Detect Unusual Transactions",
            command=self.detect_unusual_transactions,
            **button_style
        )
        self.unusual_btn.grid(row=1, column=0, padx=5, pady=5)

        self.search_btn = tk.Button(
            self.button_frame,
            text="Search Transactions",
            command=self.search_transactions,
            **button_style
        )
        self.search_btn.grid(row=1, column=1, padx=5, pady=5)

        self.recommend_btn = tk.Button(
            self.button_frame,
            text="Get Budget Recommendations",
            command=self.get_budget_recommendations,
            **button_style
        )
        self.recommend_btn.grid(row=2, column=0, padx=5, pady=5)

        self.add_btn = tk.Button(
            self.button_frame,
            text="Add New Transaction",
            command=self.add_transaction,
            **button_style
        )
        self.add_btn.grid(row=2, column=1, padx=5, pady=5)

        # Create the display frame for transaction data
        self.display_frame = tk.Frame(self.main_frame, bg="#ffffff", relief=tk.RIDGE, bd=2)
        self.display_frame.pack(fill=tk.BOTH, expand=True)

        # Create scrollable treeview for transactions
        self.tree_frame = tk.Frame(self.display_frame)
        self.tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree_scroll = tk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.transaction_tree = ttk.Treeview(
            self.tree_frame, 
            columns=("ID", "Description", "Category", "Amount", "Date", "Location"),
            show="headings",
            yscrollcommand=self.tree_scroll.set
        )
        
        # Define column headings
        self.transaction_tree.heading("ID", text="ID")
        self.transaction_tree.heading("Description", text="Description")
        self.transaction_tree.heading("Category", text="Category")
        self.transaction_tree.heading("Amount", text="Amount")
        self.transaction_tree.heading("Date", text="Date")
        self.transaction_tree.heading("Location", text="Location")
        
        # Define column widths
        self.transaction_tree.column("ID", width=50)
        self.transaction_tree.column("Description", width=200)
        self.transaction_tree.column("Category", width=150)
        self.transaction_tree.column("Amount", width=100)
        self.transaction_tree.column("Date", width=100)
        self.transaction_tree.column("Location", width=150)
        
        self.transaction_tree.pack(fill=tk.BOTH, expand=True)
        self.tree_scroll.config(command=self.transaction_tree.yview)
        
        # Set a custom style
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        style.configure("Treeview", font=('Arial', 10), rowheight=25)

        # Status bar
        self.status_bar = tk.Label(
            root, 
            text="Ready", 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            font=("Arial", 10),
            bg="#f0f0f0"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Initially load all transactions
        self.view_all_transactions()

    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            # Clear current root window
            for widget in self.root.winfo_children():
                widget.destroy()
                
            # Import and create login window
            from login import LoginWindow
            
            def on_login_success(username):
                # Clear login widgets
                for widget in self.root.winfo_children():
                    widget.destroy()
                
                # Start the main application again
                app = ExpenseTrackerGUI(self.root, username)
                self.root.title(f"Smart Personal Expense Tracker - {username}")
                
            # Show login window
            login_window = LoginWindow(self.root, on_login_success)

    def update_budget_summary(self):
        """Update the budget summary labels"""
        self.total_spent.config(text=f"Total Spent: ${self.tracker.current_user.get_total_spent():.2f}")
        self.remaining_budget.config(text=f"Remaining Budget: ${self.tracker.current_user.get_remaining_budget():.2f}")

    def clear_tree(self):
        """Clear all items from the treeview"""
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)

    def view_all_transactions(self):
        """Display all transactions in the treeview"""
        self.clear_tree()
        self.status_bar.config(text="Viewing all transactions")
        
        for tx in self.tracker.current_user.transactions:
            self.transaction_tree.insert(
                "", 
                "end", 
                values=(
                    tx.id, 
                    tx.description, 
                    tx.category, 
                    f"${tx.amount:.2f}", 
                    tx.date, 
                    tx.location
                )
            )

    def view_budget_summary(self):
        """Display the budget summary in a new window"""
        budget_window = tk.Toplevel(self.root)
        budget_window.title("Budget Summary")
        budget_window.geometry("600x500")
        budget_window.configure(bg="#ffffff")
        
        # Header
        header = tk.Label(
            budget_window,
            text=f"BUDGET SUMMARY FOR {self.tracker.current_user.name}",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Budget info
        info_frame = tk.Frame(budget_window, bg="#ffffff")
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            info_frame,
            text=f"Total Budget: ${self.tracker.current_user.total_budget:.2f}",
            font=("Arial", 12),
            bg="#ffffff",
            anchor=tk.W
        ).pack(fill=tk.X, pady=2)
        
        tk.Label(
            info_frame,
            text=f"Total Spent: ${self.tracker.current_user.get_total_spent():.2f}",
            font=("Arial", 12),
            bg="#ffffff",
            anchor=tk.W
        ).pack(fill=tk.X, pady=2)
        
        tk.Label(
            info_frame,
            text=f"Remaining Budget: ${self.tracker.current_user.get_remaining_budget():.2f}",
            font=("Arial", 12),
            bg="#ffffff",
            anchor=tk.W
        ).pack(fill=tk.X, pady=2)
        
        # Category breakdown
        cat_label = tk.Label(
            budget_window,
            text="CATEGORY BREAKDOWN",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            pady=10
        )
        cat_label.pack(fill=tk.X)
        
        # Category treeview
        cat_frame = tk.Frame(budget_window, bg="#ffffff")
        cat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        cat_tree = ttk.Treeview(
            cat_frame,
            columns=("Category", "Budget", "Spent", "Percentage", "Status"),
            show="headings"
        )
        
        cat_tree.heading("Category", text="Category")
        cat_tree.heading("Budget", text="Budget")
        cat_tree.heading("Spent", text="Spent")
        cat_tree.heading("Percentage", text="Percentage")
        cat_tree.heading("Status", text="Status")
        
        cat_tree.column("Category", width=150)
        cat_tree.column("Budget", width=100)
        cat_tree.column("Spent", width=100)
        cat_tree.column("Percentage", width=100)
        cat_tree.column("Status", width=100)
        
        cat_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add category data
        for name, category in self.tracker.current_user.categories.items():
            status = "OVER BUDGET" if category.is_over_budget() else ""
            cat_tree.insert(
                "",
                "end",
                values=(
                    category.name,
                    f"${category.budget_limit:.2f}",
                    f"${category.spent:.2f}",
                    f"{category.get_budget_percentage():.2f}%",
                    status
                )
            )
            
        self.status_bar.config(text="Viewed budget summary")

    def detect_unusual_transactions(self):
        """Run fraud detection and display unusual transactions"""
        self.clear_tree()
        self.status_bar.config(text="Detecting unusual transactions...")
        
        # Run fraud detection
        self.tracker.fraud_detector.detect_unusual_transactions(self.tracker.current_user)
        unusual_txs = self.tracker.fraud_detector.get_top_unusual_transactions(5)
        
        if not unusual_txs:
            messagebox.showinfo("Unusual Transactions", "No unusual transactions detected.")
            self.view_all_transactions()
            return
        
        # Display unusual transactions
        for tx in unusual_txs:
            self.transaction_tree.insert(
                "",
                "end",
                values=(
                    tx.id,
                    tx.description,
                    tx.category,
                    f"${tx.amount:.2f}",
                    tx.date,
                    tx.location
                ),
                tags=("unusual",)
            )
            
        # Configure tag for red text
        self.transaction_tree.tag_configure("unusual", foreground="red")
        self.status_bar.config(text=f"Found {len(unusual_txs)} unusual transactions")

    def search_transactions(self):
        """Search transactions by keyword"""
        keyword = simpledialog.askstring("Search", "Enter search keyword:")
        if not keyword:
            return
            
        self.clear_tree()
        self.status_bar.config(text=f"Searching for '{keyword}'...")
        
        # Search using Trie
        results = self.tracker.transaction_trie.search(keyword)
        
        if not results:
            messagebox.showinfo("Search Results", f"No transactions found for '{keyword}'.")
            self.view_all_transactions()
            return
            
        # Display results
        for tx in results:
            self.transaction_tree.insert(
                "",
                "end",
                values=(
                    tx.id,
                    tx.description,
                    tx.category,
                    f"${tx.amount:.2f}",
                    tx.date,
                    tx.location
                ),
                tags=("search_result",)
            )
            
        # Configure tag for blue text
        self.transaction_tree.tag_configure("search_result", foreground="blue")
        self.status_bar.config(text=f"Found {len(results)} matching transactions for '{keyword}'")

    def get_budget_recommendations(self):
        """Display budget recommendations in a new window"""
        rec_window = tk.Toplevel(self.root)
        rec_window.title("Budget Recommendations")
        rec_window.geometry("600x500")
        rec_window.configure(bg="#ffffff")
        
        # Header
        header = tk.Label(
            rec_window,
            text="BUDGET RECOMMENDATIONS",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Daily spending recommendation
        info_frame = tk.Frame(rec_window, bg="#ffffff")
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        days_left = 30 - (len(self.tracker.current_user.transactions) // 3)
        daily_rec = self.tracker.budget_planner.suggest_daily_spending(self.tracker.current_user, days_left)
        
        tk.Label(
            info_frame,
            text=f"Recommended daily spending: ${daily_rec:.2f}",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            anchor=tk.W
        ).pack(fill=tk.X, pady=5)
        
        # Weekly spending analysis
        period_label = tk.Label(
            rec_window,
            text="WEEKLY SPENDING ANALYSIS",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            pady=10
        )
        period_label.pack(fill=tk.X)
        
        period_frame = tk.Frame(rec_window, bg="#ffffff")
        period_frame.pack(fill=tk.X, padx=20, pady=10)
        
        period_tree = ttk.Treeview(
            period_frame,
            columns=("Period", "Amount"),
            show="headings",
            height=5
        )
        
        period_tree.heading("Period", text="Period")
        period_tree.heading("Amount", text="Amount")
        
        period_tree.column("Period", width=150)
        period_tree.column("Amount", width=150)
        
        period_tree.pack(fill=tk.X)
        
        # Add period data
        period_totals = self.tracker.budget_planner.analyze_spending_by_period(self.tracker.current_user.transactions)
        for period, total in period_totals.items():
            period_tree.insert(
                "",
                "end",
                values=(period, f"${total:.2f}")
            )
            
        # Over-budget categories
        over_label = tk.Label(
            rec_window,
            text="CATEGORIES OVER BUDGET",
            font=("Arial", 12, "bold"),
            bg="#ffffff",
            pady=10
        )
        over_label.pack(fill=tk.X)
        
        over_frame = tk.Frame(rec_window, bg="#ffffff")
        over_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        over_tree = ttk.Treeview(
            over_frame,
            columns=("Category", "Spent", "Budget"),
            show="headings"
        )
        
        over_tree.heading("Category", text="Category")
        over_tree.heading("Spent", text="Spent")
        over_tree.heading("Budget", text="Budget")
        
        over_tree.column("Category", width=150)
        over_tree.column("Spent", width=150)
        over_tree.column("Budget", width=150)
        
        over_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add over-budget category data
        over_budget = self.tracker.current_user.get_over_budget_categories()
        if over_budget:
            for cat in over_budget:
                over_tree.insert(
                    "",
                    "end",
                    values=(
                        cat.name,
                        f"${cat.spent:.2f}",
                        f"${cat.budget_limit:.2f}"
                    ),
                    tags=("over_budget",)
                )
            over_tree.tag_configure("over_budget", foreground="red")
        else:
            tk.Label(
                over_frame,
                text="No categories are currently over budget",
                font=("Arial", 11),
                bg="#ffffff"
            ).pack(pady=10)
            
        self.status_bar.config(text="Viewed budget recommendations")

    def add_transaction(self):
        """Add a new transaction"""
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Transaction")
        add_window.geometry("400x400")
        add_window.configure(bg="#ffffff")
        
        # Header
        header = tk.Label(
            add_window,
            text="ADD NEW TRANSACTION",
            font=("Arial", 14, "bold"),
            bg="#ffffff",
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Form frame
        form_frame = tk.Frame(add_window, bg="#ffffff")
        form_frame.pack(fill=tk.BOTH, padx=20, pady=10)
        
        # Description
        tk.Label(
            form_frame,
            text="Description:",
            font=("Arial", 11),
            bg="#ffffff",
            anchor=tk.W
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        desc_entry = tk.Entry(form_frame, width=30)
        desc_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Category
        tk.Label(
            form_frame,
            text="Category:",
            font=("Arial", 11),
            bg="#ffffff",
            anchor=tk.W
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        # Get existing categories
        categories = list(self.tracker.current_user.categories.keys())
        cat_combo = ttk.Combobox(form_frame, values=categories, width=27)
        cat_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Amount
        tk.Label(
            form_frame,
            text="Amount ($):",
            font=("Arial", 11),
            bg="#ffffff",
            anchor=tk.W
        ).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        amount_entry = tk.Entry(form_frame, width=30)
        amount_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Date
        tk.Label(
            form_frame,
            text="Date (YYYY-MM-DD):",
            font=("Arial", 11),
            bg="#ffffff",
            anchor=tk.W
        ).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        date_entry = tk.Entry(form_frame, width=30)
        date_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Location
        tk.Label(
            form_frame,
            text="Location:",
            font=("Arial", 11),
            bg="#ffffff",
            anchor=tk.W
        ).grid(row=4, column=0, sticky=tk.W, pady=5)
        
        locations = ["Local", "Online", "Nearby City", "Foreign Country"]
        loc_combo = ttk.Combobox(form_frame, values=locations, width=27)
        loc_combo.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(add_window, bg="#ffffff")
        btn_frame.pack(fill=tk.X, padx=20, pady=20)
        
        def save_transaction():
            """Save the new transaction"""
            try:
                description = desc_entry.get()
                category = cat_combo.get()
                amount = float(amount_entry.get())
                date = date_entry.get()
                location = loc_combo.get()
                
                # Validate inputs
                if not description or not category or not date or not location:
                    messagebox.showerror("Input Error", "All fields are required")
                    return
                    
                # Create new transaction with the next ID
                next_id = len(self.tracker.current_user.transactions) + 1
                tx = Transaction(next_id, description, category, amount, date, location)
                
                # Add to the tracker
                self.tracker.current_user.add_transaction(tx)
                
                # Add to trie for searching
                self.tracker.transaction_trie.insert(description, tx)
                self.tracker.transaction_trie.insert(category, tx)
                
                # Add to spending graph if not first transaction
                if len(self.tracker.current_user.transactions) > 1:
                    prev_tx = self.tracker.current_user.transactions[-2]
                    self.tracker.spending_graph.add_edge(prev_tx.category, category, amount)
                
                # Update UI
                self.update_budget_summary()
                self.view_all_transactions()
                
                # Show confirmation
                messagebox.showinfo("Success", "Transaction added successfully")
                add_window.destroy()
                
            except ValueError:
                messagebox.showerror("Input Error", "Amount must be a valid number")
        
        save_btn = tk.Button(
            btn_frame,
            text="Save Transaction",
            command=save_transaction,
            font=("Arial", 11),
            bg="#4CAF50",
            fg="white",
            padx=10,
            pady=5
        )
        save_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=add_window.destroy,
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            padx=10,
            pady=5
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)

def main():
    """Main function to start the GUI application"""
    root = tk.Tk()
    app = ExpenseTrackerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()