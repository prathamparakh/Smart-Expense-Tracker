class Transaction:
    """
    Represents a single expense transaction
    """
    
    def __init__(self, id, desc, cat, amt, dt, loc):
        """
        Construct a new Transaction object
        
        Args:
            id: Unique identifier for the transaction
            desc: Description of the transaction
            cat: Category of the expense
            amt: Amount spent
            dt: Date of the transaction
            loc: Location where transaction occurred
        """
        self.id = id
        self.description = desc
        self.category = cat
        self.amount = amt
        self.date = dt
        self.location = loc
        self.is_flagged = False
        self.unusual_score = 0.0
        
    def display(self):
        """
        Display the transaction details
        """
        print(f"{self.id:<5}{self.description:<25}{self.category:<15}${self.amount:<10.2f}{self.date:<15}{self.location:<20}", end="")
        
        if self.is_flagged:
            print(f" [FLAGGED: Unusual Score = {self.unusual_score}]")
        else:
            print()