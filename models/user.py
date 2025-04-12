from models.transaction import Transaction
from models.category import Category

class User:
    """
    Represents a user with transactions and budget information
    """
    
    def __init__(self, id, name, budget):
        """
        Construct a new User object
        
        Args:
            id: Unique identifier for the user
            name: Name of the user
            budget: Total budget amount
        """
        self.id = id
        self.name = name
        self.categories = {}
        self.transactions = []
        self.historical_spending = {}
        self.total_budget = budget
        
        # Initialize default categories with budget distribution
        self.categories["Food"] = Category("Food", budget * 0.3)
        self.categories["Housing"] = Category("Housing", budget * 0.4)
        self.categories["Transportation"] = Category("Transportation", budget * 0.1)
        self.categories["Entertainment"] = Category("Entertainment", budget * 0.1)
        self.categories["Utilities"] = Category("Utilities", budget * 0.05)
        self.categories["Miscellaneous"] = Category("Miscellaneous", budget * 0.05)
    
    def add_transaction(self, transaction):
        """
        Add a transaction to the user's records
        
        Args:
            transaction: Transaction to add
        """
        self.transactions.append(transaction)
        
        # Update category spending
        if transaction.category in self.categories:
            self.categories[transaction.category].spent += transaction.amount
        else:
            # Create new category if it doesn't exist
            self.categories[transaction.category] = Category(transaction.category, self.total_budget * 0.05)
            self.categories[transaction.category].spent = transaction.amount
        
        # Update historical spending
        if transaction.category not in self.historical_spending:
            self.historical_spending[transaction.category] = []
        self.historical_spending[transaction.category].append(transaction.amount)
    
    def get_over_budget_categories(self):
        """
        Get a list of categories that are over budget
        
        Returns:
            list: List of over-budget categories
        """
        over_budget = []
        for category in self.categories.values():
            if category.is_over_budget():
                over_budget.append(category)
        return over_budget
    
    def get_total_spent(self):
        """
        Calculate the total amount spent across all transactions
        
        Returns:
            float: Total amount spent
        """
        return sum(tx.amount for tx in self.transactions)
    
    def get_remaining_budget(self):
        """
        Calculate the remaining budget
        
        Returns:
            float: Remaining budget amount
        """
        return self.total_budget - self.get_total_spent()
    
    def get_average_spending(self, category):
        """
        Calculate the average spending for a specific category
        
        Args:
            category: Name of the category
            
        Returns:
            float: Average spending amount
        """
        if category not in self.historical_spending or not self.historical_spending[category]:
            return 0.0
        
        amounts = self.historical_spending[category]
        return sum(amounts) / len(amounts)
    
    def display_budget_summary(self):
        """
        Display a summary of the user's budget information
        """
        print(f"\n===== BUDGET SUMMARY FOR {self.name} =====")
        print(f"Total Budget: ${self.total_budget:.2f}")
        print(f"Total Spent: ${self.get_total_spent():.2f}")
        print(f"Remaining Budget: ${self.get_remaining_budget():.2f}")
        
        print("\n----- CATEGORY BREAKDOWN -----")
        print(f"{'Category':<15}{'Budget':<11}{'Spent':<11}{'Percentage':<10}")
        print("-" * 47)
        
        for category in self.categories.values():
            category.display()