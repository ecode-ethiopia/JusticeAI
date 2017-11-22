import unittest

import numpy

from feature_extraction.clustering.hdbscan.hdbscan_wrapper import HDBSCANWrapper
from util.constant import Path


class TestHdbscan(unittest.TestCase):
    def test_hdbscan(self):
        matrix = numpy.matrix([[2, 3, 4, 5], [2, 1, 6, 7], [2, 54, 12, 23]])
        sentence = numpy.array(["I shot the supremacist.", "Over 9000", "Bruce lee"])
        files = numpy.array([["1"], ["2"], ["3"]])
        data_tuple = (matrix, sentence, files)
        hdb = HDBSCANWrapper(data_tuple, 'fact', 2, 1)
        hdb.cluster()
        expected_cluster = """I shot the supremacist.\nOver 9000\nBruce lee\n\n------------------------------------------\n\n1\n2\n3\n"""
        file = Path.cluster_directory + r"fact/-1.txt"
        text = ""
        file = open(file, "r")
        for lines in file:
            text += lines
        file.close()
        self.assertEqual(text, expected_cluster)
