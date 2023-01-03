from pyspark import rdd
from pyspark.pandas import DataFrame
from pyspark.sql.functions import col, lit, array, split, array_join, array_union, concat, to_date, explode
from pyspark.sql.types import StructType, StringType, ArrayType, DecimalType, BooleanType
import cloudbillingtool.helper as helper
import pandas as pd


def load_files(spark, azure_data, work_folder ) -> rdd :
    resource_mapping_df = pd.read_csv(work_folder+"/resource_mapping.csv", sep='\t')
    type_mapping_df = pd.read_csv(work_folder+"/type_mapping.csv", sep='\t')

    return\
        spark.read\
        .options(format='csv', escape="\"", header=True)\
        .csv(azure_data)\
        .withColumn("effectivePrice",col("effectivePrice").cast("decimal(12,8)")) \
        .withColumn("quantity", col("quantity").cast("decimal(12,8)"))\
        .withColumn("costInBillingCurrency", col("costInBillingCurrency").cast("decimal(12,8)"))\
        .withColumn("costInPricingCurrency", col("costInPricingCurrency").cast("decimal(12,8)"))\
        .withColumn("costInUsd", col("costInUsd").cast("decimal(12,8)")) \
        .withColumn("paygCostInBillingCurrency", col("paygCostInBillingCurrency").cast("decimal(12,8)")) \
        .withColumn("paygCostInUsd",  col("paygCostInUsd").cast("double")) \
        .withColumn("exchangeRatePricingToBilling", col("exchangeRatePricingToBilling").cast("double")) \
        .withColumn("isAzureCreditEligible", col("isAzureCreditEligible").cast("boolean")) \
        .withColumn("PayGPrice", col("PayGPrice").cast("decimal(12,8)")) \
        .withColumn("unitPrice", col("unitPrice").cast("decimal(12,8)")) \
        .rdd \
        .map(lambda row: {
            "Provider": "azure",
            "Type":  "",    # Missing in Azure
            "Costs": row.costInBillingCurrency,
            "UnitPrice": row.unitPrice,
            "Quantity": row.quantity,
            "Product": row.ProductName,
            "Date": row.date,
            "CostResourceID": row.ResourceId,
            "CostResourceTag": helper.tags_from_json_string(row.tags) +
                                helper.merge_tags_from_dt(
                                    resource_mapping_df,
                                    type_mapping_df,
                                    row.ResourceId,
                                    row.ProductName
                                )
      })


def load_files_with_mapping(spark, azure_data, work_folder):
    hetzner_df: DataFrame = \
        load_files(spark, azure_data, work_folder)\
        .toDF()\
        .alias("azure_df") \

    joined_with_tags = hetzner_df \
        .select(lit("azure").alias("provider"),
            col("azure_df.Type"),
            col("azure_df.Product").alias("ProductName"),
            col("azure_df.Costs").cast("float").alias("Costs"),
            col("azure_df.UnitPrice").cast("float").alias("UnitPrice"),
            col("azure_df.Quantity").cast("float").alias("Quantity"),
            to_date(col("azure_df.Date"), "MM/dd/yyyy").alias("Date"),
            col("azure_df.CostResourceID").alias("CostResourceID"),
            explode("azure_df.CostResourceTag").alias("CostResourceTag"))

    return joined_with_tags
