import requests
import json
import urllib3
import yaml

from args import collect_args

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def read_yaml():
    with open('device_example.yml', "r") as file:
        data = yaml.safe_load(file)
    return data


def upload_devices():
    url, token = collect_args()
    resp = requests.post(
        url=f"{url}/api/uploadDevices/",
        verify=False,
        headers={"Content-Type": "application/json", "Authorization": token},
        data=json.dumps({"token": token, "records": read_yaml()['EXAMPLE']}),
        timeout=5,
    )
    if resp.ok:
        print(resp.json())
    else:
        print(resp.text)


if __name__ == "__main__":
    upload_devices()
