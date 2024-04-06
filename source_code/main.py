# import paths_data
# import vars_data
# import stops_data

# print('main')
import networkx as nx
import matplotlib.pyplot as plt

# Create an empty graph
G = nx.Graph()

# Add nodes
G.add_node(1)
G.add_node(2)
G.add_node(3)

# Add edges
G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 1)

# Draw the graph
nx.draw(G, with_labels=True, node_color='lightblue', node_size=1000, font_size=12)

# Display the graph
plt.show()