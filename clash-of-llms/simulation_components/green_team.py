#TO DO
#import networkData from '../../excel_api/network_output.json';
#make network graph global variable
#to do: define what game info red and blue team would need 
#only green nodes that meet certain alignment thresholds can influence others 
#alignment_min, alignment_max (eg -1 to 1). Nodes must be >0.5 or <-0.5. 
#equation: must be < alignment_min/2 || >alignment_max/2
#do we have a param for green influence factor?


#Green nodes will be updated after red and blue teams have disseminated messages
import copy


class green_team:
    def __init__(self, network_graph, blue_alignment, red_alignment):
        self._network_graph = network_graph
        self._blue_alignment=blue_alignment
        self._red_alignment=red_alignment
        self._previous_network_graph
        self._size=network_graph.number_of_nodes()

    def update_green_network(self, message, potency):
        self._previous_network_graph=copy.deepcopy(self._network_graph)
        test_copy_works()
        
        for old_node, current_node in self._previous_network_graph.nodes(), self._network_graph.nodes():
            #Each node gets influenced by its neighbours view
            node_alignment=old_node['Alignment']
            neighbors = list(self._previous_network_graph.neighbors(old_node))
            print("neighbours of ",old_node,"are ",neighbors, "and check if the node versions match",current_node)

            for neighbor in neighbors:
                neighbour_alignment=neighbor['Alignment']
                neighbour_influence=neighbor['Influence']
                print("Neighbor's alignment is ", neighbour_alignment)
                if neighbour_alignment < -0.5 or neighbour_alignment > 0.5:  #to be replaced by alignment_min/max/2. Creates threshold for node to be "influential"
                    influence_factor= influence_neighbours(neighbour_influence, neighbour_alignment) 
                    if neighbour_alignment >= node_alignment:
                        current_node['Alignment'] += influence_factor
                        print("Neighbours alignment is ", neighbour_alignment, "and old node alignment is ", node_alignment, "and ", influence_factor, "is being added")
                    else:
                        print("Neighbours alignment is ", neighbour_alignment, "and old node alignment is ", node_alignment, "and ", influence_factor, "is being subtracted")
                        current_node['Alignment'] -= influence_factor
            #could update alignment with each node value here?             
        update_team_alignments(current_node['Alignment'])

    def update_message_influence(self, message,potency,node):
        "Updates the green nodes when a message is broadcasted from red or blue teams"
        #needs to iterate through each node once, and update alignment based equation/message/potency



    def influence_neighbours(self, neighbour_influence, neighbour_alignment):
        "Returns the change in nodes alignment after influence from a single neighbour"
        update_factor=neighbour_alignment*neighbour_influence #refine equation? potentially give user adivce on suitable influence factor to ensure slow convergence of network alignment
        return update_factor


    def update_team_alignments(self, node_alignment):
        """Updates the alignment of the graph after both teams have broadcasted a message, and each node has influenced their neighbours"""
        """Operates under the assumption that 1 represents complete red team alignment, and blue team alignment is -1"""
        if node_alignment > 0.5:
            self._red_alignment+=1
        elif node_alignment < -0.5:
            self._blue_alignment+=1


    def blue_alignment(self):
        """Returns the % of the population that aligns with the blue team"""
        return (self._blue_alignment/self._size)*100

    def red_alignment(self):
        """Returns the % of the population that aligns with the red team"""
        return (self._red_alignment/self._size)*100

        
    def test_scripts():
        #TO DO 
        green_team_test=green_team(network, 30, 20)
        print("The number of nodes in this network is ", green_team_test._size)
        green_team_test.blue_alignment()
        green_team_test._red_alignment()
    def test_copy_works(self):

        



    

                