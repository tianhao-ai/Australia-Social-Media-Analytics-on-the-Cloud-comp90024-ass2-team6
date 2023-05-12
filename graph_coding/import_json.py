import json
import requests

# Set the URL and credentials for the cloud database
url = "http://group6:123456@172.26.131.122:5984/education"
auth = ("group6", "123456")

# Open the file containing the JSON data
with open("output_file.json", "r") as f:
    # Read each line of the file and upload it to the cloud database
    for line in f:
        # Parse the line as a JSON object
        data = json.loads(line)
        # Upload the JSON object to the cloud database
        response = requests.post(url, auth=auth, json=data)
        # Check the response status code to confirm the upload was successful
        if response.status_code == 201:
            print("Uploaded successfully:", data)
        else:
            print("Upload failed:", response.text)