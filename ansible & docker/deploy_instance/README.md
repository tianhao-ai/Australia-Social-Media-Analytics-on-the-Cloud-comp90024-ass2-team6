# Ansible
## How to run
1. Navigate to the `host_vars`, here we assume you are in deploy_instance directory
```
cd host_vars
```
2. Changing necessary configuration in these three files
2.1 Changing configuration in `config.yaml`. In this file, you should change the file path where you stored your private keys to cloud, you should change your user name and password to couchdb, and make any other necessary changes to the variable naming
2.2 Changing configuration in `deploy.yaml`. In this file, you should change the name of the key and scurity group, or the configuration of the instances.
3. Deploy instances on the Nectar
    ```./deploy_instances_debug.sh```  
    ```./deploy_instances.sh```
4. Configure instances environments on the Nectar
    ```./configure_instances.sh```
5. generate hosts for applications  
    ```cd inventory```  
    when you in the inventory diretory, you should make changes in `application_hosts.ini`, and input your own IP address
4. Deploy CouchDB on the Nectar instances
    ```
    ./deploy_db_and_crawler.sh
    ```
Deployment of CouchDB and instances are finished!
# NOTE
Below, is the function that removed your deploy instances, run it if you need
5. Remove instances on the Nectar
    - ```./remove_deploy_instances.sh```

