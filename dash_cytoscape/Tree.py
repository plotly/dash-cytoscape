from collections import deque


class Tree(object):
    def __init__(self, node_id, children=None, edge_id=None, data=None, edge_data=None):
        """
        An object to facilitate tree manipulation in Cytoscape
        :param node_id: The ID of this tree, passed to the node data dict
        :param children: The children of this tree, also Tree objects
        :param edge_id: The ID of the edge connecting this node to its parent
        :param data: Dictionary passed to this tree's node data dict
        :param edge_data: Dictionary passed to the data dict of the edge connecting this tree to its
        parent
        """
        self.node_id = node_id
        self.children = children
        self.edge_id = edge_id
        self.edge_data = edge_data
        self.data = data

    def is_leaf(self):
        return not self.children

    def add_child(self, child):
        self.children.append(child)

    def add_children(self, children):
        self.children.append(children)

    def get_edges(self):
        if not self.is_leaf():
            edges = [
                {
                    'data': {
                        'id': self.edge_id,
                        'source': self.node_id,
                        'target': child.node_id,
                        **self.edge_data
                    }
                }
                for child in self.children
            ]

            children_edges = [
                child.get_edges()
                for child in self.children
            ]

            return edges + children_edges

    def get_nodes(self):
        if not self.is_leaf():
            nodes = [
                {
                    'data': {
                        'id': self.node_id,
                        **self.data
                    }
                }
            ]

            children_nodes = [
                child.get_nodes()
                for child in self.children
            ]

            return nodes + children_nodes

    def get_elements(self):
        return self.get_nodes() + self.get_edges()

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

    def find_by_id(self, search_id, method='bfs'):
        for c in ' -_':
            method = method.replace(c, '')

        if method in ['bfs', 'breadthfirst', 'breadthfirstsearch']:
            return self._bfs(search_id)
        elif method in ['dfs', 'depthfirst', 'depthfirstsearch']:
            return self._dfs(search_id)
        else:
            raise ValueError('Unknown traversal method')
