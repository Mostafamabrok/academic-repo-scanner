import os
import requests
import json
from bs4 import BeautifulSoup

def get_repos_for_scan():
    repo_url_list = []

    with open("repos_info.json", "r") as file:
        repos_info_json = json.load(file)

    for repo in repos_info_json:
        repo_url_list.append(repo["url"])

    return repo_url_list


def basic_term_check(terms):

    repo_url_list = get_repos_for_scan()
    
    print(f"Scanning {len(repo_url_list)} repositories for terms.")

    term_occurrences = {}

    for repo_url in repo_url_list:
        response = requests.get(repo_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            repo_text = soup.get_text().lower()

            for term in terms:
                if term in term_occurrences:
                    term_occurrences[term] = term_occurrences[term] + repo_text.count(term.lower())
                else: 
                    term_occurrences[term] = repo_text.count(term.lower())

        else:
            print(f"Request didn't come through, status_code: {response.status_code}")

        print(f"Scanned: ({repo_url})")

    return term_occurrences

def advanced_term_check(terms):
    pass

def look_for_new_terms():
    pass

def full_scan():
    pass


def dev_test():   
    print("\n")
    print(basic_term_check(["CNN", "U-net", "Chinese"]))

dev_test()

