from pyspark import rdd
from pyspark.pandas import DataFrame
from pyspark.sql.types import StructType, StringType, DateType, ArrayType, DecimalType

import hetzner_billing

uniform_schema = StructType() \
  .add("Provider",StringType(), True) \
  .add("ProductName",StringType(), True) \
  .add("Date",DateType(), True) \
  .add("Price",DecimalType(), True) \
  .add("CostResourceTag",StringType(), True) \
  .add("CostResourceId",StringType(), True) \
  .add("Tags",ArrayType(StringType()), True )


def load_all_with_tags(spark, hetzner_data, azure_data, work_folder):
  hetzner_billing_with_tags = hetzner_billing.load_with_mapping(spark, hetzner_data, work_folder)

  # Todo: implement azure
  #azure_billing_with_tags = azure_billing.load_with_mapping(spark, hetzner_data, work_folder).rdd.collect()


  return hetzner_billing_with_tags