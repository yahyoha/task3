#!python

import argparse
import os
import boto3
import google.cloud.storage
from azure.storage.blob import BlobServiceClient


def fix_file(fin, fout):
    lc = 0
    for line in fin:
        lc += line.count(',')
        if lc < 8:
            fout.write(line[:-1])
        else:
            fout.write(line)
            lc = 0


def handle_local_storage(source_dir, target_dir, file):
    with open(source_dir + '/' + file) as fin, open(target_dir + '/fixed_' + file, 'w') as fout:
        fix_file(fin,fout)
    print("Fixed "+file+"")


def handle_s3_storage(source_dir, target_dir, file):
    s3 = boto3.client('s3')
    s3.download_file(source_dir, file, '/tmp/' + file)
    with open('/tmp/' + file) as fin, open(target_dir + '/fixed_' + file, 'w') as fout:
        fix_file(fin,fout)
    s3.upload_file(target_dir + '/fixed_' + file, target_dir, 'fixed_' + file)
    print("Fixed "+file+"")


def handle_gcp_storage(source_dir, target_dir, file):
    client = google.cloud.storage.Client()
    bucket = client.get_bucket(source_dir)
    blob = bucket.blob(file)
    blob.download_to_filename('/tmp/' + file)
    with open('/tmp/' + file) as fin, open(target_dir + '/fixed_' + file, 'w') as fout:
        fix_file(fin,fout)
    blob = bucket.blob('fixed_' + file)
    blob.upload_from_filename(target_dir + '/fixed_' + file)
    print("Fixed "+file+"")


def handle_azure_storage(source_dir, target_dir, file,storage_account,storage_key):
    # Create a blob service client
    blob_service_client = BlobServiceClient(account_url=f"https://{storage_account}.blob.core.windows.net", credential=storage_key)
    container_name, blob_name = source_dir.split("/")
    # Download the blob to a local file
    with open('/tmp/' + file, "wb") as my_blob:
        blob_service_client.get_blob_to_stream(container_name=container_name, blob_name=blob_name, stream=my_blob)
    with open('/tmp/' + file) as fin, open(target_dir + '/fixed_' + file, 'w') as fout:
        fix_file(fin,fout)
    # Upload the fixed file
    with open(target_dir + '/fixed_' + file, "rb") as data:
        blob_service_client.upload_blob(container_name=container_name, blob_name='fixed_' + blob_name, data=data)
    print("Fixed " + file + "")


def main():
    parser = argparse.ArgumentParser(description='Fix broken lines in files')
    parser.add_argument('--source_dir', type=str, help='Source directory')
    parser.add_argument('--target_dir', type=str, help='Target directory')
    parser.add_argument('--source_type', type=str, choices=['local','s3','gcp','azure'], help='Type of storage')
    parser.add_argument('--storage_account', type=str, help='storage account name for azure')
    parser.add_argument('--storage_key', type=str, help='storage key for azure')

    args = parser.parse_args()

    for file in os.listdir(args.source_dir):
        if args.source_type == 'local':
            handle_local_storage(args.source_dir, args.target_dir, file)
        elif args.source_type == 's3':
            handle_s3_storage(args.source_dir, args.target_dir, file)
        elif args.source_type == 'gcp':
            handle_gcp_storage(args.source_dir, args.target_dir, file)
        elif args.source_type == 'azure':
            handle_azure_storage(args.source_dir, args.target_dir, file, args.storage_account, args.storage_key)
        else:
            print("Invalid source type. Must be 'local', 's3', 'gcp' or 'azure'.")


if __name__ == '__main__':
    main()