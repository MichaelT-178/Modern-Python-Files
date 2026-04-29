# NOTE: whois library functionality is pretty limited 

import requests
import json

domain = input("Enter a domain: ").strip().lower()
domain = domain.replace("https://", "").replace("http://", "").split("/")[0]

url = f"https://rdap.org/domain/{domain}"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers) #, timeout=3)

if res.status_code == 200:
    print(json.dumps(res.json(), indent=2))
else:
    print(f"Failed: {res.status_code}")