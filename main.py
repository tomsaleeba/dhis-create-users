import csv
import sys
import json
import argparse
import requests
from requests.auth import HTTPBasicAuth


def cmdline_args():
    p = argparse.ArgumentParser(description='DHIS user creator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("-i", "--ignore-header", action="store_true",
           help="ignore the first line")
    p.add_argument("-s", "--server", type=str, default='http://localhost:8080',
           help="DHIS (scheme and) host, e.g. https://some.server")
    p.add_argument("-u", "--admin-user", type=str, default='admin',
           help="DHIS admin username")
    p.add_argument("-p", "--admin-pass", type=str, default='district',
           help="DHIS admin password")
    p.add_argument("-g", "--user-group", type=str, required=True,
           help="DHIS user group to apply")
    p.add_argument("-r", "--user-role", type=str, required=True,
           help="DHIS user role to apply")
    return(p.parse_args())


def do_it(args):
    row_reader = csv.reader(sys.stdin, delimiter=',', quotechar='"')
    admin_user = args.admin_user
    admin_pass = args.admin_pass
    api_base_url = '%s/api/29' % args.server
    auth = HTTPBasicAuth(admin_user, admin_pass)
    first = True
    for row in row_reader:
        if first and args.ignore_header:
            first = False
            continue
        ( first_name, org_unit, username, password ) = row
        print('[INFO] creating user=%s' % username)
        try:
            id_resp = requests.get('%s/system/id' % api_base_url, auth=auth)
            if not id_resp.status_code == 200:
                print('[ERROR] failed to generate a user ID, cannot continue. Resp=' + str(json.dumps(id_resp.json(),
                    indent=2)))
                continue
            new_user_id = id_resp.json()['codes'][0]
            create_data ={
                'id': new_user_id,
                'firstName': first_name,
                'surname': 'user',
                'userCredentials': {
                    'userInfo': { 'id': new_user_id },
                    'username': username,
                    'password': password,
                    'userRoles': [{
                        'id': args.user_role,
                    }],
                },
                'organisationUnits': [{
                    'id': org_unit,
                }],
                'userGroups': [{
                    'id': args.user_group,
                }],
            }
            create_resp = requests.post('%s/users' % api_base_url, json=create_data, auth=auth)
            fragment ='[ERROR] failed to create user="%s"' % username
            if create_resp.status_code is 200:
                if create_resp.json()['status'] == 'ERROR':
                    pretty_json = json.dumps(create_resp.json()['typeReports'], indent=2)
                    print('%s, HTTP response dump=%s' % (fragment, pretty_json))
                else:
                    print('[INFO] success creating user="%s"' % username)
            else:
                print('%s, resp=%s' % (fragment, create_resp.text))
        except Exception as e:
            raise e


if __name__ == '__main__':

    if sys.version_info<(3,0,0):
        sys.stderr.write("You need python 3.0 or later to run this script\n")
        sys.exit(1)

    if sys.stdin.isatty():
        print('[ERROR] No data supplied, you must pipe a CSV file into stdin')
        sys.exit(1)
    try:
        args = cmdline_args()
    except argparse.ArgumentError as e:
        print('[ERROR] failed to parse args: ' + str(e))
        sys.exit(1)

    do_it(args)
