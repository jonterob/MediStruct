# Graph for Department Routing (Shortest path)
class HospitalGraph:
    def __init__(self):
        # Departments as nodes
        self.departments = {
            "Reception": {"Emergency": 1, "Pharmacy": 2, "Laboratory": 3},
            "Emergency": {"Reception": 1, "ICU": 1, "Radiology": 2},
            "ICU": {"Emergency": 1, "Surgery": 1},
            "Surgery": {"ICU": 1, "Ward": 1, "Reception": 3},
            "Ward": {"Surgery": 1, "Pharmacy": 1, "Reception": 2},
            "Pharmacy": {"Reception": 2, "Ward": 1, "Reception": 2},
            "Laboratory": {"Reception": 3, "Radiology": 1},
            "Radiology": {"Emergency": 2, "Laboratory": 1, "Reception": 2}
        }
    
    def shortest_path(self, start, end):
        """Find shortest path using Dijkstra's algorithm"""
        if start not in self.departments or end not in self.departments:
            return None, float('inf')
        
        distances = {dept: float('inf') for dept in self.departments}
        distances[start] = 0
        previous = {dept: None for dept in self.departments}
        unvisited = set(self.departments.keys())
        
        while unvisited:
            # Find unvisited node with smallest distance
            current = min(unvisited, key=lambda dept: distances[dept])
            
            if distances[current] == float('inf'):
                break
            
            unvisited.remove(current)
            
            if current == end:
                break
            
            # Check neighbors
            for neighbor, weight in self.departments.get(current, {}).items():
                if neighbor in unvisited:
                    new_distance = distances[current] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current
        
        # Reconstruct path
        if distances[end] == float('inf'):
            return None, float('inf')
        
        path = []
        current = end
        while current is not None:
            path.insert(0, current)
            current = previous[current]
        
        return path, distances[end]
    
    def get_all_departments(self):
        return list(self.departments.keys())
    
    def get_neighbors(self, department):
        return self.departments.get(department, {})