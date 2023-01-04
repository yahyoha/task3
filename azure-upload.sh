# upload python runner
az storage blob upload --account-name senecstorage --container-name cloudbillingtool --file spark-run-cloudbillingtool.py --name  spark-run-cloudbillingtool.py --auth-mode login --overwrite

# upload package to azure cloud
az synapse workspace-package upload --workspace-name $SYNAPSE_WORKSPACE_NAME --package