import networkx as nx
from pyvis.network import Network

# Load the data
G = nx.read_weighted_edgelist("mammalia-dolphin-florida-social.edges")

# Community detection using the greedy modularity algorithm
communities = list(nx.algorithms.community.modularity_max.greedy_modularity_communities(G))

# Create a Pyvis network
net = Network(height='800px', width='100%', notebook=True)

# Add nodes and edges to the Pyvis network
for node in G.nodes():
    for idx, community in enumerate(communities):
        if node in community:
            community_index = idx
            break
    net.add_node(node, title=f'Community: {community_index}', size=G.degree[node] * 10, color=community_index)

for edge in G.edges(data=True):
    net.add_edge(edge[0], edge[1], value=edge[2]['weight'], title=f'Weight: {edge[2]["weight"]}', width=edge[2]['weight'], color=edge[2].get('color', None))

# Set Pyvis physics layout for better visualization
net.force_atlas_2based()

# Add legend and title
options = {
    "nodes": {
        "borderWidth": 2
    },
    "edges": {
        "smooth": {
            "type": "continuous"
        }
    },
    "interaction": {
        "hover": True,
        "navigationButtons": True,
        "keyboard": {
            "enabled": True
        },
        "zoomView": True  # Enable zoom
    },
    "manipulation": {
        "enabled": True
    },
    "physics": {
        "enabled": True,
        "stabilization": {
            "iterations": 1000,
            "updateInterval": 100
        }
    }
}

try:
    net.set_options(options)
except Exception as e:
    print(f"An error occurred while setting options: {e}")

# Save or display the interactive plot
net.show('dolphin_social_network_pyvis_with_community_detection.html')
