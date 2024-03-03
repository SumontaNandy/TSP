import networkx as nx
import tsplib95
import mst


file =  open('data/gr17.tsp')
problem = tsplib95.read(file)

mst_instance = mst.MST(problem.get_graph())
mst_instance.get_mst()


