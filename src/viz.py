import os
import folium
from folium.features import DivIcon
import numpy as np
from datetime import datetime, timedelta
import params
import matplotlib.pyplot as plt
import ast

coloricons_choices = [
    'red', 'blue', 'green', 'orange', 'purple', 'pink', 'cadetblue', 'darkred', 'darkblue',
    'darkgreen', 'darkpurple', 'lightred', 'lightblue', 'lightgreen',
    'lightgray', 'gray', 'beige'
]
colorlines_choices = [
    'red', 'blue', 'green', 'orange', 'purple',
    'pink', 'cadetblue', 'darkred', 'darkblue',
    'darkgreen', 'indigo', 'tomato', 'lightblue',
    'lightgreen', 'lightgray', 'gray', 'beige'
]

def init_map(puzzle, map_name):

    fmap = folium.Map(location=[puzzle.data.latitude.mean(), puzzle.data.longitude.mean()], zoom_start=params.zoom_level)

    for i in puzzle.data.postcode:
        POSTCODE = i
        POP = 'Postcode ' + POSTCODE + '-\tID: ' + puzzle.data.loc[puzzle.data.postcode == POSTCODE].index.values[0]
        LAT = puzzle.data.loc[puzzle.data.postcode == POSTCODE].latitude.values[0]
        LON = puzzle.data.loc[puzzle.data.postcode == POSTCODE].longitude.values[0]

        folium.Marker([LAT, LON], popup=POP).add_to(fmap)

    start_time = params.departure_time
    start_time = datetime.strptime(start_time, '%H:%M')
    label = 'Depot -' + ' Postcode: ' + puzzle.depot_postcode + '-\tTime: ' + str(start_time.time())[:-3]

    folium.Marker([puzzle.depot_latitude, puzzle.depot_longitude], popup=label, icon=folium.Icon(color='black')).add_to(fmap)

    map_path = puzzle.output_path + "/maps"
    if not os.path.exists(map_path):
        os.makedirs(map_path)

    map_filename = map_path + "/" + map_name
    fmap.save(map_filename)

    return fmap


def routes_map(puzzle, routes, map_name):

    fmap = folium.Map(location=[puzzle.data.latitude.mean(), puzzle.data.longitude.mean()], zoom_start=params.zoom_level)

    LAT_DEPOT = puzzle.depot_latitude
    LON_DEPOT = puzzle.depot_longitude

    start_time = params.departure_time
    start_time = datetime.strptime(start_time, '%H:%M')

    line0 = '<div style="font-size: 11pt"> -------------------------------'
    line1 = '<div style="font-size: 11pt"> Number of Vans    =  %d </div>' % (routes.num_vans)
    line2 = '<div style="font-size: 11pt"> Number of Stops   =  %d </div>' % (routes.num_stops)
    line3 = '<div style="font-size: 11pt"> Total Time        =  %.f [min] </div>' % (routes.total_time)
    line4 = '<div style="font-size: 11pt"> Route Evaluation  =  %s </div>'%(routes.evaluate_routes_time())

    label = line0 + line1 + line2 + line0 + line3 + line0 + line4 + line0

    folium.Marker([LAT_DEPOT, LON_DEPOT], icon=DivIcon(icon_size=(250, 250), icon_anchor=(-500, 350), html=label)).add_to(fmap)

    for m in range(routes.num_vans):
        points = [tuple([LAT_DEPOT, LON_DEPOT])]
        for n in range(1, routes.van_num_stops[m] + 1):
            PC_ID = routes.van_stop_list[m][n]
            POSTCODE = puzzle.data.loc[puzzle.data.index == PC_ID].postcode.values[0]
            LAT = puzzle.data.loc[puzzle.data.index == PC_ID].latitude.values[0]
            LON = puzzle.data.loc[puzzle.data.index == PC_ID].longitude.values[0]
            DELTAT = timedelta(minutes=int(routes.van_times[m][n]))
            TIME = start_time + DELTAT
            POP = 'Route #'+str(m + 1) + '\t-\tStop #'+str(n) + '\t-\tPostcode: ' + POSTCODE + '\t-\tTime: ' + str(TIME.strftime('%H:%M'))

            folium.Marker([LAT, LON], popup=POP, icon=folium.Icon(color=coloricons_choices[m % len(coloricons_choices)])).add_to(fmap)
            points.append(tuple([LAT, LON]))

        points.append(tuple([LAT_DEPOT, LON_DEPOT]))

        folium.PolyLine(points, color=colorlines_choices[m % len(colorlines_choices)], weight=2.5, opacity=1).add_to(fmap)

    folium.map.LayerControl(postition='topleft').add_to(fmap)

    POSTCODE = puzzle.depot_postcode
    label = 'Depot -' + ' Postcode: ' + POSTCODE + '-\tTime: ' + str(start_time.time())[:-3]
    folium.Marker([LAT_DEPOT, LON_DEPOT], popup=label, icon=folium.Icon(color='black')).add_to(fmap)

    map_path = puzzle.output_path + "/maps"
    map_filename = map_path + "/" + map_name
    fmap.save(map_filename)

    return fmap

def plot_travel_data_distributions(puzzle, fig_name):
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(15, 7))
    ax1.hist(puzzle.time_mtx.values.flatten(), 20)
    ax1.set_xlabel('Time (min)')
    ax1.set_ylabel('Count')
    ax1.set_title(r'Distribution of times A -> B')

    ax2.hist(puzzle.distance_mtx.values.flatten(), 20)
    ax2.set_xlabel('Distance (km)')
    ax2.set_ylabel('Count')
    ax2.set_title(r'Distribution of distances A -> B')

    fig_path = puzzle.output_path + "/figs"
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
    fig_filename = fig_path + "/" + fig_name

    plt.savefig(fig_filename)

    return plt

def plot_travel_metric_scatter(puzzle, fig_name):
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.scatter(puzzle.time_mtx.values.flatten(), puzzle.distance_mtx.values.flatten())
    ax.set_xlabel('Time (min)')
    ax.set_ylabel('Distance (Km)')
    ax.set_title(r'Travel data relationship')

    fig_path = puzzle.output_path + "/figs"
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
    fig_filename = fig_path + "/" + fig_name

    plt.savefig(fig_filename)

    return plt

def plot_convergence_cost(puzzle, record_perf_df, fig_name):
    plt.figure(figsize=(10, 6))
    plt.grid()
    plt.plot(record_perf_df.iter, record_perf_df.route_cost, color='blue', label='route cost')
    plt.plot(record_perf_df.iter, record_perf_df.best_cost, color='red', label='best cost')
    plt.title('Search Convergence')
    plt.xlabel('Number of iterations')
    plt.ylabel('Total time of routes')
    plt.legend()#loc='center right', bbox_to_anchor=(0.95, 1.05))

    fig_path = puzzle.output_path + "/figs"
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
    fig_filename = fig_path + "/" + fig_name

    plt.savefig(fig_filename)

    return plt

def plot_cost_per_van(puzzle, record_perf_df, fig_name):
    route_van_times = [ast.literal_eval(x) for x in record_perf_df.route_drive_time.values]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.boxplot(route_van_times)
    ax.set_title('Boxplot of explored van duties')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Duty time')
    ax.set_xticks(range(0, len(record_perf_df), 5))
    ax.set_xticklabels(range(0, len(record_perf_df), 5))

    ax2 = ax.twinx()
    ax2.plot(record_perf_df.index, record_perf_df.route_num_vans, label="num_vans")
    ax2.set_ylabel('Number vans in solution')
    ax2.set_ylim(0, puzzle.max_vans + 1)

    plt.legend(loc='upper left')
    plt.tight_layout()

    fig_path = puzzle.output_path + "/figs"
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
    fig_filename = fig_path + "/" + fig_name
    fig.savefig(fig_filename)

