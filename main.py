import json
import os
import requests
import re
from bs4 import BeautifulSoup

def github_request(params):

    url = 'https://api.github.com/search/repositories' 

    search_response = requests.get(url, params=params)

    if search_response.status_code == 200:
        return search_response
    else:
        print(f"Search did not work, returned the following status code: {search_response.status_code}")
        return search_response.status_code

def repo_search(params, pages=1, repo_db_name="repos_info.json"):
    # This will simply search for all the repos with the query in it and write down the repo properties, like name, description, and link.
    # This can then be used later to search through repos README's and Codes look for terms and count them.

    if os.path.exists(repo_db_name):
        try:
            os.remove(repo_db_name)
        except:
            print("Removal of previous data did not work, please remove it manually.")
            print("Exiting Program...")
            exit()

    repos_info = []  # Move the repos_info list outside the loop to store results from all pages

    for page in range(1, pages + 1):  # Pages are 1-based, so loop should be 1 to pages
        params['page'] = page

        search_result = github_request(params)
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
                "url": item['html_url'],
                "term_count" : {}
            }
            if repo_info not in repos_info:  # Avoid adding duplicates
                repos_info.append(repo_info)
                print(f"{item['name']} appended to repo info json.")

    with open(repo_db_name, "w") as json_file:
        json.dump(repos_info, json_file, indent=4)
        print(f'Repository data has been dumped to "{repo_db_name}".')

def get_repo_url_list(repo_db_name="repos_info.json"):
    repo_url_list = []
    repo_db_name = "repos_info.json"

    with open(repo_db_name, "r") as file:
        repos_info_json = json.load(file)

    for repo in repos_info_json:
        repo_url_list.append(repo["url"])

    return repo_url_list

def basic_term_check(terms, repo_db_name="repos_info.json"):
    repo_url_list = get_repo_url_list()

    print(f"Scanning {len(repo_url_list)} repositories for terms.")

    term_occurrences = {}

    # Load the repository information
    with open(repo_db_name, "r") as repos_info_json:
        repos_info = json.load(repos_info_json)

    for repo in repos_info:
        repo_url = repo['url']
        response = requests.get(repo_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            repo_text = soup.get_text().lower()

            # Initialize 'term_count' in the repo dictionary if it doesn't exist
            if "term_count" not in repo:
                repo["term_count"] = {}

            for term in terms:
                term_count = repo_text.count(term.lower())
                
                # Update the term occurrences
                if term in repo["term_count"]:
                    repo["term_count"][term] += term_count
                else:
                    repo["term_count"][term] = term_count
        
        else:
            print(f"GET Request failed, Returned with status code: {response.status_code}")
        print(f"Scanned: ({repo_url})")

    # Save the updated repository information back to the JSON file
    with open(repo_db_name, "w") as json_file:
        json.dump(repos_info, json_file, indent=4)

    return term_occurrences

def advanced_term_check(repo_db_name="repos_info.json"):
    
    repo_url_list = get_repo_url_list()
    print(f"Scanning {len(repo_url_list)} repositories for terms.") 

    with open(repo_db_name, "r") as file:
        repos_info_json = json.load(file)

    for repo_url in repo_url_list:

        response = requests.get(repo_url)

        if response.status_code == 200:
            pass

        else:
            print(f"GET requests failed, returned with status_code: {response.status_code} \nExiting Program...")
            exit

        soup = BeautifulSoup(response.text, 'html.parser') 
        repo_text = soup.get_text().lower()



def find_paper_links(repo_db_name="repos_info.json"):
    repo_url_list = get_repo_url_list()

    with open(repo_db_name, "r") as file:
        repos_info_json = json.load(file)

    for repo in repos_info_json:
        repo_url = repo['url']

        response = requests.get(repo_url)

        if response.status_code == 200:
            pass
        else:
            print(f"GET requests failed, returned with status_code: {response.status_code} \nExiting Program...")
            exit
        soup = BeautifulSoup(response.text, 'html.parser')
        repo_text = soup.get_text().lower()

        pattern = r"http?://[^\s]+"

        links = re.findall(pattern, repo_text)

        terms_to_omit_with = ["license"]

        for link in links:
            for term in terms_to_omit_with:
                if term in link:
                    links.remove(link)
        
        if "paper_links" not in repo:
            repo["paper_links"] = {}
        
        x = 0 
        for link in links:
            x=1+x
            repo["paper_links"][x] = link
            print(f"({link}) added to database")

    with open(repo_db_name, "w") as json_file:
        json.dump(repos_info_json, json_file, indent=4)
    
def main(params, pages):
    repo_search(params=params, pages=pages)
    #advanced_term_check()
    find_paper_links()
    #basic_term_check([" CNN ", " Model ", " Architecture ", " U-Net" , " V-Net ", " MRI ", " CAT ", " ISLES ", " Dataset ", " ATLAS ", "2022"])

if __name__ == '__main__':
    query = "Stroke Segmentation"
    sort_by = "stars"

    params = {
        'q': query,
        'sort': sort_by,
        'order': 'desc',
        'type': 'repositories'
    }

    main(params, pages=1)
