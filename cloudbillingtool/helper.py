import re
import os
from azure.storage.blob import BlobServiceClient


def tags_from_json_string(str):
    tags = []
    if str and len(str)>0:
        import json
        kv = json.loads(str)
        for k,v in kv.items():
            tags.append(k+"="+v)
    return tags


def flatten(l):
    return [item for sublist in l for item in sublist]


def extract_costresourceid(desc):
    if desc and len(desc) > 0:
        return re.search(r'#[0-9]+', desc).group() if re.search(r'#[0-9]+', desc) else ""
    else:
        return "NoResourceId"


def fix_date_format_for_hetzner(billing_date_hetzner):
    if not billing_date_hetzner:
        return ""
    year, day, month = billing_date_hetzner.split('-')
    return f"{month}-{day}-{year}"


def download_blobs_from_azure(account_name, account_key, container_name, target_dir):
    blob_service_client = BlobServiceClient.from_connection_string(
        f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
    )
    container_client = blob_service_client.get_container_client(container_name)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for blob in container_client.list_blobs():
        blob_client = blob_service_client.get_blob_client(container_name, blob.name)
        target_path = os.path.join(target_dir, blob.name)

        if blob.size > 0:
            if not os.path.exists(os.path.dirname(target_path)):
                os.makedirs(os.path.dirname(target_path))
            print("Download: " + blob.name)
            print("Local: " + target_path)

            with open(target_path, "wb") as f:
                data = blob_client.download_blob().readall()
                f.write(data)