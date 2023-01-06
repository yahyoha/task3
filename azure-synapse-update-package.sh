# set default resource groups
az configure --defaults group=CloudBillingTool
az account set --subscription baa0f8da-8f65-4791-83df-8b035d51a3b4

# upload package to azure cloud
az synapse workspace-package upload --workspace-name $SYNAPSE_WORKSPACE_NAME --package $PACKAGE

az synapse spark pool update --name $SPARK_POOL --workspace-name $SYNAPSE_WORKSPACE_NAME --package-action REMOVE --package $OLD_PACKAGE

az synapse spark pool update --name $SPARK_POOL --workspace-name $SYNAPSE_WORKSPACE_NAME --package-action ADD --package $NEW_PACKAGE