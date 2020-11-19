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
        return all([self.graph.node[rep]['meta'].is_parsed for rep in self.graph.nodes])
    
    def build_network(self):
        if not self.are_representatives_parsed():
            return None
        
    def add_like_weights(self, color='blue'):
        for rep in self.graph.nodes:
            rep_likes = [rep.likes for rep in self.graph.nodes]
            for liked_user in rep_likes:
                if liked_user not in self.node_names or liked_user == user:
                    continue
                    
                if self.graph.has_edge(user, liked_user, key='like'):
                    self.graph[user][liked_user]['count'] += 1
                else:
                    self.graph.add_edge(user, liked_user, key='like', attr={'weight':1, 'color':color})
        
        self.calculate_number_of_neighbors()
                
    
    def add_retweet_weights(self, weight=-2, color='red'):
        for user, user_retweets in retweets:
            for retweet in user_retweets:
                if retweet not in self.nodes or user==retweet:
                    continue
                    
                if self.graph.has_edge(user, retweet):
                    self.graph[user][retweet]['weight'] += weight
                else:
                    self.graph.add_edge(user, retweet, weight=weight)
                    
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
        colors = [mapping[self.graph.nodes()[n]['count']] for n in nodes]
        
        #pos = nx.spectral_layout(self.graph)
        fig, ax = plt.subplots(1, 1, figsize=(20, 10))

        ed = nx.draw_networkx_edges(self.graph, layout(self.graph), alpha=0.2)
        no = nx.draw_networkx_nodes(self.graph, layout(self.graph), nodelist=nodes, 
                                    node_color=colors, node_size=50, cmap=plt.cm.jet, alpha=0.5, ax=ax)
        plt.colorbar(no)
        plt.axis('off')
        plt.show()