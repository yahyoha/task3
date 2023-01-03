import re
from pyspark import rdd
from pyspark.pandas import DataFrame
from pyspark.sql.functions import col, lit, array, split, array_join, array_union, concat, to_date, explode
from pyspark.sql.types import StructType, StringType, ArrayType, DecimalType, BooleanType
import pandas as pd

#azure_schema = StructType() \
#  .add("effectivePrice", DecimalType(12,2), True) \
#  .add("quantity",DecimalType(12,2), True) \
#  .add("costInBillingCurrency", DecimalType(12,2), True )\
#  .add("costInPricingCurrency", DecimalType(12,2), True)\
#  .add("costInUsd", DecimalType(12,2), True)\
#  .add("paygCostInBillingCurrency", DecimalType(12,2), True)\
#  .add("paygCostInUsd", DecimalType(12,2), True)  \
#  .add("exchangeRatePricingToBilling", DecimalType(12,2), True)\
#  .add("isAzureCreditEligible", BooleanType(), True)\
#  .add("PayGPrice", DecimalType(12,2), True)\
#  .add("unitPrice", DecimalType(12,2), True)


def load_files(spark, azure_data, work_folder ) -> rdd :
    #resource_mapping_df = pd.read_csv(work_folder+"/resource_mapping.csv", sep='\t')
    #type_mapping_df = pd.read_csv(work_folder+"/type_mapping.csv", sep='\t')

    return\
        spark.read\
        .options(format='csv', escape="\"", header=True)\
        .csv(azure_data)\
        .withColumn("effectivePrice",col("effectivePrice").cast("double")) \
        .withColumn("quantity", col("quantity").cast("double"))\
        .withColumn("costInBillingCurrency", col("costInBillingCurrency").cast("double"))\
        .withColumn("costInPricingCurrency", col("costInPricingCurrency").cast("double"))\
        .withColumn("costInUsd", col("costInUsd").cast("double")) \
        .withColumn("paygCostInBillingCurrency", col("paygCostInBillingCurrency").cast("double")) \
        .withColumn("paygCostInUsd",  col("paygCostInUsd").cast("double")) \
        .withColumn("exchangeRatePricingToBilling", col("exchangeRatePricingToBilling").cast("double")) \
        .withColumn("isAzureCreditEligible", col("isAzureCreditEligible").cast("boolean")) \
        .withColumn("PayGPrice", col("PayGPrice").cast("double")) \
        .withColumn("unitPrice", col("unitPrice").cast("double")) \
        .rdd \
        .map(lambda row: {
            "Provider": "azure",
            "Type": row.ProductName,
            "Price": row.unitPrice,
            "ProductName": "",
            "Date": row.date,
            "CostResourceID": row.ResourceId,
            "CostResourceTag": row.tags
      })

    # Todo: key=value