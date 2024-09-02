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


def check_repo_terms():
    pass

def look_for_new_terms():
    pass

def full_scan():
    pass


def dev_test():   
    for repo_url in get_repos_for_scan():
        print(repo_url)

dev_test()

