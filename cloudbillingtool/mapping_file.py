import re
import csv
from datetime import datetime

from pyspark.shell import spark


def load_mapping_file(file_location):
    return \
        spark.read \
        .format("csv") \
        .option("header", "true") \
        .option("delimiter", "\t") \
        .option("multiLine", "true") \
        .option("ignoreTrailingWhiteSpace", "true") \
        .load(file_location)