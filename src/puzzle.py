import os
import sys
import pandas as pd
import params

class puzzle_class(object):

	def __init__(self, input=params):
		""" Data Access Paths """
		self.input_path = None
		self.output_path = None
		""" Depot Properties """
		self.depot_id = 'depot'
		self.depot_name = input.depot_name
		self.depot_sample = input.sample_name
		self.depot_postcode = None
		self.depot_latitude = None
		self.depot_longitude = None
		""" Puzzle Constraints """
		self.max_vans = input.max_vans
		self.max_duty = input.max_duty
		self.min_duty = input.min_duty
		self.service_time = input.service_time
		self.departure_time = input.departure_time
		""" Puzzle Dataset """
		self.load_dataset()
		self.printout()

	def load_dataset(self):
		# Dataset management
		self.load_data_path()
		# Reading the parcel dataframe
		suffix = "parcels.csv"
		self.data = self.load_data_file(suffix)
		# Quick tidying of data
		self.split_depot_to_parcel()
		# Reading the *time* travel matrix
		suffix = "time.csv"
		self.time_mtx = self.load_data_file(suffix)
		# Reading the *distance* travel matrix
		suffix = "distance.csv"
		self.distance_mtx = self.load_data_file(suffix)

	def load_data_path(self):
		# Path to load the puzzle dataset
		self.input_path = "../data/input/" + self.depot_name + "/" + self.depot_sample + "/"
		# Path to save the engine outputs
		self.output_path = "../data/output/" + self.depot_name + "/" + self.depot_sample + "/"

		if not os.path.exists(self.output_path):
			os.makedirs(self.output_path)

	def load_data_file(self, suffix):
		for fname in os.listdir(self.input_path):
			if fname.endswith(suffix):
				filename = os.path.join(self.input_path, fname)
				data_df = pd.read_csv(filename, sep=",", index_col=0)
				break
		else:
			sys.exit("\nNo Puzzle found in path %s\n" % self.input_path)
		return data_df

	def split_depot_to_parcel(self):
		# Recording Depot coordinates
		self.depot_postcode = self.data.loc[self.data.index == 'depot'].postcode.values[0]
		self.depot_latitude = self.data.loc[self.data.index == 'depot'].latitude.values[0]
		self.depot_longitude = self.data.loc[self.data.index == 'depot'].longitude.values[0]
		# Subsetting parcel only data
		self.data = self.data.loc[self.data.index != 'depot']
		self.stop_list = list(self.data.index)
		self.num_stops = len(self.stop_list)

	def printout(self):

		print("\nPuzzle Constraints:\n")
		print("\t Depot Name:            %s" % self.depot_name)
		print("\t Depot Postcode:        %s" % self.depot_postcode)
		print("\t Depot Latitude:        %s" % self.depot_latitude)
		print("\t Depot Longitude:       %s" % self.depot_longitude)
		print("\t Depot Max Fleet Size:   %s [vans]" % self.max_vans)
		print("\t Depot Max Duty Time:  %3d [min]" % self.max_duty)
		print("\t Depot Service Time:   %3d [min]" % self.service_time)
		print("\nDelivery Points Coordinates:\n")
		print(self.data)
