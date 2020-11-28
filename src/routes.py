import re
import datetime as dt
import random as rnd
import numpy as np
from math import ceil
import params


def zeros_padding_to_number_digits(mystring):
	"""
	Returns all numbers on 5 digits to let sort the string with numeric order.
	Ex: zeros_padding_to_number_digits("a6b12.125")  ==> "a00006b00012.00125"
	"""
	return ''.join([format(int(x), '05d') if x.isdigit() else x for x in re.split(r'(\d+)', mystring)])

class routes_class(object):

	def __init__(self, puzzle):
		self.num_vans = puzzle.max_vans
		self.max_duty = puzzle.max_duty
		self.min_duty = puzzle.min_duty
		self.num_stops = puzzle.num_stops
		self.departure = puzzle.departure_time
		self.total_time = None
		self.total_distance = None
		self.stop_list = []

	# Initial random first set of routes
	def build_at_random(self, puzzle, seed_val=12345):

		print("\n Initialisation of Routes at Random...")

		self.routes_start_at_depot(puzzle.depot_id)

		stop_list = puzzle.stop_list[:]
		list_left = len(stop_list)

		rnd.seed(seed_val)
		rnd.shuffle(stop_list)

		m = n = 0
		while list_left:

			start = self.van_stop_list[m][n]
			end = stop_list.pop(0)

			self.routes_append_postcode(puzzle, m, n, start, end)

			m = m + 1
			if m == self.num_vans:
				m = 0
				n = n + 1

			list_left -= 1

		self.routes_end_at_depot(puzzle)

		assert self.routes_sumup() == self.num_stops

		self.update_stop_list_from_vans()

	# Initial postcode-sector split set of routes
	def build_from_postcodes(self, puzzle):

		print("\n Initialisation of Routes from Sorted Postcodes...")

		self.routes_start_at_depot(puzzle.depot_id)

		avg_deliveries_per_van = int(ceil(self.num_stops / self.num_vans))

		stop_list = puzzle.data.postcode.str.replace(" ","").apply\
			(lambda x: zeros_padding_to_number_digits(x)).sort_values().index.tolist()
		list_left = len(stop_list)

		m = n = 0
		while list_left:
			start = self.van_stop_list[m][n]
			end = stop_list.pop(0)

			self.routes_append_postcode(puzzle, m, n, start, end)

			n += 1
			if n == avg_deliveries_per_van:
				n = 0
				m += 1

			list_left -= 1

		self.routes_end_at_depot(puzzle)

		assert self.routes_sumup() == self.num_stops

		self.update_stop_list_from_vans()

	# Validity Rule for optimisation
	def evaluate_routes_time(self):
		max_van_time = max([item[-1] for item in self.van_times])
		if max_van_time > params.max_duty:
			return "Invalid"
		else:
			return "Valid"

	# Validity Rule for optimisation
	def invalid_routes_max_time(self):
		if max([item[-1] for item in self.van_times]) > self.max_duty:
			return True
		else:
			return False

	# Validity Rule for optimisation
	def invalid_routes_min_time(self):
		if min([item[-1] for item in self.van_times]) < self.min_duty:
			return True
		else:
			return False

	# Validity Rule if needs to keep the Van number constant
	def accept_routes_fixed_fleet_size(self):
		if self.num_vans != params.max_vans:
			return False
		else:
			return True

	def routes_start_at_depot(self, depot_id):
		self.van_id = [(i + 1) for i in range(self.num_vans)]
		self.van_stop_list = [[depot_id] for i in range(self.num_vans)]
		self.van_times = [[0] for i in range(self.num_vans)]
		self.van_distances = [[0] for i in range(self.num_vans)]
		self.van_num_stops = [0] * self.num_vans

	def routes_append_postcode(self, puzzle, m, n, start, end):
		self.van_stop_list[m].append(end)
		self.van_times[m].append(self.van_times[m][n] + puzzle.time_mtx.loc[start, end] + params.service_time)
		self.van_distances[m].append(self.van_distances[m][n] + puzzle.distance_mtx.loc[start, end])
		self.van_num_stops[m] += 1

	def routes_end_at_depot(self, puzzle):
		for m in range(self.num_vans):
			n = self.van_num_stops[m]
			start = self.van_stop_list[m][n]
			end = puzzle.depot_id

			self.van_times[m].append(self.van_times[m][n] + puzzle.time_mtx.loc[start, end])
			self.van_distances[m].append(self.van_distances[m][n] + puzzle.distance_mtx.loc[start, end])
			self.van_stop_list[m].append(end)

	def routes_sumup(self):
		self.total_time = 0
		self.total_distance = 0
		tot_stops = 0
		for m in range(self.num_vans):
			self.total_time += self.van_times[m][-1]
			self.total_distance += self.van_distances[m][-1]
			tot_stops += self.van_num_stops[m]
		return tot_stops

	# remove consecutive depots in stop_list
	def remove_adjacent_depots(self, puzzle):
		stop_array = np.array(self.stop_list)
		stop_roll = np.roll(stop_array, -1)
		myfilter = np.where(~((stop_array == stop_roll) & (stop_array == puzzle.depot_id)))
		self.stop_list = list(stop_array[myfilter])

	# Unfold stop-list into vans
	def update_vans_from_stop_list(self, puzzle):
		# Drop empty vans
		self.remove_adjacent_depots(puzzle)
		# Number of separate vans
		self.num_vans = self.stop_list.count(puzzle.depot_id)

		stop_cnt = 0
		route_cnt = 0

		self.van_id = [(i + 1) for i in range(self.num_vans)]
		self.van_stop_list = [[] for i in range(self.num_vans)]
		self.van_stop_list[route_cnt].append(puzzle.depot_id)
		self.van_times = [[0] for i in range(self.num_vans)]
		self.van_distances = [[0] for i in range(self.num_vans)]

		for idx, stop in enumerate(self.stop_list[1:]):
			stop_cnt += 1
			previous = self.van_stop_list[route_cnt][-1]
			self.van_times[route_cnt].append(self.van_times[route_cnt][-1]
											 + puzzle.time_mtx.loc[previous, stop] + puzzle.service_time)
			self.van_distances[route_cnt].append(self.van_distances[route_cnt][-1]
											 + puzzle.distance_mtx.loc[previous, stop])
			self.van_stop_list[route_cnt].append(stop)

			if stop == puzzle.depot_id:
				self.van_times[route_cnt][-1] -= puzzle.service_time
				route_cnt += 1
				self.van_stop_list[route_cnt].append(stop)

		previous = self.van_stop_list[route_cnt][-1]
		stop = puzzle.depot_id
		self.van_times[route_cnt].append(self.van_times[route_cnt][-1] + puzzle.time_mtx.loc[previous, stop])
		self.van_distances[route_cnt].append(self.van_distances[route_cnt][-1] + puzzle.distance_mtx.loc[previous, stop])
		self.van_stop_list[route_cnt].append(puzzle.depot_id)

		assert (route_cnt + 1) == self.num_vans

		self.van_num_stops = [len(subroute) - 2 for subroute in self.van_stop_list]

		assert self.routes_sumup() == self.num_stops

	# Fold vans into stop-list
	def update_stop_list_from_vans(self):
		self.stop_list = [stops for subroute in self.van_stop_list for stops in subroute[:-1]]
		return self.stop_list

	# Set times for delivery
	def update_wallclock(self):
		start_time = self.departure
		start_time = dt.datetime.strptime(start_time, '%H:%M')

		self.vans_wallclock = [[] for i in range(self.num_vans)]
		for m in range(self.num_vans):
			self.vans_wallclock[m].append(start_time)
			for n in range(1, self.van_num_stops[m] + 1):
				self.vans_wallclock[m].append(start_time + dt.timedelta(minutes=np.int(self.van_times[m][n])))

			self.vans_wallclock[m].append(start_time + dt.timedelta(minutes=np.int(self.van_times[m][-1])))

	def print_route_stats(self):
		print("\t---------")
		print('\tNumber of Vans    =', self.num_vans)
		print('\tNumber of Stops   =', self.num_stops)
		print("\t---------")
		for m in range(self.num_vans):
			print('\t\tVan', self.van_id[m],
				  '\t Stops =', "%2d" % self.van_num_stops[m],
				  '\t Time =', "%3.f" % self.van_times[m][-1], '[min]',
				  '\t Distance =', "%3.f" % self.van_distances[m][-1], '[km]')
		print("\t---------")
		print('\tCumulative Time      =', "%3.f" % self.total_time, '[min]')
		print('\tCumulative Distance  =', "%3.f" % self.total_distance, '[min]')
		print("\t---------")
		print("\tRoute Evaluation: ", self.evaluate_routes_time())
		print("\t---------")

