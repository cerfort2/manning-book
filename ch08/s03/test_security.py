import json
import pytest
from main import APP_NAME, CONFIGURATION_FILE


@pytest.fixture(scope="module")
def resources():
    #Loads the infrastructure configuration from a JSON file
    with open(CONFIGURATION_FILE, 'r') as f:
        config = json.load(f)
    return config['resource']
    #Parses the resource block out of the JSON configuration file

@pytest.fixture
def database_firewall_rule(resources):
    return resources[0][
        'google_compute_firewall'][0][APP_NAME][0]
#Parses the Google compute firewall resource defined by Terraform from the JSON configuration

#Uses a descriptive test name explaining the policy for the firewall rule, which should not allow all traffic
def test_database_firewall_rule_should_not_allow_everything(
        database_firewall_rule):
    #Checks that 0.0.0.0/0, or allow all, is not defined in the rule’s source ranges
    assert '0.0.0.0/0' not in \
    #Uses a descriptive error message describing how to correct the firewall rule, such as removing 0.0.0.0/0 from source ranges
        database_firewall_rule['source_ranges'], \
        'database firewall rule must not ' + \
        'allow traffic from 0.0.0.0/0, specify source_ranges ' + \
        'with exact IP address ranges'
