import csv
import json
import random
from datetime import datetime, timedelta
def get_random_date():
    delta_days = random.randint(0, 60)
    random_date = datetime.now() - timedelta(days=delta_days)
    return random_date.strftime('%B %d, %Y').lower()


# List to hold the processed JSON data
json_data = []

# Read the CSV file
with open('keywords.json', 'r', encoding='utf-8') as file:
    file = json.load(file)
    for row in file:
        entry = row
        if 'content' in entry and 'date' not in entry['content']:
            entry['content']['date'] = get_random_date()
        json_data.append(entry)

# Save the processed data to a JSON file
with open('keywords.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)
