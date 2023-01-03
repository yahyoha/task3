# Install
```
pip install -r requirements
```

# Run tests
```
python3 -m unittest
```


# Run PySpark

Example
````
python3 cloudbillingtool.py tests/data/hetzner/*.csv * tests/data /tmp/cloudbillingtool_output/
````


# Load the unified Schema via pySpark
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