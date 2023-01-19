import argparse
import os
import requests
import json


# this will upload the dashboard to grafana
def upload_dashboard(dashboard_path, api_url, api_key, grafana_folder_name):
    # Set headers for API call
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key
    }
    # Make API call to get list of folders
    response = requests.get(f'{api_url}/folders', headers=headers)

    # Parse response as JSON
    folders = json.loads(response.text)
    for folder in folders:
        if folder['title'] == grafana_folder_name:
            folder_uid = folder['uid']
            break

    # Read JSON file containing the dashboard
    with open(dashboard_path, 'r') as file:
        dashboard_json = json.load(file)
        dashboard_json['id'] = None

    response = requests.post(f'{api_url}/dashboards/db', json={
        'dashboard': dashboard_json, 'folderUid': folder_uid, 'overwrite': True}, headers=headers)
    print(response.content)


def main():
    parser = argparse.ArgumentParser(description='Upload Grafana dashboard')
    parser.add_argument('--dashboard_dir', type=str, help='Source directory')
    parser.add_argument('--dashboard_name', type=str, help='Dashboard name')
    parser.add_argument('--grafana_api', type=str, help='URL Api for Grafana')
    parser.add_argument('--grafana_key', type=str, help='Key for Grafana')
    parser.add_argument('--grafana_folder_name', type=str, help='Folder name to upload')

    # Parse the command-line arguments
    args = parser.parse_args()
    dashboard_path = args.dashboard_dir + args.dashboard_name

    api_url = args.grafana_api
    api_key = args.grafana_key
    grafana_folder_name = args.grafana_folder_name

    upload_dashboard(dashboard_path, api_url, api_key, grafana_folder_name)


if __name__ == '__main__':
    main()
