import networkx as nx
import tsplib95
from mst import MST
import utils

file =  open('data/gr17.tsp')
graph = tsplib95.read(file).get_graph()

class TSP:
    def __init__(self) -> None:
        pass

    def christofides(graph:nx.Graph,kruskal_heuristics_k = None):
        mst = MST()
        if kruskal_heuristics_k:
            mst_graph = mst.get_mst_k(graph, k=kruskal_heuristics_k)
        else:
            mst_graph = mst.get_mst(graph)
        utils.plot_graph(mst_graph, 'mst.png')
        cost = mst.get_mst_cost()

        odd_nodes = MST.get_odd_degree_nodes(mst_graph)
        print('odd: ', odd_nodes)
        subgraph = nx.Graph(graph.subgraph(odd_nodes))
        utils.plot_graph(subgraph, name='subgraph.png')


        new_graph = nx.Graph()
        for e in subgraph.edges:
            new_graph.add_edge(e[0], e[1], weight= -int((subgraph[e[0]][e[1]]['weight'])))

        set_matching = nx.max_weight_matching(new_graph, maxcardinality=True)

        matching_graph = nx.Graph()
        for m in set_matching:
            matching_graph.add_edge(m[0], m[1], weight=subgraph[m[0]][m[1]]['weight'])

        # maxCardinality ensures all nodes in the subgraph are selected while making matching maximum
        set_matching = nx.min_weight_matching(subgraph, maxcardinality=True, weight="weight") 
        print(set_matching)
        matching_graph = nx.Graph()
        for u, v in set_matching:
            matching_graph.add_edge(u, v, weight=subgraph[u][v]["weight"])
        utils.plot_graph(matching_graph, 'min_matching.png')

        total_graph = nx.Graph(multi_graph=True)
        for u,v in mst_graph.edges:
            total_graph.add_edge(u,v, weight=mst_graph[u][v]['weight'])
        for u, v in matching_graph.edges:
            total_graph.add_edge(u, v, weight=1)

        utils.plot_graph(total_graph, 'total_graph.png') # wont work because weights were not added

        euler_tour_edges = nx.algorithms.eulerian_circuit(total_graph)
        print(nx.algorithms.is_eulerian(total_graph))
        # euler_tour = []
        # for e in euler_tour_edges:
        #     euler_tour.append(e)
        # euler_tour_vertices.append(euler_tour_vertices[-1]) # creating the cycle by adding the first edge
        # print("Euler Tour vertices: ", euler_tour_vertices)

        # final_graph = nx.Graph(di_graph=True)
        # for i in range(len(euler_tour_vertices) - 1):
        #     u = euler_tour_vertices[i]
        #     v = euler_tour_vertices[i+1]
        #     final_graph.add_edge(u, v, weight=graph[u][v]["weight"])
        
        # utils.plot_graph(final_graph, 'TSP.png')
        # return final_graph

    def christofidesv2(G:nx.Graph, kruskal_heuristics_k=None):
        loop_nodes = nx.nodes_with_selfloops(G)
        try:
            node = next(loop_nodes)
        except StopIteration:
            pass
        else:
            G = G.copy()
            G.remove_edge(node, node)
            G.remove_edges_from((n, n) for n in loop_nodes)

        N = len(G) - 1

        if any(len(neighbors) != N for n, neighbors in G.adj.items()):
            print('Must be a complete graph')
            return
        
        utils.plot_graph(G, 'initial.png')

        if kruskal_heuristics_k:
            tree = MST().get_mst_k(G, k=kruskal_heuristics_k)
        else:
            tree = nx.algorithms.minimum_spanning_tree(G)

        utils.plot_graph(tree, 'mst.png')

        L = G.copy()
        L.remove_nodes_from([v for v, degree in tree.degree if not (degree % 2)])
        MG = nx.MultiGraph()
        MG.add_edges_from(tree.edges)
        edges = nx.min_weight_matching(L, weight="weight")
        MG.add_edges_from(edges)
        # utils.plot_graph(MG, 'combined_graph.png')

        nodes = []
        for u, v in nx.eulerian_circuit(MG):
            if v in nodes:
                continue
            if not nodes:
                nodes.append(u)
            nodes.append(v)
        nodes.append(nodes[0])
        return nodes
    
    def getTSPCost(G: nx.Graph, nodes):
        cost = 0
        for i in range(len(nodes) - 1):
            cost += G[nodes[i]][nodes[i+1]]['weight']
        return cost

nodes = TSP.christofidesv2(graph, kruskal_heuristics_k = None)
cost = TSP.getTSPCost(graph, nodes)
print(nodes, cost)
