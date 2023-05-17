from tags import StandardTags
from server import ServerFactoryModule
from network import NetworkFactoryModule        #imports the modules downloaded by the package manager
from database import DatabaseFactoryModule

import json

if __name__ == "__main__":
    environment = 'development'
    name = f'{environment}-hello-world'

    tags = StandardTags(environment)
    network = NetworkFactoryModule(name)
    server = ServerFactoryModule(name, environment, network, tags.tags)
    database = DatabaseFactoryModule(
        name, server, network, environment, tags.tags)
    resources = {
  #uses the modules to create the JSON configuration for the network, server, and database
        'resource': network.build() + server.build() + database.build()
    }

    with open('main.tf.json', 'w') as outfile:
        #writes the python dictionary out to a JSON file to be executed by terraform later
        json.dump(resources, outfile, sort_keys=True, indent=4)
