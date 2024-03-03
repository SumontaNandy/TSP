import networkx as nx
import numpy as np
import dsu

DEBUG = True
class MST:
    def __init__(self) -> None:
        self.cost = 0

    def get_mst_k(self, graph: nx.Graph, k : int) -> nx.Graph:
        edges = graph.edges

        weighted_edges = {}
        for u, v in edges:
            weighted_edges[(u,v)] = int(graph.get_edge_data(u,v)["weight"])
        weighted_edges = sorted(weighted_edges.items(), key=lambda x: x[1], reverse=True)

        # dropping self loops in weighted edge
        i = len(weighted_edges) - 1
        print(i)
        while (weighted_edges[i][1] == 0):
            i -= 1
        weighted_edges = weighted_edges[:i]

        if DEBUG:
            print("MST weighted Edges: ",weighted_edges)

        disjoin_set = dsu.DSU(graph.nodes)
        mst_graph = nx.Graph()
        edge_count = 0
        edge_target = graph.number_of_nodes() - 1
        while edge_count != edge_target:
            k_ = min(k, len(weighted_edges))
            weights = np.array([e[1] for e in weighted_edges[-k_:]])
            weights = (weights - np.mean(weights)) / np.std(weights)
            softmax_values = np.exp(-np.array(weights))
            probabilities = list(softmax_values / sum(softmax_values))
            selected_edge_index = np.random.choice(np.arange(len(weights)), p=probabilities) + len(weighted_edges) - k_
            selected_edge = weighted_edges[selected_edge_index]

            u, v = selected_edge[0]
            if disjoin_set.find_parent(u) != disjoin_set.find_parent(v):
                disjoin_set.union_sets(u, v)
                self.cost += selected_edge[1]
                mst_graph.add_weighted_edges_from([(u,v,selected_edge[1])])
                edge_count += 1
            
            weighted_edges = weighted_edges[:selected_edge_index] + weighted_edges[selected_edge_index+1 :]
        return mst_graph

    def get_mst(self, graph: nx.Graph) -> nx.Graph:
        edges = graph.edges

        weighted_edges = {}
        for u, v in edges:
            weighted_edges[(u,v)] = int(graph.get_edge_data(u,v)["weight"])
        weighted_edges = sorted(weighted_edges.items(), key=lambda x: x[1])

        if DEBUG:
            print("MST weighted Edges: ",weighted_edges)

        disjoin_set = dsu.DSU(graph.nodes)
        mst_graph = nx.Graph()
        for edge, weight in weighted_edges:
            u, v = edge
            if disjoin_set.find_parent(u) != disjoin_set.find_parent(v):
                disjoin_set.union_sets(u, v)
                self.cost += weight
                mst_graph.add_weighted_edges_from([(u,v,weight)])

        return mst_graph

    def get_mst_cost(self):
        return self.cost
    
    def get_odd_degree_nodes(self, mst : nx.Graph) -> list:
        nodes = mst.degree

    def get_odd_degree_nodes(graph: nx.Graph):
        return [node for node,degree in graph.degree if degree % 2 == 1]


