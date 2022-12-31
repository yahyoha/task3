import unittest
from unittest import mock
from pathlib import Path

from pandas import DataFrame
from pyspark.sql import SparkSession

import cloudbillingtool.mapping_file as mapping_file

spark = SparkSession \
    .builder \
    .appName("sparkTest") \
    .getOrCreate()

class TestMappingFile(unittest.TestCase):

    def testResourceIdTagMappingFile(self):
        table: DataFrame = mapping_file.load_mapping_file(spark, "tests/data/resource_mapping.csv", mapping_file.resource_schema).toDF()
        self.assertEqual(len(table.columns), 2)
        # Todo: test columns == [CostResourceID	CostResourceTag]

    def testTypeTagMappingFile(self):
        table: DataFrame = mapping_file.load_mapping_file(spark, "tests/data/type_mapping.csv", mapping_file.type_schema).toDF()
        self.assertEqual(len(table.columns), 2)
        # Todo: test columns == [Type	CostResourceTag]
