import requests
from bs4 import BeautifulSoup
import json

url = "https://www.target.com/"
response = requests.get(url)

if response.status_code == 200:
    content = response.text
    soup = BeautifulSoup(content, 'html.parser')
    
    page_data = []

    for element in soup.find_all(text=True):

        text = element.strip()

        if text:
            tag = element.parent.name
            class_name = element.parent.get("class", [])

            if tag.lower() not in ['style', 'script']:
                page_data.append({
                    "text": text,
                    "tag": tag,
                    # "class": class_name
                })
    
    page_data_json = json.dumps(page_data, indent=4)
    
    print(page_data_json)
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")