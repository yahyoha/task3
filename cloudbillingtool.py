#!python
# Example Usage: python3 cloudbillingtool.py tests/data/hetzner/*.csv * tests/data /tmp/cloudbillingtool_output/

import sys
from pyspark.sql import SparkSession
from pyspark import SparkContext
import cloudbillingtool.azure_billing as azure_billing
import cloudbillingtool.hetzner_billing as hetzner_billing


sc = SparkContext()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(sys.argv)
        print("Usage: cloudbillingtool.py <hetzner_data> <azure_data> <work_dir> <output_path>", file=sys.stderr)
        sys.exit(-1)

    hetzner_data = sys.argv[1]
    azure_data = sys.argv[2]
    work_dir = sys.argv[3]
    output_path = sys.argv[4]

    print(sys.argv)

    # Initialize the spark context.
    spark = SparkSession\
        .builder\
        .appName("CloudBillingTool")\
        .getOrCreate()

    azure_billing_with_tags = azure_billing.load_files_with_mapping(spark, azure_data, work_dir)
    hetzner_billing_with_tags = hetzner_billing.load_files_with_mapping(spark, hetzner_data,work_dir)

    # combine azure with hetzner billing
    all_billing = azure_billing_with_tags.rdd.union(hetzner_billing_with_tags.rdd)

    # write to file
    all_billing.toDF().write.mode('overwrite').options(delimiter='\t', header=True).csv(output_path+"/all_billing")