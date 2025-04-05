import json
import requests

# make an HTTP request to get the data
url = "https://ohrghyoie8.execute-api.us-east-1.amazonaws.com/comet-scouting/submit"
request_id = "jm3jvtg47zAi9zED8j784DncF3K9kLy0cXvhLvWBjNA8nNGnV5ZySywG3iu3"

print("Processing request...")

response = requests.get(f"{url}?id={request_id}")

print("Request received.")

file_path = "aws-data.json"

with open(file_path, 'w') as json_file:
  aws_data = json.dump(response.json(), json_file, indent=2)

print(f"Data written to {file_path}.")
