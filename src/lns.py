from random import sample, shuffle, seed, randrange
from math import floor
import numpy as np
from utils import build_quick_routes


class lns_class(object):
	"""
	This class implements the Large Neighbourhood Search algorithm by Pisinger, D., & Ropke, S. (2010)
	"""

	def __init__(self, puzzle, routes, lns_destroy_frac, seed_val):
		self.stop_list = routes.stop_list  # current route
		self.num_stops = routes.num_stops  # number of stops in the current route
		self.lns_destroy_nb = int(
			floor(lns_destroy_frac * self.num_stops))  # number of stops to remove in the destroy step
		self.puzzle = puzzle  # puzzle object
		self.depot_id = puzzle.depot_id  # identifier of the depot

		seed(seed_val)

	def rnd_destroy(self):
		"""
		This function performs the random destroy operator: it removes "lns_destroy_nb" stops from the current route.
		"""

	def compute_insert_array(self, current_list, stops_insert, add_hub):
		"""
		This function calculates the cost of inserting the selected stop at every possible position in the partial stop list.
		"""
		if add_hub:
			current_list = np.append(current_list, self.depot_id)

		outward_array = self.puzzle.time_mtx.loc[
			stops_insert, current_list[1:]].values  # from insert_dp to part
		inward_array = self.puzzle.time_mtx.loc[
			current_list[:-1], stops_insert].T.values  # from part to insert_dp
		current_array = np.diag(
			self.puzzle.time_mtx.loc[current_list[:-1], current_list[1:]])
		insert_array = inward_array + outward_array - current_array
		return insert_array

	def update_insert_array(self):
		"""
		This function updates the insert_array after having inserted a delivery stop in the partial stop list.
		"""
		self.insert_array = np.delete(self.insert_array, self.stop_idx, axis=0)
		self.insert_array = np.insert(self.insert_array, self.insertion_idx, 0, axis=1)
		if len(self.partial_stop_list) - 1 == self.insertion_idx:
			insert_array_add = self.compute_insert_array(
				self.partial_stop_list[(self.insertion_idx - 1):(self.insertion_idx + 1)],
				self.stops_removed,
				True)
		else:
			insert_array_add = self.compute_insert_array(
				self.partial_stop_list[(self.insertion_idx - 1):(self.insertion_idx + 2)],
				self.stops_removed,
				False)
		self.insert_array[:,
		(self.insertion_idx - 1):(self.insertion_idx + 1)] = insert_array_add  # update 2 columns of insert_array

	def rnd_repair(self):
		"""
		This function performs the random repair operator: it inserts a random removed stop at its cheapest position in the partial route
		This is recursively performed until all removed stops are inserted.
		"""
		shuffle(self.stops_removed)
		while self.stops_removed:  # until every dp have been added
			self.insert_stop = self.stops_removed.pop(0)  # insert first dp
			self.insert_array = self.compute_insert_array(self.stop_list, self.insert_stop,
														  True)  # calculate cost of insertion into each possible position
			self.insertion_idx = np.argmin(self.insert_array) + 1  # index of minimum
			self.partial_stop_list = list(
				np.insert(self.partial_stop_list, self.insertion_idx, self.insert_stop))  # insert dp
		self.new_stop_list_repair = self.partial_stop_list

	def greedy_repair(self):
		"""
		This function perform the greedy operator: it inserts the cheapest removed stop ats its cheapest position in the partial route.
		This is recursively performed until all removed stops are inserted.
		"""

	def run(self):
		"""
		This function run the LNS algorithm and create a new route object.
		"""
		self.rnd_destroy()
		self.greedy_repair()
		new_route = build_quick_routes(self.puzzle, self.new_stop_list_repair)
		return new_route
