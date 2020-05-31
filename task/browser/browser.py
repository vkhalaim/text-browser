import sys
import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore


def is_valid_url(url):
    return len(url.split('.')) > 1


def get_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    res = []
    for item in soup.find_all(['p', 'a', 'ul', 'ol', 'li']):
        if item in soup.find_all('a'):
            res.append(Fore.BLUE + item.get_text())
        else:
            res.append(item.get_text())

    return "".join(res)


def print_file(path):
    with open(path, 'r') as f:
        for line in f:
            print(line, end="")


dir_name = sys.argv[1]
current_path = os.getcwd()
dir_path = current_path + '\\' + dir_name

if not os.path.exists(dir_path):
    os.mkdir(dir_path)

cache = dict()

user_input = ''

while True:
    user_input = input()

    if user_input == 'exit':
        break

    if is_valid_url(user_input):

        hostname = user_input.split(".", 1)[0]

        try:
            if "http://" not in user_input:
                user_input = "http://" + user_input
            response = requests.get(user_input)
        except requests.ConnectionError as exception:
            print("Error: Incorrect URL")
            continue

        text = get_content(response.text)

        path_to_file = dir_path + '\\' + hostname + ".html"

        with open(path_to_file, "w") as f:
            f.writelines(text)
            cache[hostname] = path_to_file

        print_file(path_to_file)

    elif user_input in cache:
        print_file(cache[user_input])
    else:
        print("Error: Incorrect URL")
