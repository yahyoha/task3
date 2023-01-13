<!-- PROJECT LOGO -->
<br />
<div align="center">
  <img src="multi-cloud-billing.jpg" alt="Logo" width="60" height="60">
  <h2 align="center" style="text-align: center;">Cloud Billing Tool</h2>
  <p align="center">
   Unify Your Cloud Costs, Simplify Your Bill Management with our Cloud Billing Tool
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#architecture">Architecture</a></li>
    <li><a href="#Overview-of-the-Key-Components">Overview of the Key Components</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>


## Architecture
<div align="center">
<img src="CloudBillingToolArchitecture.png" alt="Architecture" width="500" height="350">
</div>


## Overview of the Key Components

**Azure Synapse Analytics** is a fully managed, cloud-based analytics platform that allows users to ingest, prepare, manage, and serve data for immediate business intelligence and machine learning needs. It provides a unified experience for data integration and analytics by allowing us to query data using familiar T-SQL and also leveraging built-in connectors and integration with other Azure services. It also provides both serverless and provisioned options, which allows users to scale their usage and costs based on their specific needs.

**Azure Synapse Studio Notebooks** is a feature of Azure Synapse Analytics that allows us to create, edit, and run Jupyter notebooks within the Azure Synapse Studio environment. The Azure Synapse Studio Notebooks environment provides a web-based interface for creating and running Jupyter notebooks, and it also integrates with other Azure services such as Azure Data Factory, Azure Databricks, and Azure Machine Learning. It also allows us to connect to various data sources, including Synapse SQL, Synapse Analytics (formerly SQL DW), Azure Data Lake Storage, Azure Cosmos DB, and more. With the integration of Synapse Studio notebooks, you can execute the notebooks in parallel with Azure Synapse Spark or SQL and make use of the Spark or SQL pool for processing.

**In Azure Synapse, pipelines** are a fundamental building block for creating and organizing data integration and data flow workflows. They allow us to group activities together to create a cohesive and repeatable data processing job. Pipelines in Azure Synapse are based on the pipeline concept in Azure Data Factory, which has been integrated into the Azure Synapse Studio environment to provide a more streamlined and unified experience for working with data integration and data flow tasks. The low-code approach of pipelines in Azure Synapse makes it easy for developers and data engineers to quickly create and manage data integration and data flow workflows without needing to write a lot of complex code.

**Triggers** in Synapse pipelines determine when a particular pipeline(s) should be run. In an Azure Synapse environment, pipeline runs are typically instantiated by passing arguments to parameters that we define in the pipeline. We can execute a pipeline either manually or by using a trigger in a JSON definition.

**Azure Data Explorer** is a fully managed, high-performance, big data analytics platform that makes it easy to analyze high volumes of data in near real time. The Azure Data Explorer toolbox gives you an end-to-end solution for data ingestion, query, visualization, and management.

**Kusto Query Language (KQL)** is the query language used by Azure Data Explorer(ADX) to retrieve and analyze data stored in the service. Kusto is a distributed, column-store database designed for high-performance querying and processing of telemetry data. Kusto supports advanced data exploration and discovery scenarios, as well as real-time data processing and analytics scenarios. Azure Data Explorer (ADX) provides an interactive query experience for working with large datasets, and allows us to perform complex queries and aggregations on out data quickly and easily. ADX is built on top of Kusto and provides a user-friendly interface, APIs, libraries and SDK for running analytics on data stored on Kusto cluster. In short, Azure Data Explorer is the service, Kusto is the technology behind it, and KQL is the query language that we use to query data in ADX.


**Grafana** is an open-source platform for data visualization and monitoring. It provides a powerful and flexible way to create, explore, and share dashboards and metrics with a wide range of data sources. It allows users to create and publish dashboards that can be easily shared and embedded in other web pages, and it offers a wide range of visualization options such as bar graphs, line graphs, heat maps, and pie charts to help you display your data in the most meaningful and useful way possible. Grafana also provide alerting feature, which is useful for monitoring critical systems and services and alerting team members when certain conditions are met or when certain thresholds are exceeded, which allowing proactive intervention to help avoid issues and minimize downtime.


## Installation

Please clone the repo of CloudBilling Tool.

```
git clone https://gitlab.com/rocket9-code/customers/senec/cloudbillingtool-app.git
```
## Run CloudBillingTool as cli
```
usage: cloudbillingtool-run.py [-h] [--hetzner_data HETZNER_DATA] [--azure_data AZURE_DATA] [--aws_data AWS_DATA] [--metadata METADATA] [--output_path OUTPUT_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --hetzner_data HETZNER_DATA
                        Path to Hetzner data files
  --azure_data AZURE_DATA
                        Path to Azure data files
  --aws_data AWS_DATA   Path to AWS data files
  --metadata METADATA   Path to metadata (mapping files) directory
  --output_path OUTPUT_PATH
                        Path to output directory

```
## Run CloudBillingTool via docker

The following code will build a docker container (standalone). It needs the data mounted (eg. azure  blob storage or locally) and also the output folder
```
# build image
docker build -t cloudbillingtool ./

# run the container
bash docker-run.sh
#or
docker run --name cloudbillingtool -v ${PWD}/tests/data/:/data/ -v ${PWD}/tests/metadata/:/metadata/ -v /tmp/output/:/output/ cloudbillingtool

# cleanup
dockdocker stop cloudbillingtool; docker rm cloudbillingtool;  
```

## Setup CloudBillingTool with Synapse


### Deploy Infrastructure to Azure
```
git clone terraform-repo
terraform init
terraform plan
terraform validate
terraform apply
```

### Setup Grafana with Kusto Connection
1. Select 'App Registrations' service from your Azure Portal.
2. Select '+New Registration'  and Give the name of your application e.g. 'SenecBillingAppV2' and click the button 'Registration.
3. Please note the following values,APPLICATION(Client)ID and DIRECTORY(Tenant) ID from the 'App Registrations' page.
4. Navigate to 'Certificates&Secrets' which is on the left side of the page 'SenecBillingAppV2'.
5. Click '+ New Client Secret' and this will open a window. Fill up the form according to your custom name and click the button 'Add'. This will create a Secret Key and Value.Save the 'Secret value'.
6. Navigate to the Azure Cluster created by Terraform.
7. Select the database and navigate to the 'Permission' and give viewer permission to your application created in step 2.
8. Go to your 'Grafana Account' and then select 'Configuration'.
9. Select 'Plugins' Tab and Search for the plugin 'Azure Data Explorer Data Source'.Install it.
10. Now select 'Data Sources' Tab and write 'Azure Data Explorer Data Source' in the search bar.Press 'Add Data Source' button.This will open 'Data Sources / Azure Data Explorer Datasource' page.
11. Set the name 'cloudbillingsenecGrafanaV1' because dashboard will be using this same name.If you use our own custom name,you have to  update the dashboard's datasource and point it to your own 'Data Source Name.
12. Navigate to the Azure Data Explorer Web UI via the Azure Portal. The AAD application that you created in step 2 needs to be given viewer access to your Azure Data Explorer database. This is done using the dot command.
```
.add database [our_db_name] viewers (‘aadapp=[our_client_id(values from step 3);our_tenant_id(values from step 3)’)
```
13. Navigate back to your Grafana's page 'Data Sources / Azure Data Explorer Datasource' and scroll down.Stop at the section 'Connection Details'.

14. Fill up the forms as below : 
    1. Azure Cloud : Azure
    2. Cluster URL : (CLUSTER_URL_OF_OUR_YOUR_CLUSTER)
    3. Tenant ID : (TENANT_ID/DIRECTORY_ID-values from step 3)
    4. Client ID:  (APPLICATION_ID/SERVICE_PRINCIPLE_ID - values from step 3)
    5. Client Secret : (PASSWORD_CREATED_IN_STEP-This is the 'Secret Value' from the step 5)

15. Scroll down and stop at the section 'Default Schema Settings'.Select 'Default Database' dropdown and if the step 14 is successful you will see the name of the database from your 'Azure Data Explorer Cluster'.

16. Select the database and press 'Save&Test' Button.

17. Navigate Back to the 'Billing Dashboard' and you will see our visualization.
  

## Setup CloudBillingTool with K8s


# Development 
## Build
```
python setup.py bdist_wheel
```

## Run tests
```
python3 -m unittest
```

## Load the unified Schema via pySpark into your code

You can use the following python code to process the data in a separate pyspark app
```
all_bills_schema = StructType() \
    .add("Provider",StringType(), True) \
    .add("ProductName",StringType(), True) \
    .add("Date",DateType(), True) \
    .add("Costs",DecimalType(), True) \
    .add("UnitPrice",DecimalType(), True) \
    .add("Quantity", DecimalType(), True) \
    .add("CostResourceId",StringType(), True) \
    .add("CostResourceTag", ArrayType(StringType()), True)
  
    spark.read\
    .options(format='csv', escape="\"", header=False)\
    .schema(all_bills_schema)\
    .csv("path/to/data")
  ```