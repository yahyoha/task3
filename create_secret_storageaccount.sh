#!/bin/bash
# Usage: ./create_secret_storageaccount.sh REGISTRY USER TOKEN NAMESPACE

STORAGEACCOUNT_NAME="$1"
STORAGEACCOUNT_KEY="$2"
NAMESPACE="$3"

echo $STORAGEACCOUNT_NAME
echo $STORAGEACCOUNT_KEY

kubectl create secret generic azure-storage-secret --namespace $NAMESPACE \
 --from-literal=azurestorageaccountname="$STORAGEACCOUNT_NAME" \
 --from-literal=azurestorageaccountkey="$STORAGEACCOUNT_KEY"