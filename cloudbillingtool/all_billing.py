from pyspark import rdd
from pyspark.pandas import DataFrame
from pyspark.sql.types import StructType, StringType, DateType, ArrayType, DecimalType

all_bills_schema = StructType() \
  .add("Provider",StringType(), True) \
  .add("ProductName",StringType(), True) \
  .add("Date",DateType(), True) \
  .add("Costs",DecimalType(), True) \
  .add("UnitPrice",DecimalType(), True) \
  .add("Quantity", DecimalType(), True) \
  .add("CostResourceId",StringType(), True) \
  .add("CostResourceTag", ArrayType(StringType()), True)