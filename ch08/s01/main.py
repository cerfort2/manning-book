import json
import iam
import os
#Creates the role configuration based on a list of roles for a service account, including networking, App Engine, and Cloud SQL


def build_frontend_configuration():
    name = 'frontend'
    roles = [
        'roles/compute.networkAdmin',#Imports the application access management factory module to create access management roles for the frontend application
        'roles/appengine.appAdmin',
        'roles/cloudsql.admin'
    ]
    project = os.environ['CLOUDSDK_CORE_PROJECT']

    frontend = iam.ApplicationFactoryModule(name, roles, project)
    resources = {
        'resource': frontend._build()
    }
    return resources
#Uses the method to create the JSON configuration for the pipeline’s access permissions

if __name__ == "__main__":
    resources = build_frontend_configuration()

    #Writes the Python dictionary out to a JSON file to be executed by Terraform later
    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile, sort_keys=True, indent=4)
