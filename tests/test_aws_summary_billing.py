import unittest
import sys
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws
from cloudbillingtool import aws_summary_billing

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

spark = SparkSession \
    .builder \
    .appName("sparkTest") \
    .getOrCreate()


class TestAwsBilling(unittest.TestCase):

    def testAwsBillingLoad(self):
        aws_billing_with_tags = aws_summary_billing.load_files_with_mapping(spark, "tests/data/aws_cost_summary/*.csv", "tests/metadata")

        output_df = aws_billing_with_tags \
            .withColumn("CostResourceTag", concat_ws(";", col("CostResourceTag"))) \
            .withColumn("ProductTag", concat_ws(";", col("ProductTag")))

        for row in output_df.collect():
            print(row)
