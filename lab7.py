"""6.009 Lab 7 -- Faster Gift Delivery."""


from graph import Graph

# NO ADDITIONAL IMPORTS ALLOWED!
class GraphFactory:
    """Factory methods for creating instances of `Graph`."""

    def __init__(self, graph_class):
        """Return a new factory that creates instances of `graph_class`."""
        self.graph_class = graph_class

    def from_list(self, adj_list, labels=None):
        """Create and return a new graph instance.

        Use a simple adjacency list as source, where the `labels` dictionary
        maps each node name to its label.

        Parameters:
            `adj_list`: adjacency list representation of a graph
                        (as a list of lists)
            `labels`: dictionary mapping each node name to its label;
                      by default it's None, which means no label should be set
                      for any of the nodes

        Returns:
            new instance of class implementing `Graph`

        adj_list = [[1, 3], [2], [0], []]
        """
        graph = self.graph_class()
        if labels == None:
            for i in range(len(adj_list)):
                graph.add_node(i)
        else:
            for i in range(len(adj_list)):
                graph.add_node(i, labels[i])
        for name in range(len(adj_list)):
            for val in adj_list[name]:
                graph.add_edge(name, val)
        return graph

    def from_dict(self, adj_dict, labels=None):
        """Create and return a new graph instance.

        Use a simple adjacency dictionary as source where the `labels`
        dictionary maps each node name its label.

        Parameters:
            `adj_dict`: adjacency dictionary representation of a graph
            `labels`: dictionary mapping each node name to its label;
                      by default it's None, which means no label should be set
                      for any of the nodes

        Returns:
            new instance of class implementing `Graph`

        """
        graph = self.graph_class()
        if labels == None:
            for key in adj_dict:
                graph.add_node(key)
        else:
            for key in adj_dict:
                graph.add_node(key, labels[key])
        for name in adj_dict:
            for val in adj_dict[name]:
                graph.add_edge(name, val)
        return graph


class FastGraph(Graph):
    """Faster implementation of `Graph`.

    Has extra optimizations for star and clique patterns.
    """

    def __init__(self):
        self.labels = {}
        self.graph = {}
        self.clique_size = {1: set()}
        #Name to cliques, where cliques are represented as a set of frozen sets
        self.cliques = {}


    def query(self, pattern):
        #This verifies if the current path is correct.
        def verify_path(match):
            for i in range(len(match)-1):
                node = match[i]
                edges = pattern[i][1]
                for edge in edges:
                    try:
                        if match[edge] not in self.graph[node]:
                            return False
                    except:
                        continue
            else:
                return True

        final = []
        out_degree = len(pattern) - 1
        #Creates matches similar to how it was done in lab 6, however the
        #current pattern is checked before each recursive call.
        def query_helper(pattern, temp):
            if len(pattern) == 1:
                for node in self.graph:
                    if pattern[0][0] == '*' or self.labels[node] == pattern[0][0]:
                        if node not in temp:
                            for i in pattern[len(pattern)-1][1]:
                                if temp[i] not in self.graph[node]:
                                    break
                            else:
                                final.append(temp + [node])
            else:
                for node in self.graph:
                    if pattern[0][0] == '*' or self.labels[node] == pattern[0][0]:
                        if node not in temp:
                            # if len(self.graph[node]) >= out_degree and len(pattern[0][1]) == out_degree:
                            temp.append(node)
                            if verify_path(temp):
                                query_helper(pattern[1:], temp)
                            temp.pop()

        #Does the Cliques:
        def clique_pattern(pattern, temp, nodes):
            if len(pattern) == 1:
                for node in nodes:
                    if node not in temp:
                        if pattern[0][0] == '*' or self.labels[node] == pattern[0][0]:
                            final.append(temp + [node])
            else:
                for node in nodes:
                    if node not in temp:
                        if pattern[0][0] == '*' or self.labels[node] == pattern[0][0]:
                            temp.append(node)
                            clique_pattern(pattern[1:], temp, nodes)
                            temp.pop()
        # Checks for a clique
        def clique_checker(pattern):
            clique = 0
            for i in range(len(pattern)):
                if len(pattern[i][1]) == len(pattern) - 1:
                    clique += 1
            if clique == len(pattern):
                return True
            return False

        if clique_checker(pattern):
            print(self.clique_size)
            if len(pattern) in self.clique_size:
                clique_set = self.clique_size[len(pattern)]
            else:
                clique_set = set()
            final = []
            print(clique_set)
            for clique in clique_set:
                clique_pattern(pattern, [], clique)
            return final

        def star_pattern(pattern, temp, nodes):
            if len(pattern) == 1:
                for node in nodes:
                    if node not in temp:
                        if pattern[0][0] == '*' or self.labels[node] == pattern[0][0]:
                            final.append(temp + [node])
            else:
                for node in nodes:
                    if node not in temp:
                        if pattern[0][0] == '*' or self.labels[node] == pattern[0][0]:
                            temp.append(node)
                            star_pattern(pattern[1:], temp, nodes)
                            temp.pop()

        def verify_path_stars(start, current):
            start_neighbors = self.graph[start]
            if current == start:
                return True
            if current not in start_neighbors:
                return False
            return True

        def check_outdegree(pattern):
            out_degree = len(pattern) - 1
            if out_degree < 5:
                return False
            count = 0
            for tup in pattern:
                if len(tup[1]) > 0:
                    count += 1
                    if count == 2:
                        return False
            return True
        #For the case with stars
        y_n_star = check_outdegree(pattern)
        if y_n_star:
            for i in range(len(pattern)):
                if len(pattern[i][1]) == len(pattern) - 1:
                    index = i
                    new = pattern[0]
                    break
            start_nodes = []
            for node in self.graph:
                if len(self.graph[node]) >= len(pattern) - 1:
                    start_nodes.append(node)
            pattern[0] = pattern[i]
            pattern[i] = new
            start = pattern[0]
            for neigh in pattern[0][1]:
                if neigh == 0:
                    neigh = i
            final = []
            pattern_0 = pattern[1:]
            for node in start_nodes:
                if start[0] == '*' or self.labels[node] == start[0]:
                    star_pattern(pattern_0, [node], self.graph[node])
            for list in final:
                new_0 = list[i]
                list[i] = list[0]
                list[0] = new_0
            return final



        #This part does normal Query
        query_helper(pattern, [])
        #This part just checks for extra patterns that were added in final and
        #removes them.
        final_copy = final.copy()
        for list in final_copy:
            tag = True
            for i in range(len(list)):
                if not tag:
                    break
                node = list[i]
                edges = pattern[i][1]
                for edge in edges:
                    if list[edge] not in self.graph[node]:
                        tag = False
                        final.remove(list)
        return final

    def add_node(self, name, label=''):
        """Add a node with name `name` and label `label`."""
        if name in self.labels:
            raise ValueError
        else:
            self.graph[name] = set()
            self.labels[name] = label
            self.clique_size[1].add(frozenset([name]))
            self.cliques[name] = {frozenset([name])}


    def remove_node(self, name):
        """Remove the node with name `name`."""
        if name not in self.graph:
            raise LookupError
        else:
            self.graph.pop(name, None)
            self.labels.pop(name, None)
            #remove edges as well
            for node in self.graph:
                if name in self.graph[node]:
                    self.graph[node].remove(name)
            for node in self.cliques:
                cliques_to_remove = []
                for f_set in self.cliques[node]:
                    if name in f_set:
                        cliques_to_remove.append(f_set)
                        if len(f_set) in self.clique_size:
                            if f_set in self.clique_size[len(f_set)]:
                                self.clique_size[len(f_set)].remove(f_set)
                for clique in cliques_to_remove:
                    self.cliques[node].remove(clique)



    def add_edge(self, start, end):
        """Add a edge from `start` to `end`."""
        if start not in self.graph:
            raise LookupError
        if end not in self.graph:
            raise LookupError
        if end in self.graph[start]:
            raise ValueError
        else:
            self.graph[start].add(end)
        f_set_to_add = []
        for f_set in self.cliques[start]:
            for neighbor in f_set:
                if neighbor not in self.graph[end] or end not in self.graph[neighbor]:
                    break
            else:
                new_f_set = f_set | (frozenset([end]))
                f_set_to_add.append(new_f_set)
                if len(new_f_set) in self.clique_size:
                    self.clique_size[len(new_f_set)].add(new_f_set)
                else:
                    self.clique_size[len(new_f_set)] = {new_f_set}
        for clique in f_set_to_add:
            self.cliques[start].add(clique)


    def remove_edge(self, start, end):
        """Remove the edge from `start` to `end`."""
        if start not in self.graph:
            raise LookupError
        if end not in self.graph:
            raise LookupError
        if end not in self.graph[start]:
            raise LookupError
        self.graph[start].remove(end)
        for node in self.cliques:
            cliques_to_remove = []
            for f_set in self.cliques[node]:
                if start in f_set and end in f_set:
                    cliques_to_remove.append(f_set)
                    orig_len_clique = len(f_set)
                    if orig_len_clique in self.clique_size:
                        if f_set in self.clique_size[orig_len_clique]:
                            self.clique_size[orig_len_clique].remove(f_set)
            for clique in cliques_to_remove:
                self.cliques[node].remove(clique)




if __name__ == '__main__':
    pass
