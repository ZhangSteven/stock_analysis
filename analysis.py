# coding=utf-8
# 
# Doing analysis for index movements.
#
# 
from scipy.stats.stats import pearsonr
from stock_analysis.utility import get_current_directory

class InconsistentLength(Exception):
	pass

import logging
logger = logging.getLogger(__name__)



def moving_index_correlation(move_length, dates, index1, index2):
	"""
	Compute the moving correlation between two indices.
	"""
	skip_zeros = max(count_leading_zeros(index1), count_leading_zeros(index2))
	return dates[move_length+skip_zeros-1:], \
			moving_correlation(move_length, index1[skip_zeros:], index2[skip_zeros:])



def count_leading_zeros(index):
	"""
	The data file uses zero to represent a missing value of an index.
	So we count the number of leading zeros of that index.
	"""
	for i in range(len(index)):
		if index[i] != 0:
			break

	return i



def moving_correlation(move_length, s1, s2):
	"""
	Compute the moving correlation between two series: s1, s2.

	Return: a list containing the moving correlation between s1 and s2,
		each element of that list is of the form (coe, p_value)
	"""
	result = []
	if len(s1) != len(s2):
		logger.error('moving_correlation(): inconsistent length, s1:{0}, s2:{1}'.
						format(len(s1), len(s2)))
		raise InconsistentLength()

	if move_length > len(s1):
		return result

	for i in range(0, len(s1)-move_length+1):
		result.append(get_correlation(s1[i:i+move_length], s2[i:i+move_length]))

	return result



def get_correlation(s1, s2):
	"""
	Compute correlation between two series: s1 and s2. They are equal in length.
	"""
	return pearsonr(s1, s2)



if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)

	# import os
	# data_file = os.path.join(get_current_directory(), 'data files', 'A-share-index.xlsx')
	# dates, indices = read_file(data_file)
	# write_csv(dates[20:], moving_correlation(20, indices['CSI300'], indices['ZhongZheng 500']))


