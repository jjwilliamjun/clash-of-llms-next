import copy
import networkx as nx


class GreenTeam:
    def __init__(self, network_graph, blue_alignment, red_alignment):
        self._network_graph = network_graph 
        self._blue_alignment=blue_alignment #Number of "blue-leaning" nodes in the graph
        self._red_alignment=red_alignment #Number of "red-leaning" nodes in the graph 
        self._previous_network_graph=network_graph
        self._size=network_graph.number_of_nodes()
        self.alignment_min=-1 #to change once parsed in from excel files
        self.alignment_max=1 #To change once that's parsed in from excel files

    def update_green_network(self):
        self._previous_network_graph=copy.deepcopy(self._network_graph)

        for old_node in self._previous_network_graph.nodes():
            previous_alignment=nx.get_node_attributes(self._previous_network_graph, "Alignment")
            current_alignment=nx.get_node_attributes(self._network_graph, "Alignment")
            node_alignment=previous_alignment[old_node] 
            neighbors = list(self._previous_network_graph.neighbors(old_node))

            if node_alignment < self.alignment_min/2 or node_alignment > self.alignment_max/2:
                for neighbor in neighbors:
                    neighbour_alignment=current_alignment[neighbor]
                    neighbour_influence=self._previous_network_graph.get_edge_data(old_node, neighbor)['weight']

                    influence_factor= self.influence_neighbours(neighbour_influence, node_alignment) 
                    if neighbour_alignment >= node_alignment:
                        new_alignment=current_alignment[neighbor] - influence_factor
                        self.update_node_alignment(neighbor, new_alignment)

                    else:
                        new_alignment=current_alignment[neighbor] + influence_factor
                        self.update_node_alignment(neighbor, new_alignment)
                      
        self.update_team_alignments(new_alignment)
        self.new_alignments()

    def new_alignments(self):
        alignment=nx.get_node_attributes(self._network_graph, "Alignment")
        for node in self._network_graph.nodes():
            print(node, alignment[node])

    def broadcast_message(self, potency, team, influence_factor):
        "Updates the green nodes when a message is broadcasted from red or blue teams"
        current_alignment=nx.get_node_attributes(self._network_graph, "Alignment")
        alignment_influence=(float(potency)/100)*influence_factor
        for node in self._network_graph.nodes():
            #Assumes blue alignment is negative, and red alignment is positive
            if team.lower() == 'blue': 
                new_alignment=current_alignment[node] - alignment_influence
                self.update_node_alignment(node, new_alignment)
            else:
                new_alignment=current_alignment[node] + alignment_influence
                self.update_node_alignment(node, new_alignment)
        self.new_alignments()


    def update_node_alignment(self, current_node, new_alignment):
        """Updates the alignment of a green node"""
        nx.set_node_attributes(self._network_graph, {current_node: new_alignment}, "Alignment")
        return

    def influence_neighbours(self, neighbour_influence, node_alignment):
        """Returns the change in nodes alignment after influence from a single neighbour"""
        
        update_factor=node_alignment*neighbour_influence
        return update_factor


    def update_team_alignments(self, node_alignment):
        """Updates the alignment of the graph after both teams have broadcasted a message, and each node has influenced their neighbours"""
        """Operates under the assumption that alignment_max represents complete red team alignment, and blue team alignment is alignment_min"""
        if node_alignment > self.alignment_max/2:
            self._red_alignment+=1
        elif node_alignment < self.alignment_min/2:
            self._blue_alignment+=1

    def print_all_node_alignments(self):
        """Prints the alignment of all nodes in the network graph"""
        alignment = nx.get_node_attributes(self._network_graph, "Alignment")
        for node_id in self._network_graph.nodes():
            node_alignment=alignment[node_id]
            print(f"Node {node_id}: Alignment = {node_alignment}")
    
    def blue_alignment(self):
        """Returns the % of the population that aligns with the blue team"""
        return (self._blue_alignment/self._size)*100

    def red_alignment(self):
        """Returns the % of the population that aligns with the red team"""
        return (self._red_alignment/self._size)*100

        
    def test_scripts():
        #WIP
        green_team_test=green_team(network, 30, 20)
        print("The number of nodes in this network is ", green_team_test._size)
        green_team_test.blue_alignment()
        green_team_test._red_alignment()
