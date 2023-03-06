# CloudBillingTool

Teams can order cloud resources (Azure, Hetzner Cloud/Hetzner Dedicated, AWS, .... ) for environments (e.g. AKS). 
These resources cause costs in the different environments. These costs should be (1) recorded, (2) evaluated and (3) 
transparently identified and presented according to a defined logic of the cost causer.

## Table of Contents

- [Project Description](#project-description)
- [Getting Started](#getting-started)

# Project Description

The CloudBillingTool collects all the different costs from providers and transform those into a unique
"allbilling" format and write this into a sql database using a jdbc driver.  

- Why did we use the Techstack
- Challenges we faced during the development

### Supported Costs Provider

Azure YES

Hetzner YES

AWS Coming SOON


# Getting Started

CloudBillingTool assumes that the billing data is properly formated. The hetzner provided costs files are corrupt and 
should be fixed, following the script 'hetzner_fix_data.py'. 

## Requirements

- Billing Data from Providers
- Python3
- SQL Server
- pySpark for processing the data
- Grafana

## How to Install and Run the Project

The CloudBillingTool downloads the costs files from the different locations and processes the data and write the output
(allbilling) into the target SQL Server Table which is visualized from Grafana.

### Infrastructure

- SQL Server
- Grafana

#### Docker Compose

```
cd docker/
docker compose up
```

#### #Cloud

Please make sure an SQL Server is setup and running. Grafana is setup and running. Network Connection exists.

## Run CloudBillingTool 

### Run CloudBillingTool via standalone (locally)
```
usage: cloudbillingtool-run.py [-h] 

python cloudbillingtool-run.py \
    --output_path /tmp/cloudbilling/output/  \
    --jdbc_url "jdbc:sqlserver://cloudbillingtool.database.windows.net:1433;databaseName=cloudbillingtooldb;user=admin;password=pw123;trustServerCertificate=true;encrypt=false;"  \
    --azure_sa_name "seneccloudbillingtool"   \
    --azure_sa_key "xxyy \
    --download

```
### Run CloudBillingTool via docker
The following code will build a docker container ( as a standalone mode). 

Run local test data
```
# build image
docker build -t cloudbillingtool ./

# run the container
bash docker-run.sh
#or
docker run --name cloudbillingtool \
    -v ${PWD}/tests/data/:/data/ \
    -v ${PWD}/tests/metadata/:/metadata/ \
    -v /tmp/output/:/output/ cloudbillingtool

# cleanup
docker stop cloudbillingtool; docker rm cloudbillingtool;  
```

Run with data from Azure storage Account
```
docker build -t cloudbillingtool ./

docker run --name cloudbillingtool
    -v ${PWD}/tests/metadata/:/metadata/ \
    -v /tmp/output/:/output/ cloudbillingtool

python cloudbillingtool-run.py \
    --output_path /tmp/cloudbilling/output/  \
    --jdbc_url "jdbc:sqlserver://cloudbillingtool.database.windows.net:1433;databaseName=cloudbillingtooldb;user=admin;password=pw123;trustServerCertificate=true;encrypt=false;"  \
    --azure_sa_name "seneccloudbillingtool"  \
    --azure_sa_key "xxyy \
    --download
```

### Run CloudBillingTool via submitting to a SparkCluster

Todo:

### How to Add a new Costs Data Source

This will describe how you can add more data sources to the costs description.

## Setup CloudBillingTool with K8s and SQL Server

Todo: Architecture Diagram

``
cd docker/
docker-compose up
``

### create data structures in sqlserver
``
./sqldata/sql_create_tables.sh
``

### Generate Data into sqlserver
```
python cloudbillingtool-run.py --hetzner_data "/home/senec/seneccloudbillingtool/hetznerbilling/*.csv"     --metadata "tests/metadata"     --jdbc_url "jdbc:sqlserver:// cloudbillingtool.database.windows.net:1433;databaseName=cloudbillingtool;user=cloudbillingtool_admin;password=WooQuuWaer7o;trustServerCertificate=true;encrypt=false;"     --jdbc_table "allbilling"   --azure_sa_name "seneccloudbillingtool"   --azure_sa_key "5Gm67oAb2JcvdtMKn4KRBCZQhmmrZnrRgs8W3pCM+/SJNQ8TFci0b9I7+7PWkO1tGLNhK7wDmbxf+AStFWm2RA=="


python cloudbillingtool-run.py --hetzner_data "tests/data/hetzner/*.csv" \
    --azure_data "tests/data/azure/*.csv" \
    --metadata "tests/metadata" \
    --output_path "/tmp/cloudbillingtool/" \
    --jdbc_url "jdbc:sqlserver://localhost:1433;databaseName=cloudbillingtool;user=SA;password=chiiKu4x*1;trustServerCertificate=true;encrypt=false;" \
    --jdbc_table "allbilling"
```

### Query data from sqlserver
``
./sqldata/sql_query.sh
``

### Grafana Data Source

Create a new sqlserver data source using username: SA with password "chiiKu4x*1" sql1:1433 on database "cloudbillingtool"

### Grafana Dashboard with Grafana API Key
Access Grafana via localhost:3000 with admin/password and generate an GRAFANA_API_KEY=abc
Create Grafana dashboard using the API KEY
```
GRAFANA_API_KEY=abc
GRAFANA_API=http://localhost:3000/api
python upload_grafana_dashboard.py --dashboard_dir grafana/ --dashboard_name CloudBillingDashboard.json --grafana_api $GRAFANA_API --grafana_key $GRAFANA_API_KEY
```


# Developmen./sqldata/sql_create_tables.sh

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

 