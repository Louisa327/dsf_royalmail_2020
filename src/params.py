## Sample Variables
depot_name = "EDINBURGH"
sample_name = "sample_050"

## Hard Constraints
max_vans = 5
max_duty = 360
min_duty = 90
service_time = 5
departure_time = "10:00"

## OR-tools variables
# Options available are: "GREEDY_DESCENT", "TABU_SEARCH", "GUIDED_LOCAL_SEARCH", "SIMULATED_ANNEALING"
search_ortools_options = "GREEDY_DESCENT"
num_ortools_iters = 100
spancost_coeff = 0

## LNS Variable
lns_destroy_frac = 0.4
lns_max_iter = 100

## Simulated Annealing Parameters
sa_control_temp = 1.25 # Needs to be greater than 1
sa_cooling_rate = 0.75 # Needs to be smaller than 1

## Map Zoom Option
zoom_level = 10