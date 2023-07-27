# Note
Hi, I am one of the contributors from the repository https://github.com/Wen20011009/CCC-ass2-team6, and this repository is the fork version, which is aimed at doing some improvements from the original works.
# Cluster and Cloud Computing Assignment 2 - Australia Social Media Analytics on the Cloud
Welcome to the CCC-ass2-team6 repository. This repository is set up to allow you to deploy a ubuntu instance in MRC, deployed couchDB instance, and Wordpress instance in your cloud, run a Mastodon harvester in docker container, and perform regular disk usage checks on your instance. 
After deployed all necessary container, some python script could be help to produce some useful analysis of stream data and Twitter historical data, and the python script contains MapReduce function would help to distributed task of analysis into multiple process.
In addition, we also have necessary file that store the HTML and Javascript of the website.
At last, you are more than welcome to check our video in youtube to gain further understanding of this project: https://youtu.be/EBhZff-8_gI
# Getting Started
Before getting start, ensure you read the `requirements.txt` , and have necessary package
In planning stage, our initial deployment were planned as following picture:
<img src="Graph/pipeline.png" alt="pipeline" title="System Architecture">
# 1. Creating an Instance in your Cloud
In planning stage, the deployment of instance use following configuration:
<img src="Graph/instance_config.png" alt="deployment config" title="System Architecture">
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
Once you have your instance set up with Wordpress, navigate to the `harvester (crawler)` directory.
```
cd harvester (crawler)
```
Follow the instructions in the README within this directory to deploy the Mastodon harvester.
After the deployment of above 3 stages, your node might works like below:
<img src="Graph/instance_connect.png" alt="instance connection" title="System Architecture">
# 4. Deploying the Disk Usage Check Script(optional)
Finally, navigate to the `ansible & docker/error_handling` directory.
```
cd ansible & docker/error_handling
```
Follow the instructions in the README within this directory to deploy the shell script that regularly checks disk usage in your instance. If disk usage reaches 90%, the script will stop the container from collecting data to prevent overload.
# 5. Uploading the data to couchdb or creating any necessary analysis
Finally, navigate to the `data_processing_mapreduce & upload_to_couchdb` directory.
```
cd data_processing_mapreduce & upload_to_couchdb
```
Follow the instructions in the README within this directory.
# 6. Extracting the grouping data could plot the graph
navigate to the `graph_coding` directory. 
```
cd graph_coding
```
Following the readme in the folder would created the necessary data to plotting graph
# 7. LDA Model
Running from top to down of the file `Model/LDA_bad_word.ipynb` would generate the `result` file
which could visualized a cluster of topic.
# Other files
Some other folders might not documented above, and their functionality would listed below:
* `frontend` : since we using wordpress for our website application, so only the file we additionly use to produce extra functionality in website would put in here
* `SUDO_Data`: These file is for placing the file we collected from sudo
* `report`: These file would be used to placed our final report
# Acknowledgments
This program was created as a project for COMP90024 Cluster and Cloud Computing at University of Melbourne. Special thanks to teaching teams :Prof.Richard Sinnott, Researchers Yao (Alwyn) Pan, Cloud Architect Luca Morandini and other staff for their guidance and support.
