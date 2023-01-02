from pyspark import rdd
from pyspark.pandas import DataFrame
from pyspark.sql.types import StructType, StringType, DateType, ArrayType, DecimalType

uniform_schema = StructType() \
  .add("Provider",StringType(), True) \
  .add("ProductName",StringType(), True) \
  .add("Date",DateType(), True) \
  .add("Price",DecimalType(), True) \
  .add("CostResourceTag",StringType(), True) \
  .add("CostResourceId",StringType(), True) \
  .add("Tags",ArrayType(StringType()), True )