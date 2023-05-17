class Module():
    #Creates a startup script that reconstructs the manual installation commands for the Cloud SQL Auth proxy
    def _startup_script(self):
        #Sets a variable as the proxy download URL
        proxy_download = 'https://dl.google.com/cloudsql/' + \
            'cloud_sql_proxy.linux.amd64'
        #Sets a variable that runs the Cloud SQL Auth proxy binary on port 3306
        exec_start = '/usr/local/bin/cloud_sql_proxy ' + \
            '-instances=${google_sql_database_instance.' + \
            f'{self._environment}.connection_name}}=tcp:3306'
        
        #Returns a shell script that installs the proxy and starts it up with the server
        return f"""
        #!/bin/bash
        wget {proxy_download} -O /usr/local/bin/cloud_sql_proxy
        chmod +x /usr/local/bin/cloud_sql_proxy
        
        #Configures the systemd daemon to start and stop the Cloud SQL Auth proxy
        cat << EOF > /usr/lib/systemd/system/cloudsqlproxy.service
        [Install]
        WantedBy=multi-user.target

        [Unit]
        Description=Google Cloud Compute Engine SQL Proxy
        Requires=networking.service
        After=networking.service

        [Service]
        Type=simple
        WorkingDirectory=/usr/local/bin
        ExecStart={exec_start}
        Restart=always
        StandardOutput=journal
        User=root
        EOF

        systemctl daemon-reload
        systemctl start cloudsqlproxy
        """
    #Uses the module to create the JSON configuration for the server
    def __init__(self, service, environment,
                 zone, machine_type='e2-micro'):
        self._name = f'{service}-{environment}'
        self._environment = environment
        self._zone = zone
        self._machine_type = machine_type

    #Uses the module to create the JSON configuration for the Google compute instance and includes a startup script to install the proxy
    def build(self):
        return [
            {
                #Creates the Google compute instance by using a Terraform resource based on the name, address, region, and network
                'google_compute_instance': {
                    self._environment: {
                        'allow_stopping_for_update': True,
                        'boot_disk': [{
                            'initialize_params': [{
                                'image': 'ubuntu-1804-lts'
                            }]
                        }],
                        'machine_type': self._machine_type,
                        'name': self._name,
                        'zone': self._zone,
                        'network_interface': [{
                            'subnetwork':
                            '${google_compute_subnetwork.' +
                            f'{self._environment}' + '.name}',
                            'access_config': {
                                'network_tier': 'STANDARD'
                            }
                        }],
                        #The factory for the promotions application’s server uses a service account to access GCP services.
                        'service_account': [{
                            'email': '${google_service_account.' +
                            f'{self._environment}' + '.email}',
                            'scopes': ['cloud-platform']
                        }],
                        'metadata_startup_script': self._startup_script()
                    }
                }
            }
        ]
