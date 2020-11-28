import sys
import time
from datetime import datetime
from puzzle import puzzle_class
from routes import routes_class
from ortools_solver import run_or_tools
from vrp_solver import run_vrp_solver
from manifest import printout
import utils
import viz

def main():

    start_time = time.time()
    start_date = datetime.now()

    print("\n##################################################################\n")
    print("\t...Loading Dataset...")

    puzzle = puzzle_class()

    viz.init_map(puzzle, "delivery_point_locations.html")

    current_time = utils.mytimeprint(start_time, start_time)

    print("\n##################################################################\n")
    print("\t...Building Initial Routes...")

    init_routes = routes_class(puzzle)

    init_routes.build_from_postcodes(puzzle)
    # init_routes.build_at_random(puzzle)

    viz.routes_map(puzzle, init_routes, "init_routes_postcodes.html")

    print("\n\t...Inital Solution...\n")
    init_routes.print_route_stats()

    current_time = utils.mytimeprint(current_time, start_time)

    print("\n##################################################################\n")
    print("\t...Running OR-tools solver...\n")

    or_routes = run_or_tools(puzzle, init_routes)

    viz.routes_map(puzzle, or_routes, "ortools_routes_solution.html")

    print("\n##################################################################\n")
    print("\t...OR-tools solution...\n")

    or_routes.print_route_stats()

    current_time = utils.mytimeprint(current_time, start_time)

    # print("\n##################################################################\n")
    # print("\t...Running LNS solver...\n")
    #
    # final_route, record_perf_df = run_vrp_solver(puzzle, init_routes)
    #
    # current_time = utils.mytimeprint(current_time, start_time)
    #
    # print("\n##################################################################\n")
    #
    # print("\n\t...Optimised Solution...\n")
    #
    # final_route.print_route_stats()
    #
    # printout(puzzle, final_route, "final_routes_postcodes_manifest.csv")
    #
    # # Recording outputs
    # viz.routes_map(puzzle, final_route, "final_routes_postcodes.html")
    # viz.plot_convergence_cost(puzzle, record_perf_df, 'convergence_costs.png')
    # viz.plot_cost_per_van(puzzle, record_perf_df, "boxplot_per_iter.png")
    # utils.pickle_route_class(puzzle, final_route, "final_routes_postcodes.pckl")
    #
    # current_time = utils.mytimeprint(current_time, start_time)
    #
    # print("\n##################################################################\n")
    # end_date = datetime.now()
    # print("-----\nVRP engine ran on the %02d-%02d-%4d\n" % (start_date.day, start_date.month, start_date.year))
    # print('... started at ' + start_date.strftime("%H:%M:%S"))
    # print('... finished at ' + end_date.strftime("%H:%M:%S"))
    # print('\ntook %s [h:m:s] \n-----' % str(end_date - start_date).split('.')[0])
    #
    # return final_route, record_perf_df


if __name__ == '__main__':
    main()
