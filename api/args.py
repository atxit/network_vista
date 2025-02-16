import argparse
import sys
from getpass import getpass


def collect_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", default=None, help="URL: https://URL")
    parser.add_argument("-t", default=None, help="token")
    parser.add_argument("-d", default=None, help="database/table name")
    parser.add_argument("-q", default=None, help='search JSON {"release": "fc2"}')
    parser.add_argument("-p", action='store_true', help='pprint output')

    args = parser.parse_args(sys.argv[1:])
    if args.u is None:
        url = input("URL:")
    else:
        url = args.u
    if args.t is None:
        token = getpass("token:")
    else:
        token = args.t
    if (token is not None and len(token)) == 0 and (url is not None and len(url)):
        sys.exit(1)
    if args.d is None and args.q is None:
        return url, token
    if args.d is None:
        print('please provide DB name')
        sys.exit(1)
    if args.q is None:
        print('please provide query JSON')
        sys.exit(1)
    return url, token, args.d, args.q, args.p
