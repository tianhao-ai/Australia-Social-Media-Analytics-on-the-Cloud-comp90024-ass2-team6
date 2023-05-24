import json

def load_elements_have_geo(file_path):
    
    sample_geo = []
    might_contains_geo = []

    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the opening square bracket '['
        file.readline()

        # Read the first object line
        line = file.readline().strip()

        index = 0
        while line:
            # Remove the trailing comma from the line if there is one
            if line.endswith(','):
                line = line[:-1]

            try:
                # Load JSON object from the line
                element = json.loads(line)

                geo_data = element['doc']['data'].get('geo', {})  # Use .get() method
                includes_data = element['doc'].get('includes', {}) # check whether it have includes
                
                if geo_data != {}:
                    sample_geo.append(element)
                elif includes_data != {}:
                    might_contains_geo.append(element)

            except json.JSONDecodeError as e:
                print(f"JSON decoding error at index {index}: {e}")

            # Read the next line
            line = file.readline().strip()

            # Increment the index
            index += 1
            if index % 1000000 == 0:
                print('current index:', index)
                break # remove this break to read whole json file

    return sample_geo, might_contains_geo

large_json_file = 'twitter-huge.json' # change to your path of huge tweet
tweet_have_geo, tweet_might_have_geo = load_elements_have_geo(large_json_file)
with open('upload_twitter_data/contain_geo_tweet.json', 'w') as f:
    for line in tweet_have_geo:
        json.dump(line, f)
        f.write('\n')