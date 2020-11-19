import networkx as nx
import matplotlib.pyplot as plt
from itertools import count

class Political_Graph():
    
    def __init__(self, representative_nodes):
        self.graph = nx.MultiGraph()
        self.node_names = [rep.screen_name for rep in representative_nodes]
        
        for rep in representative_nodes:
            self.graph.add_node(rep.screen_name, meta=rep)
    
    def are_representatives_parsed(self):
        return all([self.graph.nodes[rep]['meta'].is_parsed for rep in self.graph.nodes])
    
    def build_network(self):
        if not self.are_representatives_parsed():
            return None
        
    def add_interactions(self, interaction_type, color='blue'):
        for rep in self.graph.nodes:
            rep_interactions = getattr(self.graph.nodes[rep]['meta'], interaction_type)
            
            for user in rep_interactions:
                if user not in self.node_names or user == rep:
                    continue
                    
                if self.graph.has_edge(rep, user, key=interaction_type):
                    self.graph[rep][user][interaction_type]['attr']['count'] += 1
                else:
                    self.graph.add_edge(rep, user, key=interaction_type, attr={'count':1, 'color':color})
        
        self.calculate_number_of_neighbors()
    
    def get_isolated_nodes(self):
        isolated = []
        for node in self.graph.nodes():
            if self.graph.degree(node) == 0:
                isolated.append(node)
        
        return isolated
                    
    def delete_isolated_nodes(self):
        for node in self.get_isolated_nodes():
            self.graph.remove_node(node)
    
    def calculate_number_of_neighbors(self):
        for k in self.graph.nodes():
            self.graph.nodes()[k]['count'] = len(self.graph[k])
    
    def draw_graph(self, layout):
        nodes = self.graph.nodes()

        groups = set(nx.get_node_attributes(self.graph, 'count').values())
        mapping = dict(zip(sorted(groups), count()))
        
        node_colors = [mapping[self.graph.nodes()[n]['count']] for n in nodes]
        edge_colors = [self.graph[u][v][key]['attr']['color'] for u,v,key in self.graph.edges]
        
        #pos = nx.spectral_layout(self.graph)
        fig, ax = plt.subplots(1, 1, figsize=(20, 10))

        ed = nx.draw_networkx_edges(self.graph, layout(self.graph), alpha=1, edge_color=edge_colors)
        no = nx.draw_networkx_nodes(self.graph, layout(self.graph), nodelist=nodes, 
                                    node_color=node_colors, node_size=50, cmap=plt.cm.jet, alpha=0.5, ax=ax)
        plt.colorbar(no)
        plt.axis('off')
        plt.show()