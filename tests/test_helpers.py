import unittest
import sys
import os

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cloudbillingtool import helper

def filterCostResourceTag(mapping_file, column, filterValue ):
    return mapping_file.loc[mapping_file[column].str.contains("Base-image")]['CostResourceTag']


class TestHelpers(unittest.TestCase):

    def testMergeAndJoinExtraction(self):
        mapping_files_path = "tests/metadata/mappingfiles"

        resource_mapping_df = pd.read_csv(mapping_files_path + "/resource_mapping.csv", sep='\t')
        type_mapping_df = pd.read_csv(mapping_files_path + "/type_mapping.csv", sep='\t')

        # We would like to test if the idea works with dataframes

        # fillter CostReourceTags from typemapping for column Type
        filtered_df = type_mapping_df.loc[type_mapping_df['Type'].str.contains("Base-image")]['CostResourceTag']
        self.assertEqual(list(filtered_df) , ['IT-OPS'])

        # fillter CostReourceTags from typemapping for column Type
        filtered_df = type_mapping_df.loc[type_mapping_df['Type'].str.contains("Cloud-Projekt")]['CostResourceTag']
        self.assertEqual(list(filtered_df), ['IT-OPS', 'IT-OPS', 'IT-OPS', 'IT-OPS'] )

        # fillter CostReourceTags from typemapping for column CostResourceID
        filtered_df = resource_mapping_df.loc[resource_mapping_df['CostResourceID'].str.contains("1355658")]['CostResourceTag']
        self.assertEqual(list(filtered_df), ['CPO'])

        # fillter CostReourceTags from typemapping for column CostResourceID
        filtered_df = resource_mapping_df.loc[resource_mapping_df['CostResourceID'].str.contains("2164922")]['CostResourceTag']
        self.assertEqual(list(filtered_df), ['Integration'])

        # fillter ProductTag from typemapping for column CostResourceID
        filtered_df = resource_mapping_df.loc[resource_mapping_df['CostResourceID'].str.contains("1355658")]['ProductTag']
        self.assertEqual(list(filtered_df), ['gitlab-runner1'])

        # fillter ProductTag from typemapping for column CostResourceID
        filtered_df = resource_mapping_df.loc[resource_mapping_df['CostResourceID'].str.contains("asdasds")]['ProductTag']
        self.assertEqual(list(filtered_df), [])