# Uploading the Twitter that contains the geo location to your couchdb

# 1. upload the Twitter that contains the geo location
The data uploaded in this part, would be a infrasture of any further analysis,
running the following code would start the uploading progress to your couchdb(it might takes long time):

To run the program, use the following command:

```mpiexec -n <num_processes> python mpi_upload_geo_tweet.py```

Replace `<num_processes>` with the number of processes you want to use for the computation

Here's an example of how to run the program with 2 processes about file <mpi_upload_geo_tweet.py>:

```mpiexec -n 2 python mpi_upload_geo_tweet.py```

If you cannot run the above command you could have tried following:

```mpirun -n 2 python mpi_upload_geo_tweet.py```

Or change `python` to `python3`

# 2. Uploading the data related to secenario
Once you have the full data that contains geo location, you might store some data that relate to secenario

And you can using similar method to upload the data

```mpiexec -n <num_processes> python <mpi_upload_file.py>```

You might want to change mpi_upload_file.py to `<mpi_upload_bad_word.py>` or `<mpi_upload_crime_data.py>`, 
that would upload the tweet contains bad words and tweet contains crime words to your couchDB
