import heapq
from models.transaction import Transaction
from models.user import User

class FraudDetector:
    """
    Detects unusual spending patterns using priority queue
    """
    
    def __init__(self):
        # Use a list for the priority queue
        self.unusual_transactions = []
    
    def detect_unusual_transactions(self, user):
        """
        Detect unusual transactions for a user
        
        Args:
            user: User whose transactions to analyze
        """
        # Clear previous results
        self.unusual_transactions = []
        
        for tx in user.transactions:
            # Reset flag
            tx.is_flagged = False
            tx.unusual_score = 0.0
            
            # Calculate score based on average spending in category
            avg_spending = user.get_average_spending(tx.category)
            
            # Simple scoring: how much higher than average
            if avg_spending > 0:
                tx.unusual_score = tx.amount / avg_spending - 1.0
                
                # Location-based bonus
                if tx.location != "Local" and tx.location != "Online":
                    tx.unusual_score += 0.3
                
                # Flag if unusual
                if tx.unusual_score > 0.7:
                    tx.is_flagged = True
                    # Use negative unusual_score for max-heap behavior in a min-heap
                    heapq.heappush(self.unusual_transactions, (-tx.unusual_score, tx))
    
    def get_top_unusual_transactions(self, limit):
        """
        Get the top unusual transactions
        
        Args:
            limit: Maximum number of transactions to return
            
        Returns:
            list: Top unusual transactions
        """
        result = []
        
        # Create a copy of the heap
        temp = self.unusual_transactions.copy()
        
        # Extract the top transactions to the result list
        count = 0
        while temp and count < limit:
            # Extract transaction and ignore the negative score we used for sorting
            _, tx = heapq.heappop(temp)
            result.append(tx)
            count += 1
        
        return result