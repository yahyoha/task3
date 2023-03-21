from pyspark import rdd
from pyspark.sql.types import StructType, StringType, DateType, ArrayType, DecimalType

from . import azure_billing
from . import hetzner_billing
#from . import aws_billing
from . import aws_summary_billing

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

    allbilling_df = spark.createDataFrame(spark.sparkContext.emptyRDD(), schema=all_bills_schema)

    azure_billing_with_tags = azure_billing.load_files_with_mapping(spark, azure_data, metadata_path)

    hetzner_billing_with_tags = hetzner_billing.load_files_with_mapping(spark, hetzner_data, metadata_path)

    aws_billing_without_tags = aws_summary_billing.load_files_with_mapping(spark, aws_data, metadata_path)

    # add new data sources here
    # you can add any costs data source which follow the "all billing schema"

    # add hetzner and aws to azure 
    return allbilling_df.rdd \
                .union(azure_billing_with_tags.rdd)\
                .union(hetzner_billing_with_tags.rdd)\
                .union(aws_billing_without_tags.rdd)
                # add new data source here
