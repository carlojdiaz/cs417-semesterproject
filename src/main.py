import sys
from typing import (Iterator, Tuple)

from parse_temps import (parse_raw_temps)


def main():
    """
    Driver function for project
    """
    input_temps = sys.argv[1]
    base_name = sys.argv[1][0:len(sys.argv[1]) - 4]
    time=[]

    # will contain all the temperature values of each core
    core_0_temps = []
    core_1_temps = []
    core_2_temps = []
    core_3_temps = []

    # will contain data pertaining to the line between each temperature value (interpolation)
    core_0_lines = []
    core_1_lines = []
    core_2_lines = []
    core_3_lines = []

    # fill with temperature values of each core
    with open(input_temps, 'r') as temps_file:
        for temps_as_floats in parse_raw_temps(temps_file):
            time.append(temps_as_floats[0])
            core_0_temps.append(temps_as_floats[1][0])
            core_1_temps.append(temps_as_floats[1][1])
            core_2_temps.append(temps_as_floats[1][2])
            core_3_temps.append(temps_as_floats[1][3])

    # append the evaluated values to the list containing the line data
    index = 0
    for t in time:
        core_0_lines.append(interpolate(time, core_0_temps, index))
        core_1_lines.append(interpolate(time, core_1_temps, index))
        core_2_lines.append(interpolate(time, core_2_temps, index))
        core_3_lines.append(interpolate(time, core_3_temps, index))
        index += 1
        if index == len(time) - 1:
            break


    # will contain a tuple with constants obtained from solving augmented matrices (global lsa)
    # first value in tuple will be c0, or the y-intercept of global approximated line
    # second value in tuple will be c1, or the slope of global approximated line
    core_0_global_lsa_constants = solve_augmented_matrix(time, core_0_temps)
    core_1_global_lsa_constants = solve_augmented_matrix(time, core_1_temps)
    core_2_global_lsa_constants = solve_augmented_matrix(time, core_2_temps)
    core_3_global_lsa_constants = solve_augmented_matrix(time, core_3_temps)


    # write the data from interpolation and global lsa in a fixed format to a .txt file
    write_output(core_0_lines, core_0_global_lsa_constants, 0, base_name)
    write_output(core_1_lines, core_1_global_lsa_constants, 1, base_name)
    write_output(core_2_lines, core_2_global_lsa_constants, 2, base_name)
    write_output(core_3_lines, core_3_global_lsa_constants, 3, base_name)



def interpolate(times, core_temps, index) -> Iterator[Tuple[Tuple[float, float], Tuple[float,float]]]:
    """
    Perform linear interpolation to find the exact line between each temperature in the given core

    Args:
        times: a list of the times
    
        core_temps: a list of a single core's temperatures

        index: the index of the core currently being worked on

    Return:
        a tuple of tuples, where:
            the first tuple contains the lower time bound and the upper time bound
            the second tuple contains the slope of the line and the y-intercept of the line
    """
    x_1 = times[index]
    x_2 = times[index+1]
    y_1 = core_temps[index]
    y_2 = core_temps[index+1]
    slope = (y_2 - y_1) / (x_2 - x_1)
    y_intercept = y_1 - (slope * x_1)

    time_ranges = (x_1, x_2)
    line_data = (slope, y_intercept)

    return ((time_ranges, line_data))


def solve_augmented_matrix(times, core_temps) -> Tuple[float, float]:
    """
    Solve the resulting vector in the augmented matrix developed by performing global least squares approximation

    Args:
        times: a list of the times
    
        core_temps: a list of a single core's temperatures

    Return:
        a tuple, where:
            the first index contains c0, the y-intercept of the approximated line
            the second index contains c1, the slope of the approximated line
    """
    n = len(times)
    sum_x = 0
    sum_f = 0
    sum_x_f = 0
    sum_x_squared = 0
    c0 = 0
    c1 = 0

    temp_index = 0
    for t in times:
        sum_x += t
        sum_f += core_temps[temp_index]
        sum_x_f += t * core_temps[temp_index]
        sum_x_squared += sum_x ^ 2
        temp_index += 1

    c0 = ( (sum_x_squared * sum_f) - (sum_x * sum_x_f) ) / ( (n * sum_x_squared) - (sum_x ^ 2) )
    c1 = ( (n * sum_x_f) - (sum_x * sum_f) ) / ( (n * sum_x_squared) - (sum_x ^ 2) )

    return (c0, c1)



def write_output(core_interpolated_lines, core_global_lsa_constants, core_number, base_name):
    """
    Write the data for the core's interpolated lines and approximated line from global least squares approximation into a text file

    Args:
        core_interpolated_lines: list containing the times (upper and lower bound), slope, and y-intercept for each line

        core_global_lsa_constants: tuple that holds the constants for the core's approximated line
            first index: contains the approximated y-intercept
            second index: contains the approximated slope

        core_number: the number of the core being printed

        base_name: the name of the .txt file used for input

    Write:
        generate a text file, titled with its respective core number, and write all the lines between each point
    """
    index = 0
    with open(f"{base_name}-core-{core_number}.txt", 'w') as wf:
        for data in core_interpolated_lines:
            time_1 = data[0][0]
            time_2 = data[0][1]
            slope = data[1][0]
            y_intercept = data[1][1]
            wf.write(f"{time_1:5} <= x < {time_2:6}; y_{index:<7}  =  {y_intercept:{12}.{4}f}  +  {slope:{8}.{4}f}x; interpolation\n")
            index += 1

        wf.write("\n")
        approximated_y_intercept = core_global_lsa_constants[0]
        approximated_slope = core_global_lsa_constants[1]
        wf.write(f'{"y":>22} {"=":>10} {approximated_y_intercept:{14}.{4}f} + {approximated_slope:{9}.{4}f}x; global least squares approximation')


if __name__ == "__main__":
    main()