import json #Imports Python’s JSON library because you will need to load a JSON file
import pytest

#Sets a constant with the expected filename for the network configuration. 
#The tests read the network configuration from network.tf.json.
NETWORK_CONFIGURATION_FILE = 'network.tf.json'

#Sets the expected network name to hello-world-network
expected_network_name = 'hello-world-network'

#Opens the JSON file with the network configuration and loads it as a test fixture
@pytest.fixture(scope="module")
def configuration():
    with open(NETWORK_CONFIGURATION_FILE, 'r') as f:
        return json.load(f)

#Creates a new test fixture that references the loaded JSON configuration and parses for any resource type. 
#It parses the JSON based on Terraform’s JSON resource structure.
@pytest.fixture
def resource():
    def _get_resource(configuration, resource_type):
        for resource in configuration['resource']:
            if resource_type in resource.keys():
                return resource[resource_type]
    return _get_resource

#Gets the google_compute_network Terraform resource out of the JSON file
@pytest.fixture
def network(configuration, resource):
    return resource(configuration, 'google_compute_network')[0]

#Gets the google_compute_subnetwork Terraform resource out of the JSON file
@pytest.fixture
def subnets(configuration, resource):
    return resource(configuration, 'google_compute_subnetwork')

#Pytest will run this test to check the configuration for the network name to match hello-world-network. 
#It references the network fixture.
def test_configuration_for_network_name(network):
    assert network[expected_network_name][0]['name'] \
        == expected_network_name

#Pytest will run this test to check the configuration for the number of subnets to equal 3.
#It references the subnet fixture.
def test_configuration_for_three_subnets(subnets):
    assert len(subnets) == 3

#Pytest will check for the correct subnet IP range configuration.
#It references the subnet fixture.
def test_configuration_for_subnet_ip_ranges(subnets):
    for i, subnet in enumerate(subnets):
        assert subnet[next(iter(subnet))
                      ][0]['ip_cidr_range'] == f"10.0.{i}.0/24"
