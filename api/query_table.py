import time
import urllib3
import requests
import json

from api.login_api import system_login, collect_args

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

### Example Search Query ###
#self.search_query = {"release": "fc2"}


class QueryTable:
    def __init__(self, url, token, db_name, rows_per_response=50, search_query=None):
        self.token = token
        self.url = url
        self.db_name = db_name
        self.rows_per_response = rows_per_response
        
        if search_query is None:
            self.search_query = {}
        if isinstance(search_query, dict):
            self.search_query = search_query
        else:
            self.search_query = {}

    def execute_query(self):
        table_result = []
        run_query = True
        current_page = 1
        while run_query:
            resp = requests.post(
                url=f"{self.url}/table_api/query_table/",
                verify=False,
                headers={"Content-Type": "application/json"},
                data=json.dumps(
                    {
                        "token": self.token,
                        "db": self.db_name,
                        "currentPage": current_page,
                        "numberOfRows": self.rows_per_response,
                        "searchDict": self.search_query,
                    }
                ),
                timeout=20,
            )
            if resp.ok:
                result_dict = resp.json()
                table_result.extend(result_dict["table"])
                if (
                    result_dict["totalRows"] == 0
                    or result_dict["displayedRows"] == result_dict["totalRows"]
                ):
                    return table_result
                current_page += 1
                time.sleep(1)


if __name__ == "__main__":
    arg_url, arg_username, arg_password, arg_db_name = collect_args()
    token = system_login(arg_url, arg_username, arg_password)
    query_table = QueryTable(arg_url, token, arg_db_name)
    print(query_table.execute_query())
