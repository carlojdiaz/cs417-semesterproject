import sys
from typing import (Iterator, Tuple)

from parse_temps import (parse_raw_temps)


def global_least_squares_approx():
    """
    Driver function for global least squares approximation
    """
    input_temps = sys.argv[1]

    # will contain all the temperature values of each core
    core_0_temps = []
    core_1_temps = []
    core_2_temps = []
    core_3_temps = []

    # fill with temperature values of each core
    with open(input_temps, 'r') as temps_file:
        for temps_as_floats in parse_raw_temps(temps_file):
            core_0_temps.append((temps_as_floats[0], temps_as_floats[1][0]))
            core_1_temps.append((temps_as_floats[0], temps_as_floats[1][1]))
            core_2_temps.append((temps_as_floats[0], temps_as_floats[1][2]))
            core_3_temps.append((temps_as_floats[0], temps_as_floats[1][3]))

    # will contain a tuple with constants obtained from solving augmented matrices
    # first value in tuple will be c0, or the y-intercept of global approximated line
    # second value in tuple will be c1, or the slope of global approximated line
    global_lsa_constants = []

    global_lsa_constants.append(solve_augmented_matrix(core_0_temps))
    global_lsa_constants.append(solve_augmented_matrix(core_1_temps))
    global_lsa_constants.append(solve_augmented_matrix(core_2_temps))
    global_lsa_constants.append(solve_augmented_matrix(core_3_temps))

    print_output(global_lsa_constants)

def solve_augmented_matrix(core_temps) -> Tuple[float, float]:
    n = len(core_temps)
    sum_x = 0
    sum_f = 0
    sum_x_f = 0
    sum_x_squared = 0
    c0 = 0
    c1 = 0

    for i in core_temps:
        sum_x += i[0]
        sum_f += i[1]
        sum_x_f += i[0] * i[1]
        sum_x_squared += (sum_x) ^2

    c0 = ( (sum_x_squared * sum_f) - (sum_x * sum_x_f) ) / ( (n * sum_x_squared) - (sum_x ^ 2) )
    c1 = ( (n * sum_x_f) - (sum_x * sum_f) ) / ( (n * sum_x_squared) - (sum_x ^ 2) )

    return (c0, c1)


def print_output(core_global_lsa_constants):
    """
    Write the data for each core's temperatures into a text file

    Args:
        core_global_last_constants: list containing the times (upper and lower bound), slope, and y-intercept for each line

    Print:

    """
    index = 0
    for data in core_global_lsa_constants:
        y_intercept = data[0]
        slope = data[1]
        print(f"core_{index:<11}; y  =  {y_intercept:{12}.{4}f}  +  {slope:{8}.{4}f}x; global least squares approximation")
        index += 1



if __name__ == "__main__":
    global_least_squares_approx()