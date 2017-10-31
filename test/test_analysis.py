"""
Test the open_jpm.py
"""

import unittest2
from datetime import datetime
from os.path import join
from stock_analysis.analysis import moving_correlation, get_index_returns, \
                                    moving_indices_return_correlation
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



    def test_get_index_returns(self):
        file = join(get_current_directory(), 'samples', 'index_sample1.xlsx')
        dates, indices = read_file(file)

        dates, index_returns = get_index_returns(dates, indices)
        self.assertEqual(len(dates), 8)
        self.assertEqual(dates[0], datetime(2010,6,1))
        self.assertEqual(dates[7], datetime(2010,6,10))

        self.assertEqual(len(index_returns), 3)
        self.assertEqual(len(index_returns['CSI300']), 8)
        self.assertAlmostEqual(index_returns['CSI300'][0], -1.049377196)
        self.assertAlmostEqual(index_returns['CSI300'][7], -1.154150431)

        self.assertEqual(len(index_returns['Chuang Ye Ban']), 8)
        self.assertAlmostEqual(index_returns['Chuang Ye Ban'][0], -2.6767)
        self.assertAlmostEqual(index_returns['Chuang Ye Ban'][7], 3.679175523)



    def test_moving_indices_return_correlation(self):
        file = join(get_current_directory(), 'samples', 'index_sample1.xlsx')
        dates, indices = read_file(file)
        dates2, correlations = moving_indices_return_correlation(5, dates, indices)
        self.assertEqual(len(dates2), 4)
        self.assertEqual(dates2[0], datetime(2010,6,7))
        self.assertEqual(dates2[3], datetime(2010,6,10))

        self.assertEqual(len(correlations), 3)
        for name in correlations:
            if 'ZhongZheng' in name and 'CSI300' in name:
                zz500_csi300 = correlations[name]
            elif 'Chuang Ye Ban' in name and 'CSI300' in name:
                chuangye_csi300 = correlations[name]
            else:
                zz500_chuangye = correlations[name]

        self.assertEqual(len(zz500_csi300), 4)
        self.assertAlmostEqual(zz500_csi300[0][0], 0.760362648)
        self.assertAlmostEqual(zz500_csi300[3][0], 0.993147601)

        self.assertEqual(len(zz500_chuangye), 4)
        self.assertAlmostEqual(zz500_chuangye[0][0], 0.735154396)
        self.assertAlmostEqual(zz500_chuangye[3][0], -0.669078755)

        self.assertEqual(len(chuangye_csi300), 4)
        self.assertAlmostEqual(chuangye_csi300[0][0], 0.143796753)
        self.assertAlmostEqual(chuangye_csi300[3][0], -0.646945593)


    # def test_write_csv(self):
    #     file = join(get_current_directory(), 'samples', 'index_sample1.xlsx')
    #     dates, indices = read_file(file)
    #     dates2, correlation = moving_index_return_correlation(5, dates, indices['CSI300'], indices['ZhongZheng 500'])
    #     write_csv(dates2, correlation, 'csi300-zhongzheng500', join(get_current_directory(), 'samples'))

    #     dates3, correlation = moving_index_return_correlation(5, dates, indices['ZhongZheng 500'], indices['Chuang Ye Ban'])
    #     write_csv(dates3, correlation, 'zhongzheng500-chuangyeban', join(get_current_directory(), 'samples'))
