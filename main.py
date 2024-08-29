import requests
import os
import shutil
import json


def api_test():
    urls_dict = {

        'repos' : 'https://api.github.com/search/repositories?q='
        }

    query = "dumprun"
    test_response = requests.get(urls_dict["repos"]+query)

    if test_response.status_code == 200:
        response = test_response.json()
        print(response)

    else:
        print(f"Didn't Work, Response code: {test_response.status_code}")

def setup_boilerplate():
    global search

    urls_dict = {
        'repos' : 'https://api.github.com/search/repositories?q='
    }

    def search(query):
        search_response = requests.get(urls_dict["repos"]+query)

        if search_response.status_code == 200:
            return search_response

        else:
            print(f"Search did not work, returned following status code: {search_response.status_code}")
            return 0

def basic_repo_search(query):
    #This will simply search for all the repos with the query in it and write down the repo properties, like name, description, and link.
    #This can then be used later to search through repos README's and Codes look for terms and count them.
    #CURRENTLY, does not serve this function and is just used for testing, once this line is removed that means it is serving this function.
    print(search(query).json())


def main(query):
    setup_boilerplate()
    basic_repo_search(query)

main("dumprun")
