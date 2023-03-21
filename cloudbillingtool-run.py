#!python
# Example ./cloudbillingtool-run.py --hetzner_data "tests/data/hetzner/*.csv" --azure_data "tests/data/azure/*.csv" --metadata "tests/metadata" --output_path "/tmp/output2"

import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws, explode, size
from cloudbillingtool import all_billing

from pyspark.sql.functions import udf, col
from pyspark.sql.types import ArrayType, StringType

from cloudbillingtool.helper import download_blobs_from_azure


def non_empty_filter(col):
    return [x for x in col if x]


non_empty_filter_udf = udf(non_empty_filter, ArrayType(StringType()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--temp_path', help='Path for storing temporal filed', default='/tmp/cloudbilling/' )
    parser.add_argument('--output_path', help='Path to output directory')
    parser.add_argument('--jdbc_url', help='JDBC Connection String')
    parser.add_argument('--jdbc_table', help='JDBC Target Table', default='allbilling' )

    parser.add_argument('--azure_sa_name', help='Azure Storage Account Name' )
    parser.add_argument('--azure_sa_key', help='Azure Storage Account Key')
    parser.add_argument('--azurebilling_container', help='Azure Storage Account Container', default='azurebilling')
    parser.add_argument('--metadata_container', help='Metdata Account Container', default='metadata')
    parser.add_argument('--awsbilling_container', help='Aws Billing Account Container', default='awsbilling')
    parser.add_argument('--hetznerbilling_container', help='Hetzner Account Container', default='hetznerbilling')

    parser.add_argument('--download', help='enable/disable download',  action='store_true')

    args = parser.parse_args()

    hetzner_data = args.temp_path + args.hetznerbilling_container
    azure_data = args.temp_path + args.azurebilling_container
    aws_data = args.temp_path + args.awsbilling_container
    metadata_dir = args.temp_path + args.metadata_container
    output_path = args.output_path

    if args.download:

        # Download azure billing data
        download_blobs_from_azure(args.azure_sa_name, args.azure_sa_key, args.azurebilling_container, azure_data)

        # Download hetznerdata
        download_blobs_from_azure(args.azure_sa_name, args.azure_sa_key, args.hetznerbilling_container, hetzner_data)

        # Download awsdata
        download_blobs_from_azure(args.azure_sa_name, args.azure_sa_key, args.awsbilling_container, aws_data)

        # Download awsdata
        download_blobs_from_azure(args.azure_sa_name, args.azure_sa_key, args.metadata_container, metadata_dir)


    azure_select_files = azure_data + "/subscriptions/*/*/*/*.csv"

    hetzner_select_files = hetzner_data + "/*.csv"

    # Initialize the spark context.
    spark = SparkSession\
        .builder\
        .appName("CloudBillingTool")\
        .config("spark.driver.extraClassPath", "jdbc/mssql-jdbc.jar")\
        .getOrCreate()

    print("Spark Version #"+spark.version) # spark 3.3.1

    # combine azure with hetzner billing
    all_billing_data = all_billing.generate_uniform_data_from(spark, azure_select_files
                                                              , hetzner_data, aws_data, metadata_dir)


    # Map the CostResourceTag to a joined Tag list as a string
    # write to file| summarize sum(Costs)
    if args.jdbc_url:
        all_billing_data.toDF() \
            .withColumn("CostResourceTag", non_empty_filter_udf(col("CostResourceTag"))) \
            .withColumn("ProductTag", non_empty_filter_udf(col("ProductTag"))) \
            .withColumn("CostResourceTag", concat_ws(",", col("CostResourceTag"))) \
            .withColumn("ProductTag", concat_ws(",", col("ProductTag"))) \
            .write \
            .format("jdbc") \
            .mode("overwrite") \
            .option("url", args.jdbc_url) \
            .option("dbtable", args.jdbc_table) \
            .save()

        all_billing_data.toDF() \
            .withColumn("CostResourceTag", non_empty_filter_udf(col("CostResourceTag"))) \
            .select( explode("CostResourceTag").alias("CostResourceTag")) \
            .distinct() \
            .write \
            .format("jdbc") \
            .mode("overwrite") \
            .option("url", args.jdbc_url) \
            .option("dbtable", args.jdbc_table+"_tags") \
            .save()

    if args.output_path:
        all_billing_data.toDF() \
            .withColumn("CostResourceTag", non_empty_filter_udf(col("CostResourceTag"))) \
            .withColumn("ProductTag", non_empty_filter_udf(col("ProductTag"))) \
            .withColumn("CostResourceTag", concat_ws(",", col("CostResourceTag"))) \
            .withColumn("ProductTag", concat_ws(",", col("ProductTag"))) \
            .write.mode('overwrite').options(delimiter='\t', header=True).csv(output_path + "/all_billing")

        all_billing_data.toDF() \
            .withColumn("CostResourceTag", non_empty_filter_udf(col("CostResourceTag"))) \
            .select( explode("CostResourceTag").alias("CostResourceTag")) \
            .distinct() \
            .write.mode('overwrite').options(delimiter='\t', header=True).csv(output_path + "/all_billing_tags")
