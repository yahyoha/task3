
# Example Usage: python3 cloudbillingtool.py tests/data/hetzner/*.csv * tests/data /tmp/cloudbillingtool_output/

import sys
import cloudbillingtool.all_billing
from cloudbillingtool import all_billing
from pyspark.sql import SparkSession
import pyspark

from pyspark import SparkContext
sc =SparkContext()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: cloudbillingtool.py <hetzner_data> <azure_data> <work_dir> <output_path>", file=sys.stderr)
        sys.exit(-1)

    hetzner_data = sys.argv[1]
    azure_data = sys.argv[2]
    work_dir = sys.argv[3]
    output_path = sys.argv[4]

    # Initialize the spark context.
    spark = SparkSession\
    .builder\
    .appName("CloudBillingTool")\
    .getOrCreate()

    bills = cloudbillingtool.all_billing.load_all_with_tags(spark, hetzner_data, azure_data, work_dir )

    bills.write.mode('overwrite').options(delimiter='\t').csv(output_path+"/all_bills")