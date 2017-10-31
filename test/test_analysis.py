"""
Test the open_jpm.py
"""

import unittest2
from datetime import datetime
from os.path import join
from stock_analysis.analysis import moving_correlation, moving_index_correlation
from stock_analysis.read_file import read_file
from stock_analysis.utility import get_current_directory



class TestAnalysis(unittest2.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestAnalysis, self).__init__(*args, **kwargs)



    def test_read_file(self):
        file = join(get_current_directory(), 'samples', 'index_sample1.xlsx')
        dates, indices = read_file(file)
        self.assertEqual(len(dates), 15)
        self.assertEqual(dates[0], datetime(2010,5,21))
        self.assertEqual(dates[14], datetime(2010,6,10))
        self.assertEqual(len(indices), 3)
        self.assertEqual(len(indices['CSI300']), 15)
        self.assertAlmostEqual(indices['CSI300'][0], 2768.791)
        self.assertAlmostEqual(indices['ZhongZheng 500'][0], 3982.385)
        self.assertAlmostEqual(indices['Chuang Ye Ban'][0], 0)
        self.assertAlmostEqual(indices['CSI300'][14], 2750.023)
        self.assertAlmostEqual(indices['ZhongZheng 500'][14], 4223.566)
        self.assertAlmostEqual(indices['Chuang Ye Ban'][14], 1117.478)



    def test_moving_correlation(self):
        s1 = [1,2,3,4]
        s2 = [4,5,6,9]
        result = moving_correlation(3, s1, s2)
        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(result[0][0], 1.0)
        self.assertAlmostEqual(result[0][1], 0.0)
        self.assertAlmostEqual(result[1][0], 0.960768923)
        self.assertAlmostEqual(result[1][1], 0.178912375)



    def test_moving_index_correlation(self):
        file = join(get_current_directory(), 'samples', 'index_sample1.xlsx')
        dates, indices = read_file(file)

        dates2, correlation = moving_index_correlation(5, dates, indices['CSI300'], indices['ZhongZheng 500'])
        self.assertEqual(len(dates2), 11)
        self.assertEqual(dates2[0], datetime(2010,5,27))
        self.assertEqual(dates2[10], datetime(2010,6,10))
        self.assertEqual(len(correlation), 11)
        self.assertAlmostEqual(correlation[0][0], 0.872911784)
        self.assertAlmostEqual(correlation[10][0], 0.760721226)

        dates3, correlation = moving_index_correlation(5, dates, indices['ZhongZheng 500'], indices['Chuang Ye Ban'])
        self.assertEqual(len(dates3), 5)
        self.assertEqual(dates3[0], datetime(2010,6,4))
        self.assertEqual(dates3[4], datetime(2010,6,10))
        self.assertEqual(len(correlation), 5)
        self.assertAlmostEqual(correlation[0][0], 0.702914316)
        self.assertAlmostEqual(correlation[4][0], 0.746776576)

