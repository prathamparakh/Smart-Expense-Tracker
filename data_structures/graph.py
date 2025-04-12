class Graph:
    """
    Implements a graph using adjacency list to model spending patterns
    """
    
    def __init__(self):
        """
        Initialize an empty adjacency list
        """
        self.adjacency_list = {}
    
    def add_edge(self, from_node, to_node, weight):
        """
        Add an edge to the graph
        
        Args:
            from_node: Source vertex (category)
            to_node: Destination vertex (category)
            weight: Edge weight (transaction amount)
        """
        if from_node not in self.adjacency_list:
            self.adjacency_list[from_node] = []
        
        self.adjacency_list[from_node].append((to_node, weight))
    
    def get_connections(self, node):
        """
        Get all connected vertices from a node
        
        Args:
            node: Source node
            
        Returns:
            list: Connected nodes with weights
        """
        if node in self.adjacency_list:
            return self.adjacency_list[node]
        return []
    
    def find_frequent_patterns(self, min_support):
        """
        Find frequent spending patterns in the graph
        
        Args:
            min_support: Minimum frequency to consider a pattern frequent
            
        Returns:
            list: List of frequent patterns
        """
        pattern_count = {}
        
        # Count occurrences of each pattern (sequence of transactions)
        for node, edges in self.adjacency_list.items():
            for to_node, _ in edges:
                pattern = f"{node} -> {to_node}"
                pattern_count[pattern] = pattern_count.get(pattern, 0) + 1
        
        # Filter patterns that meet minimum support threshold
        frequent_patterns = []
        for pattern, count in pattern_count.items():
            if count >= min_support:
                frequent_patterns.append(pattern)
        
        return frequent_patterns
    
    def visualize_spending_behavior(self):
        """
        Display a text visualization of the spending behavior
        """
        print("\n===== SPENDING BEHAVIOR GRAPH =====")
        for node, edges in self.adjacency_list.items():
            print(f"Category: {node}")
            for to_node, weight in edges:
                print(f"  --> {to_node} (${weight:.2f})")
        print("===================================")