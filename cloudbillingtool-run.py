#!python3

import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws
from cloudbillingtool import all_billing

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--hetzner_data', help='Path to Hetzner data files' )
    parser.add_argument('--azure_data', help='Path to Azure data files' )
    parser.add_argument('--aws_data', help='Path to AWS data files' )
    parser.add_argument('--metadata', help='Path to metadata (mapping files) directory')
    parser.add_argument('--output_path', help='Path to output directory')
    args = parser.parse_args()

    hetzner_data = args.hetzner_data
    azure_data = args.azure_data
    aws_data = args.aws_data
    metadata_dir = args.metadata
    output_path = args.output_path

    # Initialize the spark context.
    spark = SparkSession\
        .builder\
        .appName("CloudBillingTool")\
        .getOrCreate()

    # combine azure with hetzner billing
    all_billing_data = all_billing.generate_uniform_data_from(spark, azure_data, hetzner_data, aws_data, metadata_dir )

    # Map the CostResourceTag to a joined Tag list as a string
    # write to file
    all_billing_data.toDF() \
        .withColumn("CostResourceTag", concat_ws(";", col("CostResourceTag"))) \
        .write.mode('overwrite').options(delimiter='\t', header=True).csv(output_path+"/all_billing")