import requests
import json
import urllib3

from login_api import system_login, collect_args

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


EXAMPLE = [
    {
        "hostName": "r1",
        "ipAddress": "192.168.0.241",
        "regionId": "emea",
        "siteId": "abc",
    },
    {
        "hostName": "r2",
        "ipAddress": "192.168.0.242",
        "regionId": "emea",
        "siteId": "abc",
    },
    {
        "hostName": "r3",
        "ipAddress": "192.168.0.243",
        "regionId": "emea",
        "siteId": "abc",
    },
    {
        "hostName": "esw1",
        "ipAddress": "192.168.0.245",
        "regionId": "emea",
        "siteId": "abc",
    },
    {
        "hostName": "esw2",
        "ipAddress": "192.168.0.246",
        "regionId": "emea",
        "siteId": "abc",
    },
    {
        "hostName": "esw3",
        "ipAddress": "192.168.0.247",
        "regionId": "emea",
        "siteId": "abc",
    },
]


def upload_dynamic_devices(url, token):
    resp = requests.post(
        url=f"{url}/table_api/uploadDynamicDevices/",
        verify=False,
        headers={"Content-Type": "application/json"},
        data=json.dumps({"token": token, "records": EXAMPLE}),
        timeout=3,
    )
    print(resp.json())
    return resp


if __name__ == "__main__":
    arg_url, arg_username, arg_password, _ = collect_args()
    token = system_login(arg_url, arg_username, arg_password)
    upload_dynamic_devices(arg_url, token)
