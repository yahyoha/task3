# set default resource groups
#az configure --defaults group=CloudBillingTool
#az account set --subscription baa0f8da-8f65-4791-83df-8b035d51a3b4

# upload python runner
az storage blob upload --account-name senecstorage --container-name cloudbillingtool --file spark-run-cloudbillingtool.py --name  spark-run-cloudbillingtool.py --auth-mode login --overwrite

# upload package to azure cloud
az synapse workspace-package upload --workspace-name $SYNAPSE_WORKSPACE_NAME --package $PACKAGE

az synapse spark pool create --name $SPARK_POOL --workspace-name $SYNAPSE_WORKSPACE_NAME --spark-version 3.2 --node-count 3 --node-size small

az synapse spark pool update --name $SPARK_POOL --workspace-name $SYNAPSE_WORKSPACE_NAME --package-action ADD --package $PACKAGE

#--library-requirements