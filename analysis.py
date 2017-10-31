# coding=utf-8
# 
# Doing analysis for index movements.
#
# 
from scipy.stats.stats import pearsonr
from statistics import mean, median, stdev
from stock_analysis.utility import get_current_directory, get_output_directory
from stock_analysis.read_file import read_file
import os, csv

class InconsistentLength(Exception):
	pass

import logging
logger = logging.getLogger(__name__)



def moving_indices_return_correlation(move_length, dates, indices):
	"""
	Compute the move return correlation among a group of indices.
	"""
	dates, index_returns = get_index_returns(dates, indices)
	index_names = list(index_returns.keys())
	correlations = {}
	for i in range(len(index_names)):
		for j in range(i+1, len(index_names)):
			correlations[index_names[i]+'-'+index_names[j]] = \
				moving_correlation(move_length, index_returns[index_names[i]], index_returns[index_names[j]])

	return dates[move_length-1:], correlations



def get_correlation_stats(correlations, num_dates):
	"""
	Compute the mean, median and standard deviation of the correlation
	coefficients on each date.
	"""
	stats = []
	for i in range(num_dates):
		coe_list = [correlations[name][i][0] for name in correlations]
		stats.append((mean(coe_list), median(coe_list), stdev(coe_list)))
	
	return stats

	

# def moving_index_return_correlation(move_length, dates, index1, index2):
# 	"""
# 	Compute the moving correlation between two indices.
# 	"""
# 	dates, index1_return, index2_return = get_index_returns(dates, index1, index2)
# 	return dates[move_length-1:], \
# 			moving_correlation(move_length, index1_return, index2_return)



def get_index_returns(dates, indices):
	"""
	Computer the index return for each date.
	"""
	leading_zeros = []
	for index_name in indices:
		leading_zeros.append(count_leading_zeros(indices[index_name]))

	skip_zeros = max(leading_zeros)

	index_returns = {}
	for index_name in indices:
		index_returns[index_name] = get_return_percentage(indices[index_name][skip_zeros:])

	return dates[1+skip_zeros:], index_returns



def get_return_percentage(index):
	r = []
	for i in range(1,len(index)):
		r.append((index[i]/index[i-1] - 1.0)*100.0)

	return r



def count_leading_zeros(index):
	"""
	For index, it uses zero to represent a missing value, for return value, it uses
	-100 to represent a missing value.
	"""
	for i in range(len(index)):
		if not index[i] in [0, -100]:
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



def write_csv(dates, correlations, stats, name, output_dir=get_output_directory()):
	file = os.path.join(output_dir, name+'.csv')
	with open(file, 'w', newline='') as csvfile:
		file_writer = csv.writer(csvfile, delimiter=',')

		cor_names = [name for name in correlations]
		file_writer.writerow(['date'] + cor_names + ['mean', 'median', 'stdev'])
		for i in range(len(dates)):
			file_writer.writerow([date_to_string(dates[i])] + \
									[correlations[name][i][0] for name in cor_names] + \
									[stats[i][0], stats[i][1], stats[i][2]])
		# end of for loop

	# end of with



def date_to_string(dt):
	return str(dt.year) + '-' + str(dt.month) + '-' + str(dt.day)



if __name__ == '__main__':
	import logging.config
	logging.config.fileConfig('logging.config', disable_existing_loggers=False)

	file = os.path.join(get_current_directory(), 'data files', 'ZhongZheng500 industry index.xlsx')
	dates, indices = read_file(file)
	dates2, correlations = moving_indices_return_correlation(60, dates, indices)
	stats = get_correlation_stats(correlations, len(dates2))
	write_csv(dates2, correlations, stats, 'coe_A_shares')
