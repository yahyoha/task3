import unittest
from unittest import mock
from pathlib import Path

from pandas import DataFrame

import cloudbillingtool.hetzner_billing as hetzner_billing


class TestHetznerBilling(unittest.TestCase):
    def testHetznerBillingLoad(self):
        table: DataFrame = hetzner_billing.load_files("tests/data/hetzner/*.csv").toDF()
        table.show()
        #self.assertEqual(len(table), 868)