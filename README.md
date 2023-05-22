# CCC-ass2-team6
CCC-ass2-team6
Welcome to the GitHub repository for our project, CCC-ass2-team6. This repository contains code for deploying an instance on your cloud, deploying Wordpress on this instance, and implementing a Mastodon harvester. There's also a shell script for error handling to monitor the disk usage in your instance.

Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites
A cloud instance (The specific requirements will be detailed in the specific README files)
Docker and Ansible installed on your machine
Installation
Follow the steps below to set up and run our project.

Step 1: Creating the Cloud Instance
Navigate to the directory:

cd CCC-ass2-team6/ansible & docker/deploy_instance
Here, you will find a README file with detailed instructions on how to set up the cloud instance. Make sure to follow these instructions carefully.

Step 2: Deploying Wordpress on the Instance
Navigate to the directory:

cd CCC-ass2-team6/ansible & docker/deploy_wordpress
This directory contains a README file with instructions for deploying Wordpress on your instance. Follow these instructions to complete this step.

Step 3: Deploying the Mastodon Harvester
Navigate to the directory:

cd CCC-ass2-team6/ansible & docker/harvester (crawler)
In this directory, you'll find a README file with instructions on deploying the Mastodon harvester on your instance. Make sure to follow these instructions.

Step 4: Implementing Error Handling
Navigate to the directory:

cd CCC-ass2-team6/ansible & docker/error_handling
Here, there is a README file with instructions to deploy the shell script for error handling. This script performs regular checks of disk usage in your instance. If your disk usage reaches 90%, the script will stop the container from collecting data.

Contributing
We encourage you to contribute to this project! Please check out the Contributing to CCC-ass2-team6 guide for guidelines about how to proceed.

Support
If you're having trouble with the project, please open an issue in the GitHub Repository or contact us directly. We’ll try to solve it as soon as possible.

Authors
CCC-ass2-team6 Team - Initial work

