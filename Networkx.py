#Networkx

"""
Documentation
https://networkx.github.io/documentation/stable/index.html
"""

import networkx as nx
import matplotlib.pyplot as plt
#%%
"""
Lav en graf
"""

G = nx.Graph()
print(type(G))

#%%
"""
Visualiser grafen
"""
nx.draw(G)
plt.show()

#%%
"""
Tilføj nodes og edges enkeltvis
"""
G.add_node("a")
G.add_node("b")
G.add_edge("a","b")

fig, (ax1,ax2) = plt.subplots(1,2)
nx.draw(G,with_labels=True,ax = ax1)
nx.draw_networkx(G,ax = ax2)
plt.show()
#%%%
"""
Tilføj nodes og edges fra et subscriptable objekt
"""

nodes = ["c","d","e"]
edges = [("a","e"),("b","d"),("c","d"),("d","e")]
G.add_nodes_from(nodes)
G.add_edges_from(edges)
nx.draw_networkx(G)
plt.show()



print(G.nodes(), "\n", "Antallet af nodes: ", G.number_of_nodes())
print(G.edges(), "\n", "Antallet af edges: ", G.number_of_nodes())
print("Naboer til a: ", list(G.adj["a"]))
#%%
"""
Degree
"""
print("Graden af alle knuder i G: ", G.degree())
print("Graden af knude a: ", G.degree("a"))
#%%
"""
Adjacency matrix og Incidence matrix
"""
A = nx.adjacency_matrix(G)
M = nx.incidence_matrix(G)
print("Adjacency matrix: ", "\n", A.todense())
print("Incidence matrix: ", "\n", M.todense())

#%%
"""
Kredsløb, simple stier og grids
"""

C=nx.cycle_graph(4)
P=nx.path_graph(4)

#4x4 grid
grid = nx.grid_2d_graph(4,4)

fig, (ax1,ax2,ax3) = plt.subplots(1,3)
nx.draw(C,ax=ax1)
nx.draw(P,ax=ax2, node_color="g")
nx.draw(grid,ax=ax3, node_color= "r")
plt.show()

#%%
from networkx.algorithms import tree
print(tree.recognition.is_tree(C), tree.recognition.is_tree(P))

#%%
"""
Tilfældige grafer
"""
from networkx import generators
rand_tree = generators.trees.random_tree(5,seed = 0)
rand_graph = generators.random_graphs.gnm_random_graph(5,6, seed = 0)

print( tree.recognition.is_tree(rand_tree))
fig, (ax1, ax2) = plt.subplots(1,2)
nx.draw(rand_tree, ax=ax1, node_color="r")
nx.draw(rand_graph, ax=ax2)
plt.show()


#%%
"""
Bipartite graf
"""
from networkx.algorithms import bipartite
B = nx.Graph()
#Kan tilføje attributer til knuder. Kunne f.eks. også være weights
B.add_nodes_from(["x1","x2","x3"], bipartite = 0)
B.add_nodes_from(["y1", "y2"], bipartite = 1)

edges = [("x1", "y1"), ("x1", "y2"), ("x2", "y1"), ("x3", "y2")]
B.add_edges_from(edges)
print(nx.bipartite.is_bipartite(B)) # False hvis ikke bipartite

#%%
print(B.nodes(data=True))
# Sets og color raises error hvis grafen ikke er bipartite
X, Y = nx.bipartite.sets(B)
print("X: ",X, "\n", "Y: ",  Y)
colors = nx.bipartite.color(B)
print(colors)


#%%%
pos = dict()
pos.update((n, (0, idx*10)) for idx, n in enumerate(X))
pos.update((n, (0.5, idx*10)) for idx, n in enumerate(Y))
"""
Bemærk nx.bipartite.color ændrer rækkefølge, så man kan ikke benytte denne list 
comprehension
color = ["r" if colors[key] == 1 else "b" for key in colors]
"""
color = ["r" if node[1]['bipartite'] == 1 else "b" for node in B.nodes(data=True)]
fig, (ax1, ax2) = plt.subplots(1,2)
nx.draw(B, with_labels = True, ax = ax1, node_color = color)
nx.draw(B,pos = pos, with_labels=True, ax = ax2, node_color = color)

plt.show()

#%%
"""
Komplette grafer
"""
K_4 = nx.complete_graph(4)
K_3_3 = nx.complete_bipartite_graph(3,3)

print(nx.bipartite.is_bipartite(K_3_3)) #
print(K_3_3.nodes(data=True))
#%%
color = ["r" if node[1]['bipartite'] == 1 else "b" for node in K_3_3.nodes(data=True)]
fig, (ax1, ax2) = plt.subplots(1,2)
nx.draw(K_4, ax = ax1)
nx.draw(K_3_3, ax=ax2, node_color = color)
plt.show()
#%%
"""
Subgraphs
"""
print(K_4.edges())
#Subgraphs made from subset of E(K_4)
H1 = K_4.edge_subgraph([(0,3), (1,3), (1,2)])
print(H1.nodes())

fig, (ax1, ax2) = plt.subplots(1,2)
nx.draw(H1, ax=ax1)
# Subgraphs made from a subset of V(K_4)
H2 = K_4.subgraph([0,2,3]) 
nx.draw(H2, ax=ax2, node_color="r")
plt.show()

#%%
"""
Symmetric differences og andre operatorer
"""
from networkx.algorithms import operators
C1 = nx.cycle_graph(5)
C2 = nx.cycle_graph(5)
print(C1.nodes(), C2.nodes())

#%%
G = operators.binary.union(C1,C2, rename=("o-", "i-"))
G1 = operators.binary.disjoint_union(C1,C2)
print(G.nodes(),"\n", G1.nodes)


nx.draw(G1, with_labels = True)
plt.show()
#%%
#Vi kan lime disse to grafer sammen
edges = [(i,i+5) for i in G1.nodes() if i <=4]
G1.add_edges_from(edges)


pos1 = {0: (0,10), 1: (-0.3, 7.5), 2: (-0.2, 3), 3: (0.2, 3), 4: (0.3, 7.5), 5: (0,8), 6: (-0.15,6.5), 7: (-0.1,4.5),
      8: (0.1,4.5), 9: (0.15,6.5)}
nx.draw(G1, with_labels = True, pos=pos1)
plt.show()

#%%
"""
Matching og covering
"""
from networkx.algorithms import matching
M = set(((0,5), (6,7), (2,3), (8,9)))
edge_color = ["r" if edge in M else "black" for edge in G1.edges()]
print(matching.is_matching(G, M))
nx.draw(G1, pos = pos1, with_labels=True, edge_color =  edge_color)
plt.show()

#%%
path = nx.Graph()
path.add_nodes_from(G1.nodes())
path.add_edges_from([(1,6), (6,7), (2,7), (2,3), (3,8), (8,9), (9,4)])
#nx.draw(path, pos=pos, with_labels=True)

m_graph = nx.Graph()
m_graph.add_nodes_from(G1.nodes())
m_graph.add_edges_from(list(M))

new_matching = operators.binary.symmetric_difference(m_graph, path) #Skal have samme knuder

nx.draw(new_matching, pos= pos1, with_labels = True)
plt.show()


#%%
M = set(new_matching.edges())
print("Er M en matching i G?: ", matching.is_matching(G1,M))
print("Er M en maximal matching i G?: ",matching.is_maximal_matching(G1, M))
print("Er M en perfekt matching i G?: ", matching.is_perfect_matching(G1, M))

#%%
"""
Bemærk at maximum_matching returner et dict, mens maximal_matching returner
et set.
"""
max_matching = nx.bipartite.maximum_matching(B)
max_matching1 = nx.matching.maximal_matching(B)
vertex_cover = nx.bipartite.to_vertex_cover(B, max_matching)
print("bipartite.maximum_matching(B) returner følgende dict: ",max_matching
      ,"\n", "matching.maximal_matching(B) giver os sættet: "
      , max_matching1)
print("Vores vertex cover bliver: ", vertex_cover)

node_color = ["g" if node in vertex_cover else "b" for node in B.nodes()]
edge_color = ["r" if edge in max_matching1 or (edge[1], edge[0]) in max_matching1
              else "black" for edge in B.edges()]
nx.draw(B, pos = pos, with_labels = True, node_color = node_color, 
        edge_color = edge_color)
plt.show()

#%%
"""
Finding a path
"""
#Betragter tidligere eksempel
nx.draw(G1, pos=pos1, with_labels=True)
plt.show()
#%%

path = list(nx.algorithms.simple_paths.shortest_simple_paths(G1, 1,4))
print("Alle stier fra knude 1 til knude 4: ", *path)
print("Shortest path: ", list(path)[0])

path_edges = [(n, path[0][idx+1]) for idx,n in enumerate(path[0][:-1])]
print(path_edges)
edge_color = ["r" if edge in path_edges or (edge[1], edge[0]) in path_edges else "black" for edge in G1.edges()]
nx.draw(G1, pos=pos1, with_labels=True, edge_color = edge_color)
plt.show()