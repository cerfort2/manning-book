#Pytest uses Libcloud to call the GCP API and get the server’s current state. 
#It checks that the server is running.
from libcloud.compute.types import NodeState
from main import generate_json, SERVER_CONFIGURATION_FILE
import os
import pytest
import test_utils

TEST_SERVER_NAME = 'hello-world-test'

#During the test session, uses a pytest test fixture to apply the configuration and creates a test server on GCP
@pytest.fixture(scope='session')
def apply_changes():
 # Generates a Terraform JSON file that uses the server module
    generate_json(TEST_SERVER_NAME)
    assert os.path.exists(SERVER_CONFIGURATION_FILE)
 #Using Terraform, initializes and deploys the server using the Terraform JSON file
    assert test_utils.initialize() == 0
    yield test_utils.apply()
 #Deletes the test server with Terraform and removes the JSON configuration file at the end of the test session
    assert test_utils.destroy() == 0
    os.remove(SERVER_CONFIGURATION_FILE)

#Pytest will run this test to verify that the output status of the changes has succeeded.
def test_changes_have_successful_return_code(apply_changes):
    return_code = apply_changes[0]
    assert return_code == 0

#Pytest will run this test to verify that the changes do not return with an error.
def test_changes_should_have_no_errors(apply_changes):
    errors = apply_changes[2]
    assert errors == b''

#Pytest will run this test and check that the configuration adds one resource, the server
def test_changes_should_add_1_resource(apply_changes):
    output = apply_changes[1].decode(encoding='utf-8').split('\n')
    assert 'Apply complete! Resources: 1 added, ' + \
        '0 changed, 0 destroyed' in output[-2]

#Pytest uses Libcloud to call the GCP API and get the server’s current state.
#It checks that the server is running.
def test_server_is_in_running_state(apply_changes):
    gcp_server = test_utils.get_server(TEST_SERVER_NAME)
    assert gcp_server.state == NodeState.RUNNING
