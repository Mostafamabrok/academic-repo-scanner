import requests
import os
import json

def search(params):
        
    url = 'https://api.github.com/search/repositories' 

    search_response = requests.get(url, params=params)

    if search_response.status_code == 200:
        return search_response
    else:
        print(f"Search did not work, returned the following status code: {search_response.status_code}")
        return search_response.status_code

def basic_repo_search(params, pages=2):
    # This will simply search for all the repos with the query in it and write down the repo properties, like name, description, and link.
    # This can then be used later to search through repos README's and Codes look for terms and count them.

    if os.path.exists("repos_info.json"):
        try:
            os.remove("repos_info.json")
        except:
            print("Removal of previous data did not work, please remove it manually.")
            print("Exiting Program...")
            exit()

    repos_info = []  # Move the repos_info list outside the loop to store results from all pages

    for page in range(1, pages + 1):  # Pages are 1-based, so loop should be 1 to pages
        params['page'] = page

        search_result = search(params)
        if isinstance(search_result, int):
            print(f"ERROR: Could not perform search, returned status code: {search_result}")
            print("Exiting Program...")
            exit()

        try:
            search_response = search_result.json()
        except AttributeError:
            print("You have likely made too many requests in a short period of time. Wait some time and try again.")
            print("Exiting Program...")
            exit()

        items = search_response.get('items', [])

        for item in items:
            repo_info = {
                "title": item['name'],
                "url": item['html_url']
            }
            if repo_info not in repos_info:  # Avoid adding duplicates
                repos_info.append(repo_info)
                print(f"{item['name']} appended to repo info json.")

    with open("repos_info.json", "w") as json_file:
        json.dump(repos_info, json_file, indent=4)
        print("JSON data has been dumped.")

def main(params, pages):
    basic_repo_search(params=params, pages=pages)

if __name__ == '__main__':
    query = "Stroke Segmentation"
    sort_by = ""

    params = {
        'q': query,
        'sort': sort_by,
        'order': 'desc',
        'type': 'repositories'
    }

    main(params, pages=1)




