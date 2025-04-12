class TrieNode:
    """
    Represents a node in the Trie data structure
    """
    
    def __init__(self):
        """
        Construct a new TrieNode object
        """
        self.children = {}
        self.is_end_of_word = False
        self.transactions = []

class Trie:
    """
    Implements a Trie data structure for fast text-based search
    """
    
    def __init__(self):
        """
        Construct a new Trie object
        """
        self.root = TrieNode()
    
    def insert(self, word, transaction):
        """
        Insert a word into the trie with associated transaction
        
        Args:
            word: Word to insert
            transaction: Associated transaction
        """
        current = self.root
        
        for c in word:
            if c not in current.children:
                current.children[c] = TrieNode()
            current = current.children[c]
        
        current.is_end_of_word = True
        current.transactions.append(transaction)
    
    def search(self, prefix):
        """
        Search for transactions matching a prefix
        
        Args:
            prefix: Prefix to search for
            
        Returns:
            list: Matching transactions
        """
        current = self.root
        results = []
        
        # Navigate to the node corresponding to the prefix
        for c in prefix:
            if c not in current.children:
                return results  # Prefix not found
            current = current.children[c]
        
        # Collect all transactions under this prefix using DFS
        self._collect_transactions(current, results)
        return results
    
    def _collect_transactions(self, node, results):
        """
        Helper method to collect all transactions under a node
        
        Args:
            node: The current node
            results: List to store the results
        """
        if node is None:
            return
        
        if node.is_end_of_word:
            results.extend(node.transactions)
        
        for child in node.children.values():
            self._collect_transactions(child, results)