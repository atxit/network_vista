import requests
import json
import urllib3
import yaml

from login_api import system_login, collect_args

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def read_yaml():
    with open('device_example.yml', "r") as file:
        data = yaml.safe_load(file)
    return data


def upload_dynamic_devices(url, token):
    resp = requests.post(
        url=f"{url}/table_api/uploadDynamicDevices/",
        verify=False,
        headers={"Content-Type": "application/json"},
        data=json.dumps({"token": token, "records": read_yaml()['EXAMPLE']}),
        timeout=3,
    )
    return resp


if __name__ == "__main__":
    arg_url, arg_username, arg_password, _ = collect_args()
    session_token = system_login(arg_url, arg_username, arg_password)
    upload_dynamic_devices(arg_url, session_token)
