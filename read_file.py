# coding=utf-8
#

from xlrd import open_workbook
from xlrd.xldate import xldate_as_datetime


def read_file(filename, starting_row=0):
	"""
	Read index time series information from the Excel file.
	"""
	wb = open_workbook(filename=filename)
	ws = wb.sheet_by_index(0)

	fields = read_data_fields(ws, 0)
	
	row = 1
	dates = []
	indices = initialize_indices(fields)
	while row < ws.nrows:
		if is_blank_line(ws, row):
			break

		dates.append(xldate_as_datetime(ws.cell_value(row, 0), 0))
		for column in range(1, len(fields)):
			indices[fields[column]].append(ws.cell_value(row, column))

		row = row + 1
	# end of while loop

	return dates, indices



def initialize_indices(fields):
	indices = {}
	for i in range(1, len(fields)):
		indices[fields[i]] = []

	return indices



def read_data_fields(ws, row):
	column = 0
	fields = []
	while column < ws.ncols:
		cell_value = ws.cell_value(row, column)
		if is_empty_cell(ws, row, column):
			break

		fields.append(cell_value.strip())
		column = column + 1

	return fields



def is_blank_line(ws, row):
	for i in range(5):
		if not is_empty_cell(ws, row, i):
			return False

	return True



def is_empty_cell(ws, row, column):
	cell_value = ws.cell_value(row, column)
	if not isinstance(cell_value, str) or cell_value.strip() != '':
		return False
	else:
		return True