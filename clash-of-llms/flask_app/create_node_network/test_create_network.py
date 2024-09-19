import unittest
import os
from create_network import create_node_network
from excel_api.import_excel import import_node_attributes, import_node_connections

class TestCreateNetwork(unittest.TestCase):

    def setUp(self):
        # Define paths relative to this script's location
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.attributes_file = os.path.join(current_dir, "NodeAttributes.xlsx")
        self.connections_file = os.path.join(current_dir, "NodeConnections.xlsx")
        self.output_file = os.path.join(current_dir, "network_output.json")

        # Ensure the test cleans up after itself
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

        # Load test data
        self.node_attributes = import_node_attributes(self.attributes_file)
        self.node_connections = import_node_connections(self.connections_file)

    def tearDown(self):
        # Clean up generated files
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_network_creation(self):
        # Run the function to create the network
        create_node_network(self.node_attributes, self.node_connections)

        # Check if the file was created
        self.assertTrue(os.path.exists(self.output_file), "network_output.json was not created")

        # Optionally, you could add more checks here to validate the content of the JSON file

if __name__ == "__main__":
    unittest.main()
