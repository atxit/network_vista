import json
import argparse
import sys
import getpass
import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def collect_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", default=None, help="https://URL")
    parser.add_argument("-u", default=None, help="username")
    parser.add_argument("-p", default=None, help="username")
    parser.add_argument("-db", default=None, help="DataBase Name")
    args = parser.parse_args(sys.argv[1:])
    if args.l is None:
        url = input("URL:")
    else:
        url = args.l
    if args.u is None:
        username = input("username:")
    else:
        username = args.u
    if args.p is None:
        password = getpass.getpass("password:")
    else:
        password = args.p

    if len(password) == 0 and len(username) == 0 and len(url) == 0:
        sys.exit(1)
    return url, username, password, args.db


def system_login(url, username, password):
    try:
        response = requests.post(
            url=f"{url}/table_api/login/",
            verify=False,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"username": username, "password": password}),
            timeout=3,
        )
    except requests.exceptions.InvalidURL:
        print(f"URL failure: {url}")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print(f"URL timed out: {url}")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"URL failure: {url}")
        sys.exit(1)
    if response.ok:
        print('login successful')
        return response.json().get("token")
    elif response.status_code == 400:
        print("username or password error")
        sys.exit(1)
    else:
        print(response.text)

if __name__ == "__main__":
    url, username, password, db_name = collect_args()
    system_login(url, username, password)
