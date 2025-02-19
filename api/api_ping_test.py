import urllib3
import requests
from args import collect_args

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def ping_test():
    url, token = collect_args()
    url += '/api/ping/'
    headers = {"Content-Type": "application/json", "Authorization": token}
    response = requests.post(url=url, headers=headers)
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Error:", response.status_code, response.text)


if __name__ == "__main__":
    ping_test()