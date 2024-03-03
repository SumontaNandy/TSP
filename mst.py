import networkx as nx
class MST:
    def __init__(self, graph : nx.Graph) -> None:
        self.graph = graph

    def get_mst(self) -> nx.Graph:
        edges = self.graph.edges
        print(edges)