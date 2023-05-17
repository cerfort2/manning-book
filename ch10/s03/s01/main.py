import blue
import iam
import json
import os

if __name__ == "__main__":
    resources = {
        'resource': blue.build()
        + iam.build()
    }
    #Writes the Python dictionary out to a JSON file to be executed by Terraform later
    with open('main.tf.json', 'w') as outfile:
        json.dump(resources, outfile,
                  sort_keys=True, indent=4)
