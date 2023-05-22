# CCC-ass2-team6
Welcome to the CCC-ass2-team6 repository. This repository is set up to allow you to deploy a ubuntu instance in MRC, deployed couchDB instance, and Wordpress instance in your cloud, run a Mastodon harvester in docker container, and perform regular disk usage checks on your instance
# Getting Started
Follow the steps below to run the project.
# 1. Creating an Instance in your Cloud
First, navigate to the `ansible & docker/deploy_instance` directory.
```
cd ansible & docker/deploy_instance
```
Follow the instructions outlined in the README within this directory to create your instance.
# 2. Deploying Wordpress on your Instance
Next, navigate to the `ansible & docker/deploy_wordpress` directory.
```
cd ansible & docker/deploy_wordpress
```
# 3. Deploying the Mastodon Harvester
Once you have your instance set up with Wordpress, navigate to the `ansible & docker/harvester (crawler)` directory.
```
cd ansible & docker/harvester (crawler)
```
Follow the instructions in the README within this directory to deploy the Mastodon harvester.
# 4. Deploying the Disk Usage Check Script
Finally, navigate to the `ansible & docker/error_handling` directory.
```
cd ansible & docker/error_handling
```
Follow the instructions in the README within this directory to deploy the shell script that regularly checks disk usage in your instance. If disk usage reaches 90%, the script will stop the container from collecting data to prevent overload.
