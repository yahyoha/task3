import unittest
from unittest import mock
from pathlib import Path

from pandas import DataFrame

from cloudbillingtool.mapping_file import load_mapping_file


class TestTagMappingFile(unittest.TestCase):

    def testResourceIdTagMappingFile(self):
        table: DataFrame = load_mapping_file("tests/data/resourceid_mapping_table.csv").toPandas()
        self.assertEqual(len(table.columns), 2)
        # Todo: test columns == [CostResourceID	CostResourceTag]

    def testTypeTagMappingFile(self):
        table: DataFrame = load_mapping_file("tests/data/type_mapping_table.csv").toPandas()
        self.assertEqual(len(table.columns), 2)
        # Todo: test columns == [Type	CostResourceTag]
