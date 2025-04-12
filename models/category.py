class Category:
    """
    Represents a spending category with budget limits
    """
    
    def __init__(self, name="", limit=0.0):
        """
        Construct a new Category object
        
        Args:
            name: Name of the category
            limit: Budget limit for the category
        """
        self.name = name
        self.budget_limit = limit
        self.spent = 0.0
    
    def is_over_budget(self):
        """
        Check if spending has exceeded the budget limit
        
        Returns:
            bool: True if over budget, False otherwise
        """
        return self.spent > self.budget_limit
    
    def get_budget_percentage(self):
        """
        Calculate what percentage of the budget has been spent
        
        Returns:
            float: Percentage of budget used
        """
        if self.budget_limit == 0:
            return 0
        return (self.spent / self.budget_limit) * 100.0
    
    def display(self):
        """
        Display the category details
        """
        output = f"{self.name:<15}${self.budget_limit:<10.2f}${self.spent:<10.2f}{self.get_budget_percentage():<10.2f}% "
        
        if self.is_over_budget():
            output += "[OVER BUDGET]"
            
        print(output)