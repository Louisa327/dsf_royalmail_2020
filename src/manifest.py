import os
import sys
import pandas as pd
import string

hash=string.ascii_letters+string.digits
#####################################
def printout(puzzle, solution, filename):
	# load file name and path
	pathname = puzzle.output_path + "/solutions"
	if not os.path.exists(pathname):
		os.makedirs(pathname)
	manifest_name = pathname + "/" + filename
	# Create dataframe with both DO-hub and DP coordinates
	fields = ['barcode', 'postcode', 'latitude', 'longitude',
			  'van_number', 'stop_number',
			  'delta_distance', 'cumul_distance',
			  'delta_time', 'cumul_time', 'wallclock_time']
	manifest = pd.DataFrame(columns=fields)
	# Setting solution wallclock
	solution.update_wallclock()
	# Preparing solution
	solution.van_id = [(i + 1) for i in range(solution.num_vans)]

	cnt_dps = 0
	for i in range(solution.num_vans):
		for j in range(solution.van_num_stops[i]+2):
			if solution.van_stop_list[i][j] == puzzle.depot_id:
				drop = 0
				parcel_pc = puzzle.depot_postcode
				parcel_lat = puzzle.depot_latitude
				parcel_long = puzzle.depot_longitude
			else:
				drop = j
				parcel_pc = puzzle.data.postcode[puzzle.data.index==solution.van_stop_list[i][j]].values[0]
				parcel_lat = puzzle.data.latitude[puzzle.data.index==solution.van_stop_list[i][j]].values[0]
				parcel_long = puzzle.data.longitude[puzzle.data.index == solution.van_stop_list[i][j]].values[0]

			if j == 0: delta_distance = 0; delta_time = 0
			else:
				delta_distance = round(solution.van_distances[i][j] - solution.van_distances[i][j-1],3)
				delta_time = round(solution.van_times[i][j] - solution.van_times[i][j-1],2)

			row_to_append = {'barcode': solution.van_stop_list[i][j],
							 'postcode': parcel_pc,
							 'latitude': parcel_lat,
							 'longitude': parcel_long,
							 'van_number': solution.van_id[i],
							 'stop_number': drop,
							 'delta_distance': delta_distance,
							 'cumul_distance': round(solution.van_distances[i][j],3),
							 'delta_time': delta_time,
							 'cumul_time': round(solution.van_times[i][j],2),
							 'wallclock_time': solution.vans_wallclock[i][j]}

			manifest = manifest.append(row_to_append, ignore_index=True)

			cnt_dps += 1
		cnt_dps += 1

	manifest.wallclock_time = manifest.wallclock_time.dt.strftime('%H:%M')

	manifest.to_csv(manifest_name, sep=',')

