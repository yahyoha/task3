from pyspark import rdd
from pyspark.sql.types import StructType, StringType, DateType, ArrayType, DecimalType

from . import azure_billing
from . import hetzner_billing

all_bills_schema = StructType() \
  .add("Provider",StringType(), True) \
  .add("ProductName",StringType(), True) \
  .add("Date",DateType(), True) \
  .add("Costs",DecimalType(), True) \
  .add("UnitPrice",DecimalType(), True) \
  .add("Quantity", DecimalType(), True) \
  .add("CostResourceId",StringType(), True) \
  .add("CostResourceTag", ArrayType(StringType()), True)


def generate_uniform_data_from(spark, azure_data, hetzner_data, aws_data, metadata_path) -> rdd:

    azure_billing_with_tags = azure_billing.load_files_with_mapping(spark, azure_data, metadata_path)

    hetzner_billing_with_tags = hetzner_billing.load_files_with_mapping(spark, hetzner_data, metadata_path)

    # Todo: aws is missing

    # combine azure with hetzner billing
    return azure_billing_with_tags.rdd.union(hetzner_billing_with_tags.rdd)