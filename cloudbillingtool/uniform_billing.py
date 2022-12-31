from pyspark import rdd
from pyspark.pandas import DataFrame
from pyspark.sql.types import StructType, StringType, DateType, ArrayType

uniform_schema = StructType() \
  .add("Provider",StringType(), True) \
  .add("ProductName",StringType(), True) \
  .add("Date",DateType(), True) \
  .add("Price",StringType(), True) \
  .add("CostResourceTage",StringType(), True) \
  .add("CostResourceId",StringType(), True) \
  .add("Tags",ArrayType(StringType()), True )