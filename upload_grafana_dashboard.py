import argparse
import os
import requests
import json


# this will upload the dashboard to grafana
def upload_dashboard(dashboard_path, api_url, api_key):
    # Get Grafana API URL and API key from GitLab environment variables

    # Set headers for API call
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key
    }

    # Read JSON file containing the dashboard
    with open(dashboard_path, 'r') as file:
        dashboard_json = json.load(file)
        dashboard_json['id'] = None

    response = requests.post(f'{api_url}/dashboards/db', json={
                             'dashboard': dashboard_json, 'folderId': 0, 'overwrite': True}, headers=headers)
    print(response.content)


def main():
    parser = argparse.ArgumentParser(description='Upload Grafana dashboard')
    parser.add_argument('--dashboard_dir', type=str, help='Source directory')
    parser.add_argument('--dashboard_name', type=str, help='Dashboard name')
    parser.add_argument('--grafana_api', type=str, help='URL Api for Grafana')
    parser.add_argument('--grafana_key', type=str, help='Key for Grafana')

    # Parse the command-line arguments
    args = parser.parse_args()
    dashboard_path = args.dashboard_dir + args.dashboard_name

    api_url = os.environ['GRAFANA_API_URL']
    api_key = os.environ['GRAFANA_API_KEY']

    upload_dashboard(dashboard_path, api_url, api_key)


if __name__ == '__main__':
    main()
