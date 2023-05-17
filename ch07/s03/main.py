# Note: This example will not apply successfully
# with Terraform because it uses mock users and
# groups. However, it will successfully pass a plan.

import json

#Defines a list of users and groups to add to the GCP project
GCP_PROJECT_USERS = [
    (
        'operations',
        'group:team-operations@example.com',
        'roles/editor'
    ),
    (
        #Adds the inventory team as a read-only group to the project
        'inventory',
        'group:inventory@example.com',
        'roles/viewer'
    )
]

#Creates a module for the GCP project users, which uses the factory pattern to attach users to roles
class GCPProjectUsers:
    def __init__(self, project, users):
        self._project = project
        self._users = users
        self.resources = self._build()
#Uses the module to create the JSON configuration for the list of users to append to GCP roles
    def _build(self):
        resources = []
        #For each group in the list, creates a Google project IAM member with the user attached to their assigned role. 
        #This resource appends the user to the roles in GCP
        for user, member, role in self._users:
            resources.append({                     
                'google_project_iam_member': [{
                    user: [{
                        'role': role,
                        'member': member,
                        'project': self._project
                    }]
                }]
            })
        return {
            'resource': resources
        }


if __name__ == "__main__":
    #Writes the Python dictionary out to a JSON file to be executed by Terraform later
    with open('main.tf.json', 'w') as outfile:
        json.dump(GCPProjectUsers(
            'infrastructure-as-code-book',
            GCP_PROJECT_USERS).resources, outfile,
            sort_keys=True, indent=2) 
        #When you write out the JSON file to be executed by Terraform, use an indentation of two spaces
