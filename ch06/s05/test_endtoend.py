from main import generate_json, SERVICE_CONFIGURATION_FILE
import os
import pytest
import requests
import test_utils
#Using Terraform, initializes and deploys the service using the Terraform JSON file

TEST_SERVICE_NAME = 'hello-world-test'

#During the test session, uses a pytest test fixture to apply the configuration and create a test service on GCP
@pytest.fixture(scope='session')
def apply_changes():
    generate_json(TEST_SERVICE_NAME)    #Generates a Terraform JSON file that uses the GCP Cloud Run module
    assert os.path.exists(SERVICE_CONFIGURATION_FILE)
    assert test_utils.initialize() == 0 #During the test session, uses a pytest test fixture to apply the configuration and create a test service on GCP
    yield test_utils.apply()
    assert test_utils.destroy() == 0
    os.remove(SERVICE_CONFIGURATION_FILE)#Destroys the GCP Cloud Run service in the testing environment, so you do not have a persistent service in your GCP project

#Uses a pytest fixture to parse the output of the configuration for the service’s URL
@pytest.fixture
def url():
    output, error = test_utils.output('url')
    assert error == b''
    service_url = output.decode(encoding='utf-8').split('\n')[0]
    return service_url

#In the test, makes an API request to the service’s URL using Python’s requests library
def test_url_for_service_returns_running_page(apply_changes, url):
    response = requests.get(url)
    assert "It's running!" in response.text 
    #In the test, checks the service’s URL response containing a specific string to indicate the service is running
