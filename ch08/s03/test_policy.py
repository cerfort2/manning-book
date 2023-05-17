import json
import pytest
from main import APP_NAME, CONFIGURATION_FILE


@pytest.fixture(scope="module")
def resources():
    with open(CONFIGURATION_FILE, 'r') as f:    #Loads the infrastructure configuration from a JSON file
        config = json.load(f)
    return config['resource']   #Parses the resource block out of the JSON configuration file


@pytest.fixture
def database_instance(resources):
    #Parses the Google compute firewall resource defined by Terraform from the JSON configuration
    return resources[2][
        'google_sql_database_instance'][0][APP_NAME][0]


def test_database_instance_should_have_tags(database_instance): #Uses a descriptive test name explaining the policy for the firewall rule, which should not allow all traffic
    assert database_instance['settings'][0]['user_labels'] \
    #Checks that 0.0.0.0/0, or allow all, is not defined in the rule’s source ranges
        is not None
    assert len(
        database_instance['settings'][0]['user_labels']) > 0, \
        'database instance must have `user_labels`' + \
        'configuration with tags'
#Uses a descriptive error message describing how to correct the firewall rule, such as removing 0.0.0.0/0 from source ranges
