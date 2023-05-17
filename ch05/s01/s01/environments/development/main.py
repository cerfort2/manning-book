import sys

#Imports directory with the modules because it exists in the same repository
sys.path.insert(1, '../../modules/gcp') 

# imports the server, database, and network factory modules for the production envrionment
from database import DatabaseFactoryModule
from server import ServerFactoryModule
from network import NetworkFactoryModule

import json


if __name__ == "__main__":
    environment = 'development'
    name = f'{environment}-hello-world'
    network = NetworkFactoryModule(name)
    server = ServerFactoryModule(name, environment, network)
    database = DatabaseFactoryModule(name, server, network, environment)
    resources = {
  #uses the modules to create the JSON configuration for the network, server, and database
        'resource': network.build() + server.build() + database.build()
    }

    #writes the python dictionary out to a json file to be executed by terraform later
    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile, sort_keys=True, indent=4)
