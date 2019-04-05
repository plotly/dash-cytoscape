from collections import deque


class Tree(object):
    def __init__(self, node_id, children=None, data=None, edge_data=None):
        """
        A class to facilitate tree manipulation in Cytoscape.
        :param node_id: The ID of this tree, passed to the node data dict
        :param children: The children of this tree, also Tree objects
        :param data: Dictionary passed to this tree's node data dict
        :param edge_data: Dictionary passed to the data dict of the edge connecting this tree to its
        parent
        """
        if not children:
            children = []
        if not data:
            data = {}
        if not edge_data:
            edge_data = {}

        self.node_id = node_id
        self.children = children
        self.data = data
        self.edge_data = edge_data
        self.index = {}

    def _dfs(self, search_id):
        if self.node_id == search_id:
            return self
        elif self.is_leaf():
            return None
        else:
            for child in self.children:
                result = child.dfs()
                if result:
                    return result

            return None

    def _bfs(self, search_id):
        stack = deque([self])

        while stack:
            tree = stack.popleft()

            if tree.node_id == search_id:
                return tree

            if not tree.is_leaf():
                for child in tree.children:
                    stack.append(child)

        return None

    def is_leaf(self):
        """
        :return: If the Tree is a leaf or not
        """
        return not self.children

    def add_child(self, child):
        """
        Add a single child to the children of a Tree.
        :param child: Tree object
        """
        self.children.append(child)

    def add_children(self, children):
        """
        Add a list of children to the current children of a Tree.
        :param children: List of Tree objects
        """
        self.children.extend(children)

    def get_edges(self):
        """
        Get all the edges of the tree in Cytoscape JSON format.
        :return: List of dictionaries, each specifying an edge
        """
        edges = [
            {
                'data': {
                    'source': self.node_id,
                    'target': child.node_id,
                    **self.edge_data
                }
            }
            for child in self.children
        ]

        for child in self.children:
            edges.extend(child.get_edges())

        return edges

    def get_nodes(self):
        """
        Get all the nodes of the tree in Cytoscape JSON format.
        :return: List of dictionaries, each specifying a node
        """
        nodes = [
            {
                'data': {
                    'id': self.node_id,
                    **self.data
                }
            }
        ]

        for child in self.children:
            nodes.extend(child.get_nodes())

        return nodes

    def get_elements(self):
        """
        Get all the elements of the tree in Cytoscape JSON format.
        :return: List of dictionaries, each specifying an element
        """
        return self.get_nodes() + self.get_edges()

    def find_by_id(self, search_id, method='bfs'):
        """
        Find a Tree object by its ID.
        :param search_id: the queried ID
        :param method: Which traversal method to use. Either "bfs" or "dfs"
        :return: Tree object if found, None otherwise
        """
        method = method.lower()

        if method == 'bfs':
            return self._bfs(search_id)
        elif method == 'dfs':
            return self._dfs(search_id)
        else:
            raise ValueError('Unknown traversal method')

    def create_index(self):
        """
        Generate the index of a Tree, and set it in place. If there was a previous index, it is
        erased. This uses a BFS traversal. Please note that when a child is added to the tree,
        the index is not regenerated. Furthermore, an index assigned to a parent cannot be
        accessed by its children, and vice-versa.
        :return: Dictionary mapping node_id to Tree object
        """
        stack = deque([self])
        self.index = {}

        while stack:
            tree = stack.popleft()
            self.index[tree.node_id] = tree

            if not tree.is_leaf():
                for child in tree.children:
                    stack.append(child)

        return self.index
