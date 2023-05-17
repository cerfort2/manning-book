import pytest
#Imports the list of GCP users and roles
from main import GCP_PROJECT_USERS, GCPProjectUsers

#Uses Python to read in the Terraform JSON configuration file. The test uses this fixture to verify that the JSON has an indentation of four spaces.
GROUP_CONFIGURATION_FILE = 'main.tf.json'


@pytest.fixture
def json():
    with open(GROUP_CONFIGURATION_FILE, 'r') as f:
        return f.readlines()

#Imports the list of GCP users and roles, including the inventory team, as a fixture to the test. 
#The test checks that each user has a prefix of “team-” to identify it as a group.
@pytest.fixture
def users():
    return GCP_PROJECT_USERS

#Uses a fixture to create a sample GCP project user using the factory module
@pytest.fixture
def binding():
    return GCPProjectUsers(
        'testing',
        [('test', 'test', 'roles/test')]).resources['resource'][0]

#Uses Python to read in the Terraform JSON configuration file. The test uses this fixture to verify that the JSON has an indentation of four spaces.
def test_json_configuration_for_indentation(json):
    assert len(json[1]) - len(json[1].lstrip()) == 4, \
        "output JSON with indent of 4"

#Imports the list of GCP users and roles, including the inventory team, as a fixture to the test. 
#The test checks that each user has a prefix of “team-” to identify it as a group.
def test_user_configuration_for_standard_team_name(users):
    for _, member, _ in GCP_PROJECT_USERS:
        assert member.startswith('team-'), \
            "group should always start with `team-`"

#Uses a fixture to create a sample GCP project user using the factory module
def test_authoritative_project_iam_binding(binding):
    #Checks that the factory module uses the correct Terraform resource of Google project IAM binding and not members. 
    #This uses an authoritative binding to add team members to a specific role
    assert 'google_project_iam_binding' in binding.keys(), \
        "use `google_project_iam_binding` to add team members to roles"
