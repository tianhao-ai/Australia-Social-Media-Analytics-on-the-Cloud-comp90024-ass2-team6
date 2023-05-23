# This page is about the deployment of Mastodon Harvester
Following the instruction in this page, you would deploy your python script in docker container to the instance you want, and it could continually collecting the stream data to CouchDB

# 1.Changing configuration
Open the `inventory.ini`, then changing IP address, and the place that store you private keys

# 2.Harvester Deployment
running the following command in your command line would deployed the harvester:
```
./deploy_crawler.sh
```
# 3. Some optional shell script
we also prepare the shell script like `remove_harvester.sh`, `restart_harvester.sh`, `stop_havester.sh`, and be careful to use them
