import sys
import time
import urllib3
import requests
import json
from args import collect_args
from pprint import pprint
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

### Example Search Query ###
#self.search_query = {"release": "fc2"}


class QueryTable:
    def __init__(self):
        self.rows_per_response = 50
        self.url, self.token, self.db, self.query, self.pprint = collect_args()
        self.query = self.query.replace("'",'"')
        try:
            self.query = json.loads(self.query)
        except json.decoder.JSONDecodeError as msg:
            print(msg)
            sys.exit(1)

    def execute_query(self):
        table_result = []
        run_query = True
        current_page = 1
        while run_query:
            resp = requests.post(
                url=f"{self.url}/api/query_table/",
                verify=False,
                headers={"Content-Type": "application/json", "Authorization": self.token},
                data=json.dumps(
                    {
                        "token": self.token,
                        "db": self.db,
                        "currentPage": current_page,
                        "numberOfRows": self.rows_per_response,
                        "searchDict": self.query,
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
                    return table_result, self.pprint
                current_page += 1
                time.sleep(1)
        return table_result, self.pprint

def main():
    query_table = QueryTable()
    result, print_pprint = query_table.execute_query()
    if len(result) == 0:
        print('no results')
        sys.exit(0)
    if print_pprint:
        pprint(result)
        sys.exit()
    for ele in result:
        print(ele)


if __name__ == "__main__":
    main()
