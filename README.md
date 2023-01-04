# CloudBillingTool
## Install
```
pip install -r requirements
```

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


## Use in the Code Load the unified Schema via pySpark

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

It will generate a 
