TEAM = 'sundew'
ENVIRONMENT = 'production'
VERSION = 'green' #Sets the name of the new network version to “green”
REGION = 'us-central1'
IP_RANGE = '10.0.0.0/24' #Keeps the IP address range for green the same as the blue network. GCP allows the two networks to have the same CIDR block if you have not set up peering.

zone = f'{REGION}-a'

#Uses the module to create the JSON configuration for the network and subnetwork for the green network
network_name = f'{TEAM}-{ENVIRONMENT}-network-{VERSION}'

#Creates a template for the server name, which includes the team, environment, and version (blue or green)
server_name = f'{TEAM}-{ENVIRONMENT}-server-{VERSION}'

#Labels the new version of the cluster “green”
cluster_name = f'{TEAM}-{ENVIRONMENT}-cluster-{VERSION}'
cluster_nodes = f'{TEAM}-{ENVIRONMENT}-cluster-nodes-{VERSION}'
cluster_service_account = f'{TEAM}-{ENVIRONMENT}-sa-{VERSION}'


labels = {
    'team': TEAM,
    'environment': ENVIRONMENT,
    'automated': True
}

#Uses the module to create the JSON configuration for the network, subnetwork, cluster, and server for the green network
def build(): 
    return network() + \
        server0() + \
        server1() + \
        server2()


def network(name=network_name,
            region=REGION,
            ip_range=IP_RANGE):
    return [
        {
            'google_compute_network': { #Creates the Google network by using a Terraform resource based on the name and a global routing mode
                VERSION: [{
                    'name': name,
                    'auto_create_subnetworks': False,
                    'routing_mode': 'GLOBAL' #Updates the green network’s routing mode to global to expose routes globally
                }]
            }
        },
        {
            'google_compute_subnetwork': { #Creates the Google subnetwork by using a Terraform resource based on the name, region, network, and IP address range
                VERSION: [{
                    'name': f'{name}-subnet',
                    'region': region,
                    'network': f'${{google_compute_network.{VERSION}.name}}',
                    'ip_cidr_range': ip_range
                }]
            }
        }
    ]

#Passes required attributes to the cluster, including name, node names, service accounts for automation, and region
def cluster(name=cluster_name,
            node_name=cluster_nodes,
            service_account=cluster_service_account,
            region=REGION):
    return [
        {
            #Creates the Google container cluster by using a Terraform resource with one node and on the green network
            'google_container_cluster': {
                VERSION: [
                    {
                        'initial_node_count': 1,
                        'location': region,
                        'name': name,
                        'remove_default_node_pool': True,
                        #Builds the cluster on the green network and subnetwork
                        'network': f'${{google_compute_network.{VERSION}.name}}',
                        'subnetwork': f'${{google_compute_subnetwork.{VERSION}.name}}'
                    }
                ]
            },
            'google_container_node_pool': {
                VERSION: [
                    {
                        'cluster': f'${{google_container_cluster.{VERSION}.name}}',
                        'location': region,
                        'name': node_name,
                        'node_config': [
                            {
                                'machine_type': 'e2-micro',
                                'oauth_scopes': [
                                    'https://www.googleapis.com/auth/cloud-platform'
                                ],
                                'preemptible': True,
                                'service_account': f'${{google_service_account.{VERSION}.email}}'
                            }
                        ],
                        'node_count': 0
                    }
                ]
            },
            'google_service_account': {
                VERSION: [
                    {
                        'account_id': service_account,
                        'display_name': service_account
                    }
                ]
            }
        }
    ]

#Copies and pastes each server configuration. This code snippet features the first server, server0. Other server configurations are omitted for clarity.
def server0(name=f'{server_name}-0',
            zone=zone):
    return [
        {
            #Creates a small Google compute instance (server) by using a Terraform resource on the green network
            'google_compute_instance': {
                f'{VERSION}_0': [{
                    'allow_stopping_for_update': True,
                    'boot_disk': [{
                        'initialize_params': [{
                            'image': 'ubuntu-1804-lts'
                        }]
                    }],
                    'machine_type': 'e2-micro',
                    'name': name,
                    'zone': zone,
                    'network_interface': [{
                        'subnetwork': f'${{google_compute_subnetwork.{VERSION}.name}}',
                        'access_config': {
                            #Sets the network tier to use premium networking. This enables compatibility with the underlying subnet, which uses global routing.
                            'network_tier': 'PREMIUM'
                        }
                    }],
                    'labels': labels
                }]
            }
        }
    ]


def server1(name=f'{server_name}-1',
            zone=zone):
    return [
        {
            'google_compute_instance': {
                f'{VERSION}_1': [{
                    'allow_stopping_for_update': True,
                    'boot_disk': [{
                        'initialize_params': [{
                            'image': 'ubuntu-1804-lts'
                        }]
                    }],
                    'machine_type': 'e2-micro',
                    'name': name,
                    'zone': zone,
                    'network_interface': [{
                        'subnetwork': f'${{google_compute_subnetwork.{VERSION}.name}}',
                        'access_config': {
                            'network_tier': 'PREMIUM'
                        }
                    }],
                    'labels': labels
                }]
            }
        }
    ]


def server2(name=f'{server_name}-2',
            zone=zone):
    return [
        {
            'google_compute_instance': {
                f'{VERSION}_2': [{
                    'allow_stopping_for_update': True,
                    'boot_disk': [{
                        'initialize_params': [{
                            'image': 'ubuntu-1804-lts'
                        }]
                    }],
                    'machine_type': 'e2-micro',
                    'name': name,
                    'zone': zone,
                    'network_interface': [{
                        'subnetwork': f'${{google_compute_subnetwork.{VERSION}.name}}',
                        'access_config': {
                            'network_tier': 'PREMIUM'
                        }
                    }],
                    'labels': labels
                }]
            }
        }
    ]
