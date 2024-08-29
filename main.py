import requests
import os
import shutil
import json

search_urls_dict = {

        'repos' : 'https://api.github.com/search/repositories?q='
        }

query = "dumprun"
test_response = requests.get(search_urls_dict["repos"]+query)

if test_response.status_code == 200:
    response = test_response.json()
    print(response)

else:
    print(f"Didn't Work, Response code: {test_response.status_code}")
