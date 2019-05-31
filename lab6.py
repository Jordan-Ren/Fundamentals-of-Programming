"""6.009 Lab 6 -- Gift Delivery."""


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


class SimpleGraph(Graph):
    """Simple implementation of the Graph interface."""

    def __init__(self):
        self.labels = {}
        self.graph = {}

    def query(self, pattern):
        """Return a list of subgraphs matching `pattern`.

        Parameters:
            `pattern`: a list of tuples, where each tuple represents a node.
                The first element of the tuple is the label of the node, while
                the second element is a list of the neighbors of the node as
                indices into `pattern`. A single asterisk '*' in place of the
                label matches any label.

        Returns:
            a list of lists, where each sublist represents a match, its items
            being names corresponding to the nodes in `pattern`.

        pattern ex. [("*", [1]), ('house 2', [0])] -> two nodes that have
            two directed edges between them the first of which can be any node.

        pattern ex. [('*', [1, 2]), ('*', []), ('*', [])]
        """
        temp = []
        sublists = []
        def query_helper(pattern, temp):
            '''
            The generator is suppose to add nodes with the label into the correct slot,
            not all the nodes. Label is the first element in pattern, neighbors is the
            second.
            '''
            if len(pattern) == 1:
                for node in self.graph:
                    if node not in temp and self.labels[node] == pattern[0][0]:
                        sublists.append(temp + [node])
                    elif node not in temp and pattern[0][0] == '*':
                        sublists.append(temp + [node])
            else:
                for node in self.graph:
                    if node not in temp and self.labels[node] == pattern[0][0]:
                        temp.append(node)
                        query_helper(pattern[1:], temp)
                        temp.pop()
                    elif pattern[0][0] == '*' and node not in temp:
                        temp.append(node)
                        query_helper(pattern[1:], temp)
                        temp.pop()
        query_helper(pattern, [])
        final = []
        for list in sublists:
            tag = True
            for i in range(len(list)):
                if not tag:
                    break
                node = list[i]
                edges = pattern[i][1]
                for edge in edges:
                    if list[edge] not in self.graph[node]:
                        tag = False
            if tag:
                final.append(list)
        return final


    def add_node(self, name, label=''):
        """Add a node with name `name` and label `label`."""
        if name in self.labels:
            raise ValueError
        else:
            self.graph[name] = []
            self.labels[name] = label


    def remove_node(self, name):
        """Remove the node with name `name`."""
        if name not in self.graph:
            raise LookupError
        else:
            self.graph.pop(name, None)
            # self.labels.pop(name, None)
            #remove edges as well
            for node in self.graph:
                if name in self.graph[node]:
                    self.graph[node].remove(name)

    def add_edge(self, start, end):
        """Add a edge from `start` to `end`."""
        if start not in self.graph:
            raise LookupError
        if end not in self.graph:
            raise LookupError
        if end in self.graph[start]:
            raise ValueError
        else:
            self.graph[start].append(end)

    def remove_edge(self, start, end):
        """Remove the edge from `start` to `end`."""
        if start not in self.graph:
            raise LookupError
        if end not in self.graph:
            raise LookupError
        if end not in self.graph[start]:
            raise LookupError
        self.graph[start].remove(end)

class CompactGraph(Graph):
    """Interface for a mutable graph that can answer queries."""
    def __init__(self):
        self.node_graph = {}
        self.edge_graph = {}
        self.labels = {}
        # self.key_usage = {}
        self.keys = 1

    def query(self, pattern):
        """Return a list of subgraphs matching `pattern`.

        Parameters:
            `pattern`: a list of tuples, where each tuple represents a node.
                The first element of the tuple is the label of the node, while
                the second element is a list of the neighbors of the node as
                indices into `pattern`. A single asterisk '*' in place of the
                label matches any label.

        Returns:
            a list of lists, where each sublist represents a match, its items
            being names corresponding to the nodes in `pattern`.

        """
        temp = []
        sublists = []
        def query_helper(pattern, temp):
            if len(pattern) == 1:
                for node in self.node_graph:
                    if node not in temp and self.labels[node] == pattern[0][0]:
                        sublists.append(temp + [node])
                    elif node not in temp and pattern[0][0] == '*':
                        sublists.append(temp + [node])
            else:
                for node in self.node_graph:
                    if node not in temp and self.labels[node] == pattern[0][0]:
                        temp.append(node)
                        query_helper(pattern[1:], temp)
                        temp.pop()
                    elif pattern[0][0] == '*' and node not in temp:
                        temp.append(node)
                        query_helper(pattern[1:], temp)
                        temp.pop()
        query_helper(pattern, [])
        final = []
        for list in sublists:
            tag = True
            for i in range(len(list)):
                if not tag:
                    break
                node = list[i]
                edges = pattern[i][1]
                for edge in edges:
                    if list[edge] not in self.edge_graph[self.node_graph[node]]:
                        tag = False
            if tag:
                final.append(list)
        return final

    def add_node(self, name, label=''):
        """Add a node with name `name` and label `label`."""
        if name in self.labels:
            raise ValueError
        self.labels[name] = label
        self.node_graph[name] = '0'
        if '0' not in self.edge_graph:
            self.edge_graph['0'] = set()
        #     self.key_usage['0'] = 1
        # else:
        #     self.key_usage['0'] += 1


    def remove_node(self, name):
        """Remove the node with name `name`."""
        if name not in self.node_graph:
            raise LookupError
        del self.edge_graph[self.node_graph[name]]
        del self.node_graph[name]
        # self.key_usage[self.node_graph[name]] -= 1
        # if self.key_usage[self.node_graph[name]] == 0:
        #     del self.edge_graph[self.node_graph[name]]

    def add_edge(self, start, end):
        # """Add a edge from `start` to `end`."""
        # if start not in self.node_graph:
        #     raise LookupError
        # if end not in self.node_graph:
        #     raise LookupError
        # if end in self.edge_graph[self.node_graph[start]]:
        #     raise ValueError
        start_key = self.node_graph[start]
        base = self.edge_graph[start_key] | {end}
        tag = False
        #Look through it, find if the new neighbors are found in edges
        #if so new key is key
        for key in self.edge_graph:
            if base == self.edge_graph[key]:
                self.node_graph[start] = key
                tag = True
                break
        #else: creat new key, using self.keys, increment it, add new
        #neighbors for the key.
        if not tag:
            node_key = self.node_graph[start]
            self.edge_graph[str(self.keys)] = base
            self.node_graph[start] = str(self.keys)
            self.keys += 1
        #removes the keys/neighbors in self.edge_graph that are no longer used.
        if start_key not in self.node_graph.values():
            del self.edge_graph[start_key]

    def remove_edge(self, start, end):
        """Remove the edge from `start` to `end`."""
        if start not in self.node_graph:
            raise LookupError
        if end not in self.node_graph:
            raise LookupError
        if end not in self.edge_graph[self.node_graph[start]]:
            raise LookupError
        start_key = self.node_graph[start]
        base = self.node_graph[start_key] - {end}
        tag = False
        for key in self.edge_graph:
            if base == self.edge_graph[key]:
                self.node_graph[start] = key
                tag = True
        if not tag:
            self.node_graph[start] = str(self.keys)
            self.edge_graph[str(self.keys)] = base
            self.keys += 1



def allocate_teams(graph, k, stations, gift_labels):
    """Compute the number of teams needed to deliver each gift.

    It is guaranteed that there is exactly one node for each gift type and all
    building nodes have the label "building".

    Parameters:
        `graph`: an instance of a `Graph` implementation
        `k`: minimum number of buildings that a cluster needs to contain for a
             delivery to be sent there
        `stations`: mapping between each node name and a string representing
                    the name of the closest subway/train station
        `gift_labels`: a list of gift labels

    Returns:
        a dictionary mapping each gift label to the number of teams
        that Santa needs to send for the corresponding gift to be delivered

    """
    final = {}
    station = stations.keys()
    for gift_label in gift_labels:
        for key in graph.labels:
            if graph.labels[key] == gift_label:
                gift_key = key
        gift_building = graph.query([[gift_label, [1]],['building', [0]]])
        #Check each second term in gift_building, check the label in stations
        #and keep track of how many of each.
        node_to_station = {}
        for pair in gift_building:
            node = pair[1]
            if int(node) in stations:
                if stations[int(node)] in node_to_station:
                    node_to_station[stations[int(node)]] += 1
                else:
                    node_to_station[stations[int(node)]] = 1
        for key in node_to_station:
            if node_to_station[key] >= k:
                if gift_label in final:
                    final[gift_label] += 1
                else:
                    final[gift_label] = 1
        if gift_label not in final:
            final[gift_label] = 0
    return final






if __name__ == '__main__':
    # Put code here that you want to execute when lab.py is run from the
    # command line, e.g. small test cases.
    g = CompactGraph()
    stations = {0: "Old Square", 1: "Old Square", 2: "Old Square", 3: "Old Square", 4: "Old Square", 5: "Town Hall", 6: "Town Hall", 7: "Town Hall", 8: "Town Hall", 9: "South Station", 10: "Ice Rink", 11: "Ice Rink", 12: "Ice Rink"}
    g.add_node('0', 'building')
    g.add_node('1', 'building')
    g.add_node('2', 'building')
    g.add_node('3', 'building')
    g.add_node('4', 'building')
    g.add_node('5', 'building')
    g.add_node('6', 'building')
    g.add_node('7', 'building')
    g.add_node('8', 'building')
    g.add_node('9', 'building')
    g.add_node('10', 'building')
    g.add_node('11', 'building')
    g.add_node('12', 'building')
    g.add_node('13', 'candy')
    g.add_node('14', 'puppy')
    for i in range(4):
        g.add_edge(str(i), '13')
        g.add_edge('13', str(i))
    for i in range(5, 12):
        if i == 9:
            continue
        g.add_edge(str(i), '14')
        g.add_edge('14', str(i))
    g.add_edge('9', '13')
    g.add_edge('13', '9')
    g.add_edge('7', '13')
    g.add_edge('13', '7')
    print(allocate_teams(g, 3, stations, ['candy', 'puppy']))
    pass
