import pytest       
#Imports pytest, a Python testing library. 
#You need to name the file and tests prefixed with test_ for pytest to run them.

#Imports the network factory module from main.py.
#You need to run the method for network configuration.
from main import NetworkFactoryModule

#Sets expected values as constants, such as network prefix and IP range
NETWORK_PREFIX = 'hello-world'
NETWORK_IP_RANGE = '10.0.0.0/16'

#Creates the network from the module as a test fixture based on expected values.
#This fixture offers a consistent network object for all tests to reference.
@pytest.fixture(scope="module")
def network():
    return NetworkFactoryModule(
        name=NETWORK_PREFIX,
        ip_range=NETWORK_IP_RANGE,
        number_of_subnets=3)


#Creates a separate fixture for the network configuration since you need to parse google_compute_network. 
#One test uses this fixture to test the network name.
@pytest.fixture
def network_configuration(network):
    return network._network_configuration()['google_compute_network'][0]

#Creates a separate fixture for the subnet configuration since you need to parse for google_compute_subnetwork. 
#Two tests use this fixture for checking the number of subnets and their IP address ranges.
@pytest.fixture
def subnet_configuration(network):
    return network._subnet_configuration()[
        'google_compute_subnetwork']

#Pytest will run this test to check the configuration for the network name to match hello-world-network.
#It references the network_configuration fixture.
def test_configuration_for_network_name(network, network_configuration):
    assert network_configuration[network._network_name][
        0]['name'] == f"{NETWORK_PREFIX}-network"

#Pytest will run this test to check the configuration for the number of subnets to equal 3.
#It references the subnet_configuration fixture.
def test_configuration_for_three_subnets(subnet_configuration):
    assert len(subnet_configuration) == 3

#Pytest will check the correct subnet IP range in the network example configuration. 
#It references the subnet_configuration fixture.
def test_configuration_for_subnet_ip_ranges(subnet_configuration):
    for i, subnet in enumerate(subnet_configuration):
        assert subnet[next(iter(subnet))
                      ][0]['ip_cidr_range'] == f"10.0.{i}.0/24"
