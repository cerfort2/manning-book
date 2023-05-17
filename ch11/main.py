import os
import database #Imports the database module to build the Google Cloud SQL database
import iam #Imports the Google service account module and creates the configuration with the permissions
import network #Imports the network module to build the Google network and subnetwork
import server #Imports the server module to build the Google compute instance
import json
import os

SERVICE = 'promotions'
ENVIRONMENT = 'prod'
REGION = 'us-central1'
ZONE = 'us-central1-a'
PROJECT = os.environ['CLOUDSDK_CORE_PROJECT']
role = 'roles/cloudsql.client' #Promotions service account should have permission for the “cloudsql.admin” role to access the database

if __name__ == "__main__":
    #Uses the module to create the JSON configuration for the database, network, service account, and server
    resources = {
        'resource':
        network.Module(SERVICE, ENVIRONMENT, REGION).build() + #Imports the network module to build the Google network and subnetwork
        iam.Module(SERVICE, ENVIRONMENT, REGION, PROJECT, #Imports the Google service account module and creates the configuration with the permissions
                   role).build() +
        database.Module(SERVICE, ENVIRONMENT, REGION).build() + #Imports the database module to build the Google Cloud SQL database
        server.Module(SERVICE, ENVIRONMENT, ZONE).build() #Imports the server module to build the Google compute instance
    }

    #Writes out the Python dictionary to a JSON file to be executed by Terraform later
    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile,
                  sort_keys=True, indent=4)
