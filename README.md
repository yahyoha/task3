# CloudBillingTool

```
git clone .
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

## Install

### Infrastructure
```
clone terraform-repo
terraform init
terraform plan
terraform validate
terraform apply
```


### CloudBillingTool App
```
python setup.py bdist_wheel
```

### Setup Grafana

Tbd


## Run tests
```
python3 -m unittest
```


## Run PySpark cli

You can run the cloudbillingtool locally and produce output
````
python3 cloudbillingtool.py 
    data/hetzner/*.csv
    data/azure_bills/*.csv
    mapping-tables/
    /tmp/cloudbillingtool_output/
````


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


##  Build the python module
```
python setup.py bdist_wheel
```