"""
    Graphs such as a DAG
"""

from itertools import chain, count
from typing import Any, Generator, Sequence, Tuple
class Graph():
    """
        Directed Acyclic Graph utilizing adjacency lists under the hood
    """
    def __init__(self):
        """
            Constructor
        """
        self.graph = {}

    def add_edge(self, source, destination):
        """
            Add an edge from source to destination
        """
        self.graph[source] = self.graph.get(source, set()) | set([destination])
        if destination not in self.graph:
            self.graph[destination] = set()

    def remove_edge(self, source, destination):
        """
            Remove an edge from source to destination
        """
        self.graph[source].remove(destination)

    def get_nodes(self):
        """
            Get a list of nodes
        """
        return set(chain.from_iterable((node, *edges) for node, edges in self.graph.items()))

    def get_roots(self):
        """
            Get a list of roots
        """
        return [n for n in self.get_nodes() if all(n not in edges for edges in self.graph.values())]

    def __bool__(self):
        """
            Return true if the graph is not empty
        """
        return bool(self.graph)

    def get_edges(self, node) -> Sequence[Any]:
        """
            Get a list of edges coming from the node
        """
        return self.graph[node]

    def remove_node(self, node):
        """
            Remove a node from the graph and all the edges emanating from it
        """
        for source, edges in self.graph.items():
            if node in edges:
                self.remove_edge(source, node)
        del self.graph[node]

    def __str__(self):
        return "\n".join(f"Node: {source} Edges: {edges}" for source, edges in self.graph.items())

    def get_node_distances(self, origin: Any) -> Generator[Tuple[int, Any], None, None]:
        """
            Get a list of nodes and their distance from the origin
        """
        queue = set([origin])
        seen = set([origin])
        for counter in count():
            yield from ((counter, n) for n in queue)
            edges = chain.from_iterable(self.get_edges(n) for n in queue)
            queue = set(n for n in edges if n not in seen)
            seen = seen | queue
            if not queue:
                break
