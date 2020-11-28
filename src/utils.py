import os
import re
import time
import routes
import pickle

def mytime(tstamp):
	return round(time.time() - tstamp, 2)

def mytimeprint(current_time, start_time):
	print('\n\t--- took %s / %s seconds ---' % (mytime(current_time), mytime(start_time)))
	return time.time()

def zeros_padding_to_number_digits(mystring):
	"""
	Returns all numbers on 5 digits to let sort the string with numeric order.
	Ex: zeros_padding_to_number_digits("a6b12.125")  ==> "a00006b00012.00125"
	"""
	return ''.join([format(int(x), '05d') if x.isdigit() else x for x in re.split(r'(\d+)', mystring)])

def build_quick_routes(puzzle, input_list):
	# Build class from input list
	input_routes = routes.routes_class(puzzle)
	input_routes.stop_list = input_list[:]
	input_routes.update_vans_from_stop_list(puzzle)

	return input_routes

def pickle_route_class(puzzle, route, filename):
	# load file name and path
	pathname = puzzle.output_path + "/solutions"
	if not os.path.exists(pathname):
		os.makedirs(pathname)
	picklename = pathname + "/" + filename
	# create a pickle file
	picklefile = open(picklename, 'wb')
	# pickle the route and write it to file
	pickle.dump(route, picklefile)
	# close the file
	picklefile.close()
