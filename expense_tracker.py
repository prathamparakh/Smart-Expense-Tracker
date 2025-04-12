from models.user import User
from models.transaction import Transaction
from algorithms.budget_planner import BudgetPlanner
from algorithms.fraud_detector import FraudDetector
from data_structures.trie import Trie
from data_structures.graph import Graph
import random

class ExpenseTracker:
    """
    Main class that integrates all components of the expense tracker
    """
    
    def __init__(self):
        """
        Construct a new ExpenseTracker object
        """
        # Create a sample user
        self.current_user = User(1, "John Doe", 2000.0)
        
        self.budget_planner = BudgetPlanner()
        self.fraud_detector = FraudDetector()
        self.transaction_trie = Trie()
        self.spending_graph = Graph()
        
        # Initialize with sample data
        self.generate_sample_data()
    
    def generate_sample_data(self):
        """
        Generate sample transaction data for demonstration
        """
        categories = ["Food", "Housing", "Transportation", "Entertainment", "Utilities"]
        descriptions = [
            "Grocery Store", "Restaurant", "Rent", "Gas", "Electric Bill", 
            "Movie Tickets", "Bus Fare", "Internet Bill", "Coffee Shop"
        ]
        locations = ["Local", "Online", "Nearby City", "Foreign Country"]
        
        # Create 20 sample transactions
        for i in range(20):
            # Randomly select category, description, amount
            category = categories[i % len(categories)]
            description = descriptions[i % len(descriptions)]
            amount = 20.0 + (i * 5.0)  # Simple amount generation
            
            # Format date (YYYY-MM-DD)
            day = (i % 28) + 1
            date = f"2023-05-{day:02d}"
            
            location = locations[i % len(locations)]
            
            # Create transaction
            tx = Transaction(i + 1, description, category, amount, date, location)
            
            # Add occasional unusual transactions
            if i % 5 == 0:
                tx.amount *= 3  # Make some amounts unusually large
            
            # Add to user
            self.current_user.add_transaction(tx)
            
            # Add to trie
            self.transaction_trie.insert(description, self.current_user.transactions[-1])
            self.transaction_trie.insert(category, self.current_user.transactions[-1])
            
            # Add to spending graph (if not first transaction)
            if i > 0:
                previous_category = self.current_user.transactions[i - 1].category
                self.spending_graph.add_edge(previous_category, category, amount)
    
    def run(self):
        """
        Run the main application loop
        """
        choice = None
        while choice != 0:
            print("\n===== SMART PERSONAL EXPENSE TRACKER =====")
            print("1. View All Transactions")
            print("2. View Budget Summary")
            print("3. Detect Unusual Transactions")
            print("4. Search Transactions")
            print("5. Get Budget Recommendations")
            print("0. Exit")
            
            try:
                choice = int(input("Choice: "))
                
                if choice == 1:
                    self.view_all_transactions()
                elif choice == 2:
                    self.current_user.display_budget_summary()
                elif choice == 3:
                    self.detect_unusual_transactions()
                elif choice == 4:
                    self.search_transactions()
                elif choice == 5:
                    self.get_budget_recommendations()
                elif choice == 0:
                    print("Exiting program. Goodbye!")
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
    
    def view_all_transactions(self):
        """
        Display all transactions
        """
        print("\n===== ALL TRANSACTIONS =====")
        print(f"{'ID':<5}{'Description':<25}{'Category':<15}{'Amount':<11}{'Date':<15}{'Location':<20}")
        print("-" * 91)
        
        for tx in self.current_user.transactions:
            tx.display()
    
    def detect_unusual_transactions(self):
        """
        Detect and display unusual transactions
        """
        # Run fraud detection algorithm
        self.fraud_detector.detect_unusual_transactions(self.current_user)
        
        # Get top unusual transactions
        unusual_txs = self.fraud_detector.get_top_unusual_transactions(5)
        
        print("\n===== UNUSUAL TRANSACTIONS DETECTED =====")
        if not unusual_txs:
            print("No unusual transactions detected.")
            return
        
        print(f"{'ID':<5}{'Description':<25}{'Category':<15}{'Amount':<11}{'Date':<15}{'Location':<20}{'Unusual Score'}")
        print("-" * 110)
        
        for tx in unusual_txs:
            tx.display()
    
    def search_transactions(self):
        """
        Search transactions by keyword
        """
        keyword = input("\nEnter search keyword: ")
        
        # Search using Trie
        results = self.transaction_trie.search(keyword)
        
        print(f"\n===== SEARCH RESULTS FOR '{keyword}' =====")
        if not results:
            print("No transactions found.")
            return
        
        print(f"{'ID':<5}{'Description':<25}{'Category':<15}{'Amount':<11}{'Date':<15}{'Location':<20}")
        print("-" * 91)
        
        for tx in results:
            tx.display()
    
    def get_budget_recommendations(self):
        """
        Get budget recommendations
        """
        print("\n===== BUDGET RECOMMENDATIONS =====")
        
        # Get daily spending recommendation (greedy approach)
        days_left = 30 - (len(self.current_user.transactions) // 3)  # Simplified calculation
        daily_recommendation = self.budget_planner.suggest_daily_spending(self.current_user, days_left)
        
        print(f"Recommended daily spending: ${daily_recommendation:.2f}")
        
        # Analyze spending by periods using Divide and Conquer
        period_totals = self.budget_planner.analyze_spending_by_period(self.current_user.transactions)
        
        print("\nWeekly Spending Analysis:")
        for period, total in period_totals.items():
            print(f"{period}: ${total:.2f}")
        
        # Get over-budget categories
        over_budget_categories = self.current_user.get_over_budget_categories()
        
        if over_budget_categories:
            print("\nCategories Over Budget:")
            for category in over_budget_categories:
                print(f"- {category.name}: ${category.spent:.2f} (Budget: ${category.budget_limit:.2f})")