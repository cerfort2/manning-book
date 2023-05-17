TEAM = 'sundew'
ENVIRONMENT = 'production'
VERSION = 'passive' #Sets the version to identify the passive environment
REGION = 'us-west1' #Changes the region from us-central1 to us-west1 for the passive environment
IP_RANGE = '10.0.1.0/24' #Updates a different IP address range for the passive environment to avoid sending requests

zone = f'{REGION}-a'
network_name = f'{TEAM}-{ENVIRONMENT}-network-{VERSION}'

#Remaining variables and functions reference the constants for the passive environment, including region.
server_name = f'{TEAM}-{ENVIRONMENT}-server-{VERSION}'

cluster_name = f'{TEAM}-{ENVIRONMENT}-cluster-{VERSION}'
cluster_nodes = f'{TEAM}-{ENVIRONMENT}-cluster-nodes-{VERSION}'
cluster_service_account = f'{TEAM}-{ENVIRONMENT}-sa-{VERSION}'

#Defines labels for resources so you can identify the production environment
labels = {
    'team': TEAM,
    'environment': ENVIRONMENT,
    'automated': True
}


def build():
    return network() + \
        cluster() + \
        server0() + \
        server1() + \
        server2()


def network(name=network_name,
            region=REGION,
            ip_range=IP_RANGE):
    return [
        {
            'google_compute_network': {
                VERSION: [{
                    'name': name,
                    'auto_create_subnetworks': False
                }]
            }
        },
        {
            'google_compute_subnetwork': {
                VERSION: [{
                    'name': f'{name}-subnet',
                    'region': region,
                    'network': f'${{google_compute_network.{VERSION}.name}}',
                    'ip_cidr_range': ip_range
                }]
            }
        }
    ]


def cluster(name=cluster_name,
            node_name=cluster_nodes,
            service_account=cluster_service_account,
            region=REGION):
    return [
        {
            'google_container_cluster': {
                VERSION: [
                    {
                        'initial_node_count': 1,
                        'location': region,
                        'name': name,
                        'remove_default_node_pool': True,
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
                                'machine_type': 'e2-medium',
                                'oauth_scopes': [
                                    'https://www.googleapis.com/auth/cloud-platform'
                                ],
                                'preemptible': True,
                                'service_account': f'${{google_service_account.{VERSION}.email}}'
                            }
                        ],
                        'node_count': 1
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


def server0(name=f'{server_name}-0',
            zone=zone):
    return [
        {
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
                            'network_tier': 'STANDARD'
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
                            'network_tier': 'STANDARD'
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
                            'network_tier': 'STANDARD'
                        }
                    }],
                    'labels': labels
                }]
            }
        }
    ]
