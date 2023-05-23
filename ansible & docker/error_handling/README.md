# Disk Management
This page is to run a daily cron job on the instance that you want to do the Disk storage check, but this shell script assume you have a running container about a Mastodon Harvester.
# 1. Changing configuration
changing the IP address in the `host.ini`, and the file path of the key
# 2. Deploy the Disk management
Running the shell script would perform disk management on the specific instances
```
./run_disk_monitor.sh
```
