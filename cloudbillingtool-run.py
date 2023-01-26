#!python
# Example ./cloudbillingtool-run.py --hetzner_data "tests/data/hetzner/*.csv" --azure_data "tests/data/azure/*.csv" --metadata "tests/metadata" --output_path "/tmp/output2"

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
    parser.add_argument('--jdbc_url', help='JDBC Connection String')
    parser.add_argument('--jdbc_table', help='JDBC Target Table')
    parser.add_argument('--jdbc_user', help='JDBC User')
    parser.add_argument('--jdbc_password', help='JDBC Password')


    args = parser.parse_args()

    hetzner_data = args.hetzner_data
    azure_data = args.azure_data
    aws_data = args.aws_data
    metadata_dir = args.metadata
    output_path = args.output_path

    # Initialize the spark context.
    spark = SparkSession\
        .builder\
        .appName("CloudBillingTool") \
        .getOrCreate()

    spark.sparkContext.addPyFile("lib/spark-mssql-connector-1.0.2.jar")

    print("Spark Version "+spark.version)

    # combine azure with hetzner billing
    all_billing_data = all_billing.generate_uniform_data_from(spark, azure_data, hetzner_data, aws_data, metadata_dir )

    # Map the CostResourceTag to a joined Tag list as a string
    # write to file| summarize sum(Costs)
    if args.jdbc_url:
        all_billing_data.toDF() \
            .withColumn("CostResourceTag", concat_ws(";", col("CostResourceTag"))) \
            .withColumn("ProductTag", concat_ws(";", col("ProductTag"))) \
            .write \
            .jdbc("com.microsoft.sqlserver.jdbc.spark") \
            .mode("overwrite") \
            .option("url", args.jdbc_url) \
            .option("dbtable", args.jdbc_table) \
            .option("user", args.jdbc_user) \
            .option("password", args.jdbc_password) \
            .option("tableLock", "true") \
            .option("batchsize", "500") \
            .option("reliabilityLevel", "BEST_EFFORT") \
            .save()

    if args.output_path:
        all_billing_data.toDF() \
            .withColumn("CostResourceTag", concat_ws(";", col("CostResourceTag"))) \
            .withColumn("ProductTag", concat_ws(";", col("ProductTag"))) \
            .write.mode('overwrite').options(delimiter='\t', header=True).csv(output_path + "/all_billing")
